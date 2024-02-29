package cn.city.parking.config.starter;

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

@Configuration
@PropertySource(factory = YamlPropertySourceFactory.class, value = {"classpath:application-${spring.profiles.active}.yml","classpath:bootstrap-${spring.profiles.active}.yml"})
public class CommonAutoConfig {
}
