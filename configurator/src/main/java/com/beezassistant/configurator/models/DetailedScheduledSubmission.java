package com.beezassistant.configurator.models;

import java.time.ZonedDateTime;

import org.springframework.data.rest.core.config.Projection;

@Projection(
    name="detailed",
    types={ScheduledSubmission.class}
)
public interface DetailedScheduledSubmission {

	public String getTitle();
    
    public String getUrl();

	public ZonedDateTime getScheduledTime();

	public String getFlairId();

	public String getSubreddit();
    
	public String getCommentBody();

    public CompletedSubmission getCompleted();

}