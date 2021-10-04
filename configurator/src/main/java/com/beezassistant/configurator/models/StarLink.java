package com.beezassistant.configurator.models;

import java.io.Serializable;

import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
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

	public String getName() {
		return starLinkId.getName();
	}

	public void setName(String name) {
		starLinkId.setName(name);
	}

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
