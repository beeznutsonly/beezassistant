package com.beezassistant.configurator.models;

import java.io.Serializable;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinColumns;
import javax.persistence.OneToOne;
import javax.persistence.Table;

@Entity
@Table(name="completedsubmission")
public class CompletedSubmission implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 6800233518518073631L;

	@Id
	@OneToOne
	@JoinColumns({
		@JoinColumn(name="url", referencedColumnName="url"),
		@JoinColumn(name="subreddit", referencedColumnName="subreddit")
	})
	private ScheduledSubmission scheduledSubmission;
	
	public CompletedSubmission() {
		super();
	}

	public CompletedSubmission(ScheduledSubmission scheduledSubmission) {
		super();
		this.scheduledSubmission = scheduledSubmission;
	}

	public ScheduledSubmission getScheduledSubmission() {
		return scheduledSubmission;
	}

	public void setScheduledSubmission(ScheduledSubmission scheduledSubmission) {
		this.scheduledSubmission = scheduledSubmission;
	}

	public String getUrl() {
		return scheduledSubmission.getUrl();
	}

	public String getSubreddit() {
		return scheduledSubmission.getSubreddit();
	}
	
}
