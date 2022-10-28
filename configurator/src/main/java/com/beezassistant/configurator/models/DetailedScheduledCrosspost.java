package com.beezassistant.configurator.models;

import java.time.ZonedDateTime;

import org.springframework.data.rest.core.config.Projection;

@Projection(
    name="detailed",
    types={ScheduledCrosspost.class}
)
public interface DetailedScheduledCrosspost {
    
    public String getTitle();
    
    public String getUrl();

	public ZonedDateTime getScheduledTime();

	public String getSubreddit();

    public CompletedCrosspost getCompleted();

}
