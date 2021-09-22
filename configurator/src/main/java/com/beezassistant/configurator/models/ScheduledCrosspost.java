package com.beezassistant.configurator.models;

import java.io.Serializable;
import java.time.Instant;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.IdClass;
import javax.persistence.ManyToOne;

@Entity
@IdClass(ScheduledCrosspostId.class)
public class ScheduledCrosspost implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -2838696620487828191L;

	@Id
	@ManyToOne
	private ScheduledSubmission scheduledSubmission;
	
	@Id
	private String subreddit;
	
	private Instant scheduledTime;
	
	public ScheduledCrosspost() {
		super();
	}

	public ScheduledCrosspost(
			ScheduledSubmission scheduledSubmission, 
			String subreddit, 
			Instant scheduledTime
	) {
		super();
		this.scheduledSubmission = scheduledSubmission;
		this.subreddit = subreddit;
		this.scheduledTime = scheduledTime;
	}

	public ScheduledSubmission getscheduledSubmission() {
		return scheduledSubmission;
	}

	public void setscheduledSubmission(ScheduledSubmission scheduledSubmission) {
		this.scheduledSubmission = scheduledSubmission;
	}

	public String getSubreddit() {
		return subreddit;
	}

	public void setSubreddit(String subreddit) {
		this.subreddit = subreddit;
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
		result = prime * result + ((scheduledSubmission == null) ? 0 : scheduledSubmission.hashCode());
		result = prime * result + ((subreddit == null) ? 0 : subreddit.hashCode());
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
		ScheduledCrosspost other = (ScheduledCrosspost) obj;
		if (scheduledSubmission == null) {
			if (other.scheduledSubmission != null)
				return false;
		} else if (!scheduledSubmission.equals(other.scheduledSubmission))
			return false;
		if (subreddit == null) {
			if (other.subreddit != null)
				return false;
		} else if (!subreddit.equals(other.subreddit))
			return false;
		return true;
	}
	
}
