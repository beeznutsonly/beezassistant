package com.beezassistant.configurator.models;

import java.time.Instant;

import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class ScheduledSubmission {

	@Id
	private String url;
	
	private String title;
	private String flairID;
	private Instant scheduledTime;
	
	public ScheduledSubmission() {
		super();
	}

	public ScheduledSubmission(
			String url, 
			String title, 
			Instant scheduledTime
	) {
		super();
		this.url = url;
		this.title = title;
		this.scheduledTime = scheduledTime;
	}

	public ScheduledSubmission(
			String url, 
			String title, 
			Instant scheduledTime, 
			String flairID
	) {
		super();
		this.url = url;
		this.title = title;
		this.flairID = flairID;
		this.scheduledTime = scheduledTime;
	}

	public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getFlairID() {
		return flairID;
	}

	public void setFlairID(String flairID) {
		this.flairID = flairID;
	}

	public Instant getScheduledTime() {
		return scheduledTime;
	}

	public void setScheduledTime(Instant scheduledTime) {
		this.scheduledTime = scheduledTime;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((url == null) ? 0 : url.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		ScheduledSubmission other = (ScheduledSubmission) obj;
		if (url == null) {
			if (other.url != null)
				return false;
		} else if (!url.equals(other.url))
			return false;
		return true;
	}
	
}
