package com.beezassistant.configurator.models;

import java.io.Serializable;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

import org.springframework.data.rest.webmvc.spi.BackendIdConverter;
import org.springframework.stereotype.Component;

@Component
public class ScheduledCrosspostIdConverter implements BackendIdConverter {

	@Override
	public boolean supports(Class<?> delimiter) {
		return ScheduledCrosspost.class.equals(delimiter);
	}

	@Override
	public Serializable fromRequestId(String id, Class<?> entityType) {
		String[] parts = id.split("__");
		ScheduledCrosspostId scheduledCrosspostId = new ScheduledCrosspostId();
		scheduledCrosspostId.setSubreddit(parts[0]);
		try {
			scheduledCrosspostId.setUrl(
						URLDecoder.decode(
								parts[1],
								StandardCharsets.UTF_8.toString()
						)
				);
		} 
		catch (UnsupportedEncodingException ex) {
			scheduledCrosspostId = null;
		}
		return scheduledCrosspostId;
	}

	@Override
	public String toRequestId(Serializable id, Class<?> entityType) {
		ScheduledCrosspostId scheduledCrosspostId = (ScheduledCrosspostId) id;
		try {
			return String.format(
					"%s__%s", 
					scheduledCrosspostId.getSubreddit(),
					URLEncoder.encode(
							scheduledCrosspostId.getUrl(), 
							StandardCharsets.UTF_8.toString()
					)
			);
		}
		catch (UnsupportedEncodingException e) {
			return null;
		}
	}

}
