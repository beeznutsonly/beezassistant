package com.beezassistant.configurator.models;

import java.io.Serializable;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

import org.springframework.data.rest.webmvc.spi.BackendIdConverter;
import org.springframework.stereotype.Component;

@Component
public class ScheduledSubmissionAutoReplyIdConverter implements BackendIdConverter {

	@Override
	public boolean supports(Class<?> delimiter) {
		return ScheduledSubmissionAutoReply.class.equals(delimiter);
	}

	@Override
	public Serializable fromRequestId(String id, Class<?> entityType) {
		String[] parts = id.split("__");
		ScheduledSubmissionAutoReplyId scheduledSubmissionAutoReplyId 
			= new ScheduledSubmissionAutoReplyId();
		scheduledSubmissionAutoReplyId.setSubreddit(parts[0]);
		try {
			scheduledSubmissionAutoReplyId.setUrl(
					URLDecoder.decode(
							parts[1],
							StandardCharsets.UTF_8.toString()
					)
			);
			scheduledSubmissionAutoReplyId.setCommentBody(
					URLDecoder.decode(
							parts[2],
							StandardCharsets.UTF_8.toString()
					)
			);
		} 
		catch (UnsupportedEncodingException e) {
			scheduledSubmissionAutoReplyId = null;
		}
		return scheduledSubmissionAutoReplyId;
	}

	@Override
	public String toRequestId(Serializable id, Class<?> entityType) {
		ScheduledSubmissionAutoReplyId scheduledSubmissionAutoReplyId = (ScheduledSubmissionAutoReplyId) id;
		try {
			return String.format(
					"%s__%s__%s", 
					scheduledSubmissionAutoReplyId.getSubreddit(),
					URLEncoder.encode(
							scheduledSubmissionAutoReplyId.getUrl(), 
							StandardCharsets.UTF_8.toString()
					),
					URLEncoder.encode(
							scheduledSubmissionAutoReplyId.getCommentBody(), 
							StandardCharsets.UTF_8.toString()
					)
			);
		}
		catch (UnsupportedEncodingException e) {
			return null;
		}
	}

}
