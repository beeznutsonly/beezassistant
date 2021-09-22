package com.beezassistant.configurator.models;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.IdClass;

@Entity
@IdClass(AutoCommenterId.class)
public class AutoCommenter {
	
	@Id
	private String url;
	
	@Id
	private String commentBody;
	
	private boolean oneoff;

	public AutoCommenter() {
		super();
	}

	public AutoCommenter(String url, String commentBody) {
		super();
		this.url = url;
		this.commentBody = commentBody;
	}

	public AutoCommenter(
			String url, 
			String commentBody, 
			boolean oneoff
	) {
		super();
		this.url = url;
		this.commentBody = commentBody;
		this.oneoff = oneoff;
	}

	public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
	}

	public String getCommentBody() {
		return commentBody;
	}

	public void setCommentBody(String commentBody) {
		this.commentBody = commentBody;
	}

	public boolean isOneoff() {
		return oneoff;
	}

	public void setOneoff(boolean oneoff) {
		this.oneoff = oneoff;
	}
	
	
}
