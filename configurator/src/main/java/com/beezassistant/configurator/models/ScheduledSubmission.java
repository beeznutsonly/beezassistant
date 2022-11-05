package com.beezassistant.configurator.models;

import java.time.ZonedDateTime;

import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.OneToOne;
import javax.persistence.Table;

@Entity
@Table(name="scheduledsubmission")
public class ScheduledSubmission {

	@EmbeddedId
	private ScheduledSubmissionId id;
	
	private String title;
	private ZonedDateTime scheduledTime;
	private String flairId;
	private String commentBody;

	@OneToOne(mappedBy="scheduledSubmission")
	private CompletedSubmission completed;
	


	public ScheduledSubmission() {
		super();
		// This needs to be fixed in the future
		id = new ScheduledSubmissionId();
	}
	
	
	public ScheduledSubmissionId getId() {
		return id;
	}


	public void setId(ScheduledSubmissionId id) {
		this.id = id;
	}
	
	

	public String getUrl() {
		return id.getUrl();
	}



	public void setUrl(String url) {
		id.setUrl(url);
	}



	public String getSubreddit() {
		return id.getSubreddit();
	}



	public void setSubreddit(String subreddit) {
		id.setSubreddit(subreddit);
	}



	public String getTitle() {
		return title;
	}


	public void setTitle(String title) {
		this.title = title;
	}


	public ZonedDateTime getScheduledTime() {
		return scheduledTime;
	}


	public void setScheduledTime(ZonedDateTime scheduledTime) {
		this.scheduledTime = scheduledTime;
	}


	public String getFlairId() {
		return flairId;
	}


	public void setFlairId(String flairId) {
		this.flairId = flairId;
	}
	
	public String getCommentBody() {
		return commentBody;
	}

	public void setCommentBody(String commentBody) {
		this.commentBody = commentBody;
	}

	public CompletedSubmission getCompleted() {
		return completed;
	}

	public void setCompleted(CompletedSubmission completed) {
		this.completed = completed;
	}
}
