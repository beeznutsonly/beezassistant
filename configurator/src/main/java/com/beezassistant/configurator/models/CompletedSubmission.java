package com.beezassistant.configurator.models;

import java.io.Serializable;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToOne;

@Entity
public class CompletedSubmission implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 6800233518518073631L;
	@Id
	@OneToOne
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
	
}
