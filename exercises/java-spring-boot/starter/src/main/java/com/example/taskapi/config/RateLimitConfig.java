package com.example.taskapi.config;

import com.example.taskapi.web.RateLimitingFilter;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(RateLimitProperties.class)
public class RateLimitConfig {

    @Bean
    FilterRegistrationBean<RateLimitingFilter> rateLimitingFilter(
            RateLimitProperties properties, ObjectMapper objectMapper) {
        FilterRegistrationBean<RateLimitingFilter> registration = new FilterRegistrationBean<>();
        registration.setFilter(new RateLimitingFilter(properties, objectMapper));
        registration.addUrlPatterns("/api/v1/*");
        registration.setOrder(1);
        return registration;
    }
}
