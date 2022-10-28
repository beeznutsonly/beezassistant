package com.beezassistant.configurator.models;

import java.io.Serializable;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinColumns;
import javax.persistence.OneToOne;
import javax.persistence.Table;

@Entity
@Table(name="completedcrosspost")
public class CompletedCrosspost implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -4914953242998002559L;

	@Id
	@OneToOne
	@JoinColumns({
		@JoinColumn(name = "url", referencedColumnName = "url"),
		@JoinColumn(name = "subreddit", referencedColumnName = "subreddit")
	})
	private ScheduledCrosspost scheduledCrosspost;

	public CompletedCrosspost() {
		super();
	}

	public CompletedCrosspost(ScheduledCrosspost scheduledCrosspost) {
		super();
		this.scheduledCrosspost = scheduledCrosspost;
	}

	public ScheduledCrosspost getScheduledCrosspost() {
		return scheduledCrosspost;
	}

	public void setScheduledCrosspost(ScheduledCrosspost scheduledCrosspost) {
		this.scheduledCrosspost = scheduledCrosspost;
	}
	
	public String getUrl() {
		return scheduledCrosspost.getUrl();
	}

	public String getSubreddit() {
		return scheduledCrosspost.getSubreddit();
	}
}
