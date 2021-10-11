package com.beezassistant.configurator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.rest.core.config.RepositoryRestConfiguration;
import org.springframework.data.rest.webmvc.config.RepositoryRestConfigurer;
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
}
