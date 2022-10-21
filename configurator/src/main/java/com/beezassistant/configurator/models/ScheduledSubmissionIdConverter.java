package com.beezassistant.configurator.models;

import java.io.Serializable;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

import org.springframework.data.rest.webmvc.spi.BackendIdConverter;
import org.springframework.stereotype.Component;

@Component
public class ScheduledSubmissionIdConverter implements BackendIdConverter {

	@Override
	public boolean supports(Class<?> delimiter) {
		return ScheduledSubmission.class.equals(delimiter);
	}

	@Override
	public Serializable fromRequestId(String id, Class<?> entityType) {
		String[] parts = id.split("__");
		ScheduledSubmissionId scheduledSubmissionId = new ScheduledSubmissionId();
		scheduledSubmissionId.setSubreddit(parts[0]);
		try {
			scheduledSubmissionId.setUrl(
					URLDecoder.decode(
							parts[1],
							StandardCharsets.UTF_8.toString()
					)
			);
		} 
		catch (UnsupportedEncodingException e) {
			scheduledSubmissionId = null;
		}
		return scheduledSubmissionId;
	}

	@Override
	public String toRequestId(Serializable id, Class<?> entityType) {
		ScheduledSubmissionId scheduledSubmissionId = (ScheduledSubmissionId) id;
		try {
			return String.format(
					"%s__%s", 
					scheduledSubmissionId.getSubreddit(),
					URLEncoder.encode(
							scheduledSubmissionId.getUrl(), 
							StandardCharsets.UTF_8.toString()
					)
			);
		}
		catch (UnsupportedEncodingException e) {
			return null;
		}
	}

}
