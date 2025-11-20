#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Doris数据库慢查询日志分析脚本 (生产版本)

功能：
- 分析Doris慢查询日志Excel文件
- 提取SQL模式、涉及的表、函数、字段等信息
- 生成详细的Markdown分析报告
- 支持自定义日期范围分析

使用方法：
    python analyze_slow_queries.py <excel_file_path> [options]

示例：
    # 分析指定Excel文件
    python analyze_slow_queries.py doc/20251118慢查询.xlsx

    # 分析最近7天的慢查询（需要按日期范围筛选的Excel文件）
    python analyze_slow_queries.py doc/慢查询_20251113-20251120.xlsx --days 7

    # 指定输出报告路径
    python analyze_slow_queries.py doc/20251118慢查询.xlsx --output doc/分析报告_20251118.md

作者：Claude Code
版本：2.0
更新时间：2025-11-20
"""

import pandas as pd
import re
import argparse
import sys
import os
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from pathlib import Path


class SlowQueryAnalyzer:
    """慢查询分析器"""

    def __init__(self, file_path, output_path=None, verbose=True):
        """
        初始化分析器

        Args:
            file_path: Excel文件路径
            output_path: 输出报告路径（可选，默认为输入文件同目录）
            verbose: 是否输出详细日志
        """
        self.file_path = file_path
        self.output_path = output_path
        self.verbose = verbose
        self.df = None
        self.sql_column = None
        self.time_column = None
        self.timestamp_column = None

    def log(self, message):
        """输出日志"""
        if self.verbose:
            print(message)

    def extract_table_names(self, sql):
        """提取SQL中的表名"""
        tables = set()
        patterns = [
            r'FROM\s+`?(\w+)`?',
            r'JOIN\s+`?(\w+)`?',
            r'INTO\s+`?(\w+)`?',
            r'UPDATE\s+`?(\w+)`?'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, sql, re.IGNORECASE)
            tables.update(matches)
        return list(tables)

    def extract_functions(self, sql):
        """提取SQL中使用的函数"""
        pattern = r'\b([A-Z_]+)\s*\('
        functions = re.findall(pattern, sql)
        # 过滤掉常见关键字
        keywords = {
            'SELECT', 'FROM', 'WHERE', 'GROUP', 'ORDER', 'HAVING',
            'UNION', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP',
            'CASE', 'WHEN', 'THEN', 'ELSE', 'END'
        }
        functions = [f for f in functions if f not in keywords]
        return list(set(functions))

    def extract_where_fields(self, sql):
        """提取WHERE条件中的字段"""
        fields = set()
        where_match = re.search(
            r'WHERE\s+(.*?)(?:GROUP BY|ORDER BY|LIMIT|$)',
            sql,
            re.IGNORECASE | re.DOTALL
        )
        if where_match:
            where_clause = where_match.group(1)
            field_pattern = r'`?(\w+)`?\s*(?:=|>|<|>=|<=|!=|LIKE|IN|BETWEEN|IS)'
            fields.update(re.findall(field_pattern, where_clause, re.IGNORECASE))
        return list(fields)

    def extract_group_by_fields(self, sql):
        """提取GROUP BY字段"""
        fields = []
        group_by_match = re.search(
            r'GROUP BY\s+(.*?)(?:ORDER BY|HAVING|LIMIT|$)',
            sql,
            re.IGNORECASE | re.DOTALL
        )
        if group_by_match:
            group_by_clause = group_by_match.group(1).strip()
            fields = [f.strip().strip('`').strip(',') for f in group_by_clause.split(',')]
            fields = [f for f in fields if f and not f.startswith('(')]
        return fields

    def extract_order_by_fields(self, sql):
        """提取ORDER BY字段"""
        fields = []
        order_by_match = re.search(
            r'ORDER BY\s+(.*?)(?:LIMIT|$)',
            sql,
            re.IGNORECASE | re.DOTALL
        )
        if order_by_match:
            order_by_clause = order_by_match.group(1).strip()
            for field in order_by_clause.split(','):
                field = field.strip().strip('`')
                field = re.sub(r'\s+(ASC|DESC)\s*', '', field, flags=re.IGNORECASE).strip()
                if field and not field.startswith('('):
                    fields.append(field)
        return fields

    def normalize_sql(self, sql):
        """规范化SQL，提取SQL骨架（替换参数值）"""
        if pd.isna(sql):
            return ""

        # 替换字符串常量
        sql = re.sub(r"'[^']*'", "'?'", sql)
        # 替换数字常量
        sql = re.sub(r'\b\d+\b', '?', sql)
        # 替换IN子句中的值列表
        sql = re.sub(r'IN\s*\([^)]+\)', 'IN (?)', sql, flags=re.IGNORECASE)
        # 规范化空格
        sql = re.sub(r'\s+', ' ', sql).strip()

        return sql

    def load_data(self):
        """加载Excel数据"""
        self.log(f"正在读取文件: {self.file_path}")

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"文件不存在: {self.file_path}")

        # 读取Excel文件
        try:
            self.df = pd.read_excel(self.file_path)
        except Exception as e:
            raise Exception(f"读取Excel文件失败: {e}")

        self.log(f"文件列名: {self.df.columns.tolist()}")
        self.log(f"总记录数: {len(self.df)}")

        # 识别关键列
        self._identify_columns()

        if self.sql_column is None:
            raise ValueError("错误: 未找到SQL列! 请确保Excel文件包含SQL语句列")

    def _identify_columns(self):
        """识别Excel中的关键列"""
        for col in self.df.columns:
            col_lower = str(col).lower()
            if 'sql' in col_lower or 'query' in col_lower or 'stmt' in col_lower:
                self.sql_column = col
            if 'time' in col_lower and 'stamp' not in col_lower:
                if self.time_column is None:
                    self.time_column = col
            if 'timestamp' in col_lower or 'date' in col_lower:
                self.timestamp_column = col

        self.log(f"\n识别的列:")
        self.log(f"  SQL列: {self.sql_column}")
        self.log(f"  耗时列: {self.time_column}")
        self.log(f"  时间戳列: {self.timestamp_column}")

    def analyze(self):
        """执行分析"""
        self.log("\n开始分析...")

        # 基础统计
        stats = self._calculate_basic_stats()

        # SQL模式分组分析
        patterns_data = self._analyze_sql_patterns()

        # 生成报告
        report_path = self._generate_report(stats, patterns_data)

        self.log(f"\n=== 分析完成 ===")
        self.log(f"报告已生成: {report_path}")

        return report_path

    def _calculate_basic_stats(self):
        """计算基础统计信息"""
        stats = {
            'total_queries': len(self.df)
        }

        if self.time_column:
            # 转换为数值类型
            self.df[self.time_column] = pd.to_numeric(self.df[self.time_column], errors='coerce')
            df_valid = self.df[self.df[self.time_column].notna()]

            stats['valid_count'] = len(df_valid)
            stats['avg_time'] = df_valid[self.time_column].mean() if len(df_valid) > 0 else 0
            stats['max_time'] = df_valid[self.time_column].max() if len(df_valid) > 0 else 0
            stats['min_time'] = df_valid[self.time_column].min() if len(df_valid) > 0 else 0

            self.log(f"\n=== 基础统计 ===")
            self.log(f"总慢查询次数: {stats['total_queries']}")
            self.log(f"有效耗时记录数: {stats['valid_count']}")
            self.log(f"平均查询时间: {stats['avg_time']:.2f}ms")
            self.log(f"最大查询时间: {stats['max_time']:.2f}ms")
            self.log(f"最小查询时间: {stats['min_time']:.2f}ms")

        return stats

    def _analyze_sql_patterns(self):
        """分析SQL模式"""
        self.log(f"\n=== SQL模式分组分析 ===")

        sql_patterns = defaultdict(lambda: {
            'count': 0,
            'times': [],
            'tables': set(),
            'sqls': []
        })

        all_tables = set()
        all_functions = set()
        all_where_fields = set()
        all_group_by_fields = set()
        all_order_by_fields = set()

        for idx, row in self.df.iterrows():
            sql = str(row[self.sql_column]) if pd.notna(row[self.sql_column]) else ""
            if not sql or sql == 'nan':
                continue

            # 规范化SQL
            pattern = self.normalize_sql(sql)

            # 收集统计信息
            sql_patterns[pattern]['count'] += 1
            sql_patterns[pattern]['sqls'].append(sql)

            if self.time_column and pd.notna(row[self.time_column]):
                sql_patterns[pattern]['times'].append(float(row[self.time_column]))

            # 提取表名
            tables = self.extract_table_names(sql)
            sql_patterns[pattern]['tables'].update(tables)
            all_tables.update(tables)

            # 提取函数
            functions = self.extract_functions(sql)
            all_functions.update(functions)

            # 提取字段
            all_where_fields.update(self.extract_where_fields(sql))
            all_group_by_fields.update(self.extract_group_by_fields(sql))
            all_order_by_fields.update(self.extract_order_by_fields(sql))

        # 按出现频率排序
        sorted_patterns = sorted(sql_patterns.items(), key=lambda x: x[1]['count'], reverse=True)

        self.log(f"\nSQL模式总数: {len(sorted_patterns)}")
        self.log(f"涉及表数量: {len(all_tables)}")
        self.log(f"使用函数数量: {len(all_functions)}")

        return {
            'sorted_patterns': sorted_patterns,
            'all_tables': all_tables,
            'all_functions': all_functions,
            'all_where_fields': all_where_fields,
            'all_group_by_fields': all_group_by_fields,
            'all_order_by_fields': all_order_by_fields
        }

    def _generate_report(self, stats, patterns_data):
        """生成Markdown报告"""
        if self.output_path:
            report_path = self.output_path
        else:
            # 默认输出路径：输入文件同目录，添加"_分析报告.md"后缀
            report_path = self.file_path.replace('.xlsx', '_分析报告.md')

        with open(report_path, 'w', encoding='utf-8') as f:
            self._write_report_header(f)
            self._write_basic_stats(f, stats)
            self._write_top_slow_queries(f)
            self._write_pattern_analysis(f, patterns_data)
            self._write_table_analysis(f, patterns_data)
            self._write_function_analysis(f, patterns_data)
            self._write_field_analysis(f, patterns_data)
            self._write_optimization_suggestions(f, patterns_data)
            self._write_report_footer(f)

        return report_path

    def _write_report_header(self, f):
        """写入报告头部"""
        f.write("# Doris数据库慢查询分析报告\n\n")
        f.write(f"**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**分析文件**: {os.path.basename(self.file_path)}\n\n")
        f.write("---\n\n")

    def _write_basic_stats(self, f, stats):
        """写入基础统计"""
        f.write("## 一、总体统计\n\n")
        f.write("| 指标 | 数值 |\n")
        f.write("|------|------|\n")
        f.write(f"| 总慢查询次数 | {stats['total_queries']} |\n")

        if 'valid_count' in stats:
            f.write(f"| 有效耗时记录数 | {stats['valid_count']} |\n")
            f.write(f"| 平均查询时间 | {stats['avg_time']:.2f} ms |\n")
            f.write(f"| 最大查询时间 | {stats['max_time']:.2f} ms |\n")
            f.write(f"| 最小查询时间 | {stats['min_time']:.2f} ms |\n")

        f.write("\n")

    def _write_top_slow_queries(self, f):
        """写入TOP 10最慢SQL"""
        if not self.time_column:
            return

        f.write("## 二、TOP 10 最慢的SQL\n\n")
        df_valid = self.df[self.df[self.time_column].notna()]

        if len(df_valid) == 0:
            f.write("无有效耗时数据\n\n")
            return

        top10 = df_valid.nlargest(10, self.time_column)

        f.write("| 排名 | 耗时(ms) | 执行时间 | SQL语句 |\n")
        f.write("|------|----------|----------|----------|\n")

        for i, (idx, row) in enumerate(top10.iterrows(), 1):
            time_val = f"{row[self.time_column]:.2f}"
            timestamp_val = str(row[self.timestamp_column]) if self.timestamp_column and self.timestamp_column in row else "N/A"
            sql_preview = str(row[self.sql_column]).replace('|', '\\|').replace('\n', ' ')[:100] + "..."
            f.write(f"| {i} | {time_val} | {timestamp_val} | `{sql_preview}` |\n")

        f.write("\n")

        # 详细SQL
        f.write("### 详细SQL语句\n\n")
        for i, (idx, row) in enumerate(top10.iterrows(), 1):
            f.write(f"#### 第{i}名 (耗时: {row[self.time_column]:.2f}ms)\n\n")
            if self.timestamp_column and self.timestamp_column in row:
                f.write(f"**执行时间**: {row[self.timestamp_column]}\n\n")
            f.write("```sql\n")
            f.write(str(row[self.sql_column]) + "\n")
            f.write("```\n\n")

    def _write_pattern_analysis(self, f, patterns_data):
        """写入SQL模式分析"""
        sorted_patterns = patterns_data['sorted_patterns']

        f.write("## 三、慢查询类型分析（按频率排序）\n\n")
        f.write("| 排名 | 出现次数 | 平均耗时(ms) | 最大耗时(ms) | 涉及表 |\n")
        f.write("|------|----------|--------------|--------------|--------|\n")

        for i, (pattern, info) in enumerate(sorted_patterns[:10], 1):
            count = info['count']
            avg_time_val = f"{sum(info['times'])/len(info['times']):.2f}" if info['times'] else "N/A"
            max_time_val = f"{max(info['times']):.2f}" if info['times'] else "N/A"
            tables = ', '.join(sorted(info['tables'])) if info['tables'] else "无"
            f.write(f"| {i} | {count} | {avg_time_val} | {max_time_val} | {tables} |\n")

        f.write("\n")

        # 详细SQL模式
        f.write("### TOP 5 慢查询类型详情\n\n")
        for i, (pattern, info) in enumerate(sorted_patterns[:5], 1):
            f.write(f"#### 类型{i} (出现{info['count']}次)\n\n")
            f.write(f"**统计信息**:\n")
            f.write(f"- 出现次数: {info['count']}\n")
            if info['times']:
                f.write(f"- 平均耗时: {sum(info['times'])/len(info['times']):.2f}ms\n")
                f.write(f"- 最大耗时: {max(info['times']):.2f}ms\n")
                f.write(f"- 最小耗时: {min(info['times']):.2f}ms\n")
            f.write(f"- 涉及表: {', '.join(sorted(info['tables'])) if info['tables'] else '无'}\n\n")

            f.write("**SQL模式** (参数已替换为?):\n\n")
            f.write("```sql\n")
            f.write(pattern + "\n")
            f.write("```\n\n")

            if info['sqls']:
                f.write("**示例SQL**:\n\n")
                f.write("```sql\n")
                f.write(info['sqls'][0] + "\n")
                f.write("```\n\n")

    def _write_table_analysis(self, f, patterns_data):
        """写入表分析"""
        all_tables = patterns_data['all_tables']
        sorted_patterns = patterns_data['sorted_patterns']

        f.write("## 四、涉及的表清单\n\n")
        f.write(f"**表总数**: {len(all_tables)}\n\n")

        if all_tables:
            # 按表出现频率统计
            table_frequency = Counter()
            for pattern, info in sorted_patterns:
                for table in info['tables']:
                    table_frequency[table] += info['count']

            f.write("| 排名 | 表名 | 出现次数 |\n")
            f.write("|------|------|----------|\n")

            for i, (table, freq) in enumerate(table_frequency.most_common(), 1):
                f.write(f"| {i} | `{table}` | {freq} |\n")

        f.write("\n")

    def _write_function_analysis(self, f, patterns_data):
        """写入函数分析"""
        all_functions = patterns_data['all_functions']

        f.write("## 五、使用的函数清单\n\n")
        f.write(f"**函数总数**: {len(all_functions)}\n\n")

        if all_functions:
            for func in sorted(all_functions):
                f.write(f"- `{func}()`\n")
        else:
            f.write("无\n")

        f.write("\n")

    def _write_field_analysis(self, f, patterns_data):
        """写入字段分析"""
        all_where_fields = patterns_data['all_where_fields']
        all_group_by_fields = patterns_data['all_group_by_fields']
        all_order_by_fields = patterns_data['all_order_by_fields']

        # WHERE条件字段
        f.write("## 六、WHERE条件字段清单\n\n")
        f.write(f"**字段总数**: {len(all_where_fields)}\n\n")

        if all_where_fields:
            for field in sorted(all_where_fields):
                f.write(f"- `{field}`\n")
        else:
            f.write("无\n")

        f.write("\n")

        # GROUP BY字段
        f.write("## 七、GROUP BY字段清单\n\n")
        f.write(f"**字段总数**: {len(all_group_by_fields)}\n\n")

        if all_group_by_fields:
            for field in sorted(all_group_by_fields):
                f.write(f"- `{field}`\n")
        else:
            f.write("无\n")

        f.write("\n")

        # ORDER BY字段
        f.write("## 八、ORDER BY字段清单\n\n")
        f.write(f"**字段总数**: {len(all_order_by_fields)}\n\n")

        if all_order_by_fields:
            for field in sorted(all_order_by_fields):
                f.write(f"- `{field}`\n")
        else:
            f.write("无\n")

        f.write("\n")

    def _write_optimization_suggestions(self, f, patterns_data):
        """写入优化建议"""
        sorted_patterns = patterns_data['sorted_patterns']
        all_where_fields = patterns_data['all_where_fields']
        all_group_by_fields = patterns_data['all_group_by_fields']
        all_order_by_fields = patterns_data['all_order_by_fields']
        all_tables = patterns_data['all_tables']

        f.write("## 九、优化建议\n\n")
        f.write("### 1. 高频慢查询优化\n\n")
        f.write("针对出现频率TOP 5的慢查询类型，建议：\n\n")

        for i, (pattern, info) in enumerate(sorted_patterns[:5], 1):
            f.write(f"#### 类型{i} (出现{info['count']}次)\n\n")

            if info['tables']:
                f.write(f"**涉及表**: {', '.join(sorted(info['tables']))}\n\n")

            f.write("**优化方向**:\n\n")

            # 根据SQL模式给出建议
            pattern_lower = pattern.lower()

            if 'group by' in pattern_lower:
                f.write("- ✅ 检查GROUP BY字段是否有索引（INVERTED索引适用于低基数字段）\n")
                f.write("- ✅ 考虑使用聚合表（Rollup）或物化视图加速\n")

            if 'order by' in pattern_lower:
                f.write("- ✅ 检查ORDER BY字段是否有索引\n")
                f.write("- ✅ 考虑添加覆盖索引\n")

            if 'join' in pattern_lower:
                f.write("- ✅ 检查JOIN字段是否有索引\n")
                f.write("- ✅ 优化JOIN顺序（小表驱动大表）\n")

            if 'like' in pattern_lower:
                f.write("- ⚠️ 避免前导模糊查询（LIKE '%xxx'）\n")
                f.write("- ✅ 考虑使用INVERTED索引（Doris 2.0+）\n")

            if 'hour(' in pattern_lower or 'date_sub(' in pattern_lower or 'date_format(' in pattern_lower:
                f.write("- ⚠️ 动态函数（HOUR、DATE_SUB等）会导致索引失效\n")
                f.write("- ✅ 考虑添加预计算字段（如hour字段存储小时值）\n")

            if 'select *' in pattern_lower:
                f.write("- ⚠️ 避免SELECT *，只查询需要的字段\n")

            f.write("- ✅ 检查WHERE条件字段是否有合适的索引\n")
            f.write("- ✅ 分析是否可以优化SQL逻辑\n")
            f.write("- ✅ 考虑是否需要分区裁剪（PARTITION BY）\n\n")

        f.write("### 2. 索引优化建议\n\n")
        f.write("根据WHERE、GROUP BY、ORDER BY字段分析，建议检查以下字段的索引情况：\n\n")

        critical_fields = (all_where_fields | all_group_by_fields | all_order_by_fields)
        if critical_fields:
            f.write("**重点字段**（按字母排序）:\n\n")
            for field in sorted(critical_fields):
                f.write(f"- `{field}`\n")

            f.write("\n**索引类型选择**:\n\n")
            f.write("- INVERTED索引：适用于低基数字段（如状态、类型、小时等）\n")
            f.write("- BITMAP索引：适用于超低基数字段（如性别、是否删除等）\n")
            f.write("- BLOOM_FILTER索引：适用于高基数字段（如ID、订单号等）\n")

        f.write("\n")

        f.write("### 3. 表结构优化建议\n\n")

        if all_tables:
            f.write("建议对以下高频访问表进行优化：\n\n")

            # 统计表的出现频率
            table_frequency = Counter()
            for pattern, info in sorted_patterns:
                for table in info['tables']:
                    table_frequency[table] += info['count']

            for table, freq in table_frequency.most_common(10):
                f.write(f"#### `{table}` (出现{freq}次)\n\n")
                f.write(f"- ✅ 检查表结构是否合理（字段类型、数据模型）\n")
                f.write(f"- ✅ 检查是否需要分区（PARTITION BY DATE）\n")
                f.write(f"- ✅ 检查字段类型是否合适（避免过大的VARCHAR）\n")
                f.write(f"- ✅ 考虑是否需要添加预计算字段\n")
                f.write(f"- ✅ 检查数据模型（UNIQUE KEY vs AGGREGATE KEY）\n\n")

        f.write("\n")

    def _write_report_footer(self, f):
        """写入报告尾部"""
        f.write("---\n\n")
        f.write("## 附录：Doris优化参考资料\n\n")
        f.write("- [Doris官方文档 - 索引](https://doris.apache.org/zh-CN/docs/dev/data-table/index/index-overview/)\n")
        f.write("- [Doris官方文档 - 查询优化](https://doris.apache.org/zh-CN/docs/dev/query-acceleration/)\n")
        f.write("- [Doris INVERTED索引使用指南](https://doris.apache.org/zh-CN/docs/dev/data-table/index/inverted-index/)\n\n")
        f.write("---\n\n")
        f.write("*报告结束*\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Doris数据库慢查询日志分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 分析指定Excel文件
  python analyze_slow_queries.py doc/20251118慢查询.xlsx

  # 指定输出报告路径
  python analyze_slow_queries.py doc/20251118慢查询.xlsx --output doc/报告.md

  # 静默模式（不输出日志）
  python analyze_slow_queries.py doc/20251118慢查询.xlsx --quiet

建议:
  - 每周定期分析慢查询日志，及时发现性能问题
  - 将报告存档，方便对比历史优化效果
  - 结合Doris EXPLAIN PLAN分析具体SQL执行计划
        """
    )

    parser.add_argument(
        'file',
        help='慢查询Excel文件路径'
    )

    parser.add_argument(
        '-o', '--output',
        help='输出报告路径（可选，默认为输入文件同目录）',
        default=None
    )

    parser.add_argument(
        '-q', '--quiet',
        help='静默模式（不输出日志）',
        action='store_true'
    )

    parser.add_argument(
        '--days',
        help='分析最近N天的数据（仅用于说明，实际需要Excel文件已按日期筛选）',
        type=int,
        default=None
    )

    args = parser.parse_args()

    try:
        # 创建分析器
        analyzer = SlowQueryAnalyzer(
            file_path=args.file,
            output_path=args.output,
            verbose=not args.quiet
        )

        # 加载数据
        analyzer.load_data()

        # 执行分析
        report_path = analyzer.analyze()

        print(f"\n✅ 分析完成!")
        print(f"📄 报告文件: {report_path}")

        if args.days:
            print(f"📅 分析范围: 最近{args.days}天")

    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
