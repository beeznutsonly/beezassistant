package com.beezassistant.configurator;

import java.util.Arrays;
import java.util.Collections;
import java.util.stream.Collectors;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.data.rest.core.config.RepositoryRestConfiguration;
import org.springframework.data.rest.webmvc.config.RepositoryRestConfigurer;
import org.springframework.http.HttpMethod;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;
import org.springframework.web.servlet.config.annotation.CorsRegistry;

import com.beezassistant.configurator.models.Star;

@SpringBootApplication
public class ConfiguratorApplication implements RepositoryRestConfigurer {
	
	public static void main(String[] args) {
		SpringApplication.run(ConfiguratorApplication.class, args);
	}
	
	@Override
    public void configureRepositoryRestConfiguration(RepositoryRestConfiguration config, CorsRegistry cors) {
        config.exposeIdsFor(Star.class);
    }
	
	@Bean
    public CorsFilter corsFilter() {
        final UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        final CorsConfiguration config = new CorsConfiguration();
        config.setAllowCredentials(true);
        config.setAllowedOriginPatterns(Arrays.asList(
        		"http://localhost:3000", "http://192.168.*.*:3000",
                "https://configurator-react.herokuapp.com",
                "https://beezassistant-configurator.onrender.com"
        ));
        config.setAllowedHeaders(Collections.singletonList("*"));
        config.setExposedHeaders(Arrays.asList("*"));
        config.setAllowedMethods(Arrays.stream(HttpMethod.values()).map(HttpMethod::name).collect(Collectors.toList()));
        source.registerCorsConfiguration("/**", config);
        source.registerCorsConfiguration("/api/**", config);
        return new CorsFilter(source);
    }
}
