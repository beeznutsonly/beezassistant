package com.beezassistant.configurator.models;

import java.time.ZonedDateTime;

import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.Table;

@Entity
@Table(name="scheduledsubmission")
public class ScheduledSubmission {

	@EmbeddedId
	private ScheduledSubmissionId id;
	
	private String title;
	private ZonedDateTime scheduledTime;
	private String flairId;
	
	
	public ScheduledSubmission() {
		super();
		id = new ScheduledSubmissionId(); //TODO: Clean-up this workaround
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
	
}
