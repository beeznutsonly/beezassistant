package com.beezassistant.configurator.models;

import java.io.Serializable;
import java.time.ZonedDateTime;

import javax.persistence.Entity;
import javax.persistence.EmbeddedId;
import javax.persistence.Table;

@Entity
@Table(name="scheduledcrosspost")
public class ScheduledCrosspost implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -2838696620487828191L;
	
	@EmbeddedId
	private ScheduledCrosspostId scheduledCrosspostId;
	
	private ZonedDateTime scheduledTime;
	private String title;
	
	public ScheduledCrosspost() {
		super();
		scheduledCrosspostId = new ScheduledCrosspostId();
	}
	
	
	public ScheduledCrosspostId getScheduledCrosspostId() {
		return scheduledCrosspostId;
	}


	public void setScheduledCrosspostId(ScheduledCrosspostId scheduledCrosspostId) {
		this.scheduledCrosspostId = scheduledCrosspostId;
	}
	
	public String getSubreddit() {
		return scheduledCrosspostId.getSubreddit();
	}


	public void setSubreddit(String subreddit) {
		scheduledCrosspostId.setSubreddit(subreddit);
	}
	
	public ZonedDateTime getScheduledTime() {
		return scheduledTime;
	}

	public void setScheduledTime(ZonedDateTime scheduledTime) {
		this.scheduledTime = scheduledTime;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}


	public String getUrl() {
		return scheduledCrosspostId.getUrl();
	}


	public void setUrl(String url) {
		scheduledCrosspostId.setUrl(url);
	}
	
}
