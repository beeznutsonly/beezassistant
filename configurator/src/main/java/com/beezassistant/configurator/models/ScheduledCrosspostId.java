package com.beezassistant.configurator.models;

import java.io.Serializable;

public class ScheduledCrosspostId implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -9010912996681070010L;
	private ScheduledSubmission scheduledSubmission;
	private String subreddit;
	
	public ScheduledCrosspostId() {
		super();
	}

	public ScheduledCrosspostId(
			ScheduledSubmission scheduledSubmission, 
			String subreddit
	) {
		super();
		this.scheduledSubmission = scheduledSubmission;
		this.subreddit = subreddit;
	}

	public ScheduledSubmission getScheduledSubmission() {
		return scheduledSubmission;
	}

	public void setScheduledSubmission(ScheduledSubmission scheduledSubmission) {
		this.scheduledSubmission = scheduledSubmission;
	}

	public String getSubreddit() {
		return subreddit;
	}

	public void setSubreddit(String subreddit) {
		this.subreddit = subreddit;
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
		ScheduledCrosspostId other = (ScheduledCrosspostId) obj;
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
