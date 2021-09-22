package com.beezassistant.configurator.models;

import java.io.Serializable;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToOne;

@Entity
public class CompletedCrosspost implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -4914953242998002559L;
	@Id
	@OneToOne
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
	
}
