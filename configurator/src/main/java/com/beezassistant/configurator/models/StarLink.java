package com.beezassistant.configurator.models;

import java.io.Serializable;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.IdClass;
import javax.persistence.ManyToOne;

@Entity
@IdClass(StarLinkId.class)
public class StarLink implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -4109868076889789803L;

	@Id
	@ManyToOne
	private Star star;
	
	@Id
	private String link;
	
	private String linkName;
	
	public StarLink() {
		super();
	}
	
	public StarLink(Star name) {
		this();
		this.star = name;
	}

	public StarLink(Star star, String link) {
		this(star);
		this.link = link;
	}

	public StarLink(Star star, String link, String linkName) {
		this(star, link);
		this.linkName = linkName;
	}

	public Star getStar() {
		return star;
	}

	public void setStar(Star star) {
		this.star = star;
	}

	public String getLink() {
		return link;
	}

	public void setLink(String link) {
		this.link = link;
	}

	public String getLinkName() {
		return linkName;
	}

	public void setLinkName(String linkName) {
		this.linkName = linkName;
	}
	
}
