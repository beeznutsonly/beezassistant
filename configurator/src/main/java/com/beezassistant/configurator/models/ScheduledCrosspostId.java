package com.beezassistant.configurator.models;

import java.io.Serializable;

import javax.persistence.Embeddable;

@Embeddable
public class ScheduledCrosspostId implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -9010912996681070010L;
	private String url;
	private String subreddit;
	
	public ScheduledCrosspostId() {
		super();
	}

	public ScheduledCrosspostId(
			String url, 
			String subreddit
	) {
		this();
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
		result = prime * result + ((url == null) ? 0 : url.hashCode());
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
		if (url == null) {
			if (other.url != null)
				return false;
		} else if (!url.equals(other.url))
			return false;
		if (subreddit == null) {
			if (other.subreddit != null)
				return false;
		} else if (!subreddit.equals(other.subreddit))
			return false;
		return true;
	}
	
	
	
}
