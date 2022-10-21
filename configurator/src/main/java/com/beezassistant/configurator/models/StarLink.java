package com.beezassistant.configurator.models;

import java.io.Serializable;

import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.ManyToOne;
import javax.persistence.MapsId;
import javax.persistence.Table;

@Entity
@Table(name="starlink")
public class StarLink implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -4109868076889789803L;

	@EmbeddedId
	private StarLinkId starLinkId;
	
	@ManyToOne
	@MapsId("starName")
	private Star star;

	private String linkName;
	
	public StarLink() {
		super();
		starLinkId = new StarLinkId();
	}
	
	public StarLinkId getStarLinkId() {
		return starLinkId;
	}

	public void setStarLinkId(StarLinkId starLinkId) {
		this.starLinkId = starLinkId;
	}

	

	// public String getStarName() {
	// 	return starLinkId.getStarName();
	// }

	// public void setStarName(String starName) {
	// 	starLinkId.setStarName(starName);
	// }

	public String getLink() {
		return starLinkId.getLink();
	}

	public void setLink(String link) {
		starLinkId.setLink(link);
	}

	public String getLinkName() {
		return linkName;
	}
	
	public void setLinkName(String linkName) {
		this.linkName = linkName;
	}
	
}
