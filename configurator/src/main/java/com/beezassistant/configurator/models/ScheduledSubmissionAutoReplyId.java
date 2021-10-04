package com.beezassistant.configurator.models;

import java.io.Serializable;

import javax.persistence.Embeddable;

@Embeddable
public class ScheduledSubmissionAutoReplyId implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -2610425133675625398L;
	private String url;
	private String subreddit;
	private String commentBody;
	
	public ScheduledSubmissionAutoReplyId() {
		super();
	}

	public ScheduledSubmissionAutoReplyId(
			String url,
			String subreddit,
			String commentBody
	) {
		super();
		this.url = url;
		this.subreddit = subreddit;
		this.commentBody = commentBody;
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

	public String getCommentBody() {
		return commentBody;
	}

	public void setCommentBody(String commentBody) {
		this.commentBody = commentBody;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((commentBody == null) ? 0 : commentBody.hashCode());
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
		ScheduledSubmissionAutoReplyId other = (ScheduledSubmissionAutoReplyId) obj;
		if (commentBody == null) {
			if (other.commentBody != null)
				return false;
		} else if (!commentBody.equals(other.commentBody))
			return false;
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
