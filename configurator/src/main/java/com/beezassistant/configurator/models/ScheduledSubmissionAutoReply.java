package com.beezassistant.configurator.models;

import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.Table;

@Entity
@Table(name="scheduledsubmissionautoreply")
public class ScheduledSubmissionAutoReply {
	
	@EmbeddedId
	ScheduledSubmissionAutoReplyId scheduledSubmissionAutoReplyId;
	
	public ScheduledSubmissionAutoReply() {
		super();
		scheduledSubmissionAutoReplyId = new ScheduledSubmissionAutoReplyId();
	}

	public ScheduledSubmissionAutoReplyId getScheduledSubmissionAutoReplyId() {
		return scheduledSubmissionAutoReplyId;
	}

	public void setScheduledSubmissionAutoReplyId(
			ScheduledSubmissionAutoReplyId scheduledSubmissionAutoReplyId
	) {
		this.scheduledSubmissionAutoReplyId = scheduledSubmissionAutoReplyId;
	}

	public String getUrl() {
		return scheduledSubmissionAutoReplyId.getUrl();
	}

	public void setUrl(String url) {
		scheduledSubmissionAutoReplyId.setUrl(url);
	}

	public String getSubreddit() {
		return scheduledSubmissionAutoReplyId.getSubreddit();
	}

	public void setSubreddit(String subreddit) {
		scheduledSubmissionAutoReplyId.setSubreddit(subreddit);
	}

	public String getCommentBody() {
		return scheduledSubmissionAutoReplyId.getCommentBody();
	}

	public void setCommentBody(String commentBody) {
		scheduledSubmissionAutoReplyId.setCommentBody(commentBody);
	}	
	
}
