package com.beezassistant.configurator.models;

import java.io.Serializable;

public class AutoCommenterId implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -2610425133675625398L;
	private String url;
	private String commentBody;
	
	public AutoCommenterId(String url, String commentBody) {
		super();
		this.url = url;
		this.commentBody = commentBody;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((commentBody == null) ? 0 : commentBody.hashCode());
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
		AutoCommenterId other = (AutoCommenterId) obj;
		if (commentBody == null) {
			if (other.commentBody != null)
				return false;
		} else if (!commentBody.equals(other.commentBody))
			return false;
		if (url == null) {
			if (other.url != null)
				return false;
		} else if (!url.equals(other.url))
			return false;
		return true;
	}
	
}
