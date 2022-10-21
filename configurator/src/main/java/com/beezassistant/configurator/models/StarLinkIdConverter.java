package com.beezassistant.configurator.models;

import java.io.Serializable;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

import org.springframework.data.rest.webmvc.spi.BackendIdConverter;
import org.springframework.stereotype.Component;

@Component
public class StarLinkIdConverter implements BackendIdConverter {

	@Override
	public boolean supports(Class<?> delimiter) {
		return StarLink.class.equals(delimiter);
	}

	@Override
	public Serializable fromRequestId(String id, Class<?> entityType) {
		String[] parts = id.split("__");
		StarLinkId starLinkId = new StarLinkId();
		starLinkId.setStarName(parts[0]);
		try {
			starLinkId.setLink(
					URLDecoder.decode(
							parts[1],
							StandardCharsets.UTF_8.toString()
					)
			);
		} 
		catch (UnsupportedEncodingException e) {
			starLinkId = null;
		}
		return starLinkId;
	}

	@Override
	public String toRequestId(Serializable id, Class<?> entityType) {
		StarLinkId starLinkId = (StarLinkId) id;
		try {
			return String.format(
					"%s__%s", 
					starLinkId.getStarName(),
					URLEncoder.encode(
							starLinkId.getLink(), 
							StandardCharsets.UTF_8.toString()
					)
			);
		}
		catch (UnsupportedEncodingException e) {
			return null;
		}
	}
	
}
