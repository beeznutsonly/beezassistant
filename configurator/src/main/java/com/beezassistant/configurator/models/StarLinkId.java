package com.beezassistant.configurator.models;

import java.io.Serializable;

public class StarLinkId implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -6429952764822658339L;
	private Star star;
	private String link;
	
	public StarLinkId(Star star, String link) {
		super();
		this.star = star;
		this.link = link;
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

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((link == null) ? 0 : link.hashCode());
		result = prime * result + ((star == null) ? 0 : star.hashCode());
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
		if (star == null) {
			if (other.star != null)
				return false;
		} else if (!star.equals(other.star))
			return false;
		return true;
	}

}
