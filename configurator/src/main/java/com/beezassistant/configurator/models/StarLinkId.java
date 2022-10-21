package com.beezassistant.configurator.models;

import java.io.Serializable;

import javax.persistence.Embeddable;

@Embeddable
public class StarLinkId implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -6429952764822658339L;

	private String starName;
	private String link;
	
	public StarLinkId() {
		super();
	}

	public StarLinkId(
		String starName,
		String link
	) {
		this();
		this.starName = starName;
		this.link = link;
	}

	public String getStarName() {
		return starName;
	}

	public void setStarName(String starName) {
		this.starName = starName;
	}

	public String getLink() {
		return link;
	}

	public void setLink(String link) {
		this.link = link;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((link == null) ? 0 : link.hashCode());
		result = prime * result + ((starName == null) ? 0 : starName.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		StarLinkId other = (StarLinkId) obj;
		if (link == null) {
			if (other.link != null)
				return false;
		} else if (!link.equals(other.link))
			return false;
		if (starName == null) {
			if (other.starName != null)
				return false;
		} else if (!starName.equals(other.starName))
			return false;
		return true;
	}

}
