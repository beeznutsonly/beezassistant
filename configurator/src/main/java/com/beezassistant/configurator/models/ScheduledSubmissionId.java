package com.beezassistant.configurator.models;

import java.io.Serializable;

import javax.persistence.Embeddable;

@Embeddable
public class ScheduledSubmissionId implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 8622313889261372832L;
	private String url;
	private String subreddit;
	
	public ScheduledSubmissionId() {
		super();
	}

	public ScheduledSubmissionId(String url, String subreddit) {
		super();
		this.url = url;
		this.subreddit = subreddit;
	}

	public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
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
		result = prime * result + ((subreddit == null) ? 0 : subreddit.hashCode());
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
		ScheduledSubmissionId other = (ScheduledSubmissionId) obj;
		if (subreddit == null) {
			if (other.subreddit != null)
				return false;
		} else if (!subreddit.equals(other.subreddit))
			return false;
		if (url == null) {
			if (other.url != null)
				return false;
		} else if (!url.equals(other.url))
			return false;
		return true;
	}	
	
}