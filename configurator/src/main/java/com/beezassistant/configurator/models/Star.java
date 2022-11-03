package com.beezassistant.configurator.models;

import java.time.LocalDate;
import java.util.List;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToMany;

import com.fasterxml.jackson.annotation.JsonManagedReference;

@Entity
public class Star {
	
	@Id
	private String name;
	
	private LocalDate birthday;
	private String nationality;
	private String birthPlace;
	private String yearsActive;
	private String description;

	@OneToMany(mappedBy="star", cascade = CascadeType.ALL)
	@JsonManagedReference
	private List<StarLink> starLinks;

	public Star() {
		super();
	}

	public Star(String name) {
		super();
		this.name = name;
	}

	public Star(
			String name, 
			LocalDate birthday, 
			String nationality, 
			String birthPlace, 
			String yearsActive,
			String description
	) {
		super();
		this.name = name;
		this.birthday = birthday;
		this.nationality = nationality;
		this.birthPlace = birthPlace;
		this.yearsActive = yearsActive;
		this.description = description;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public LocalDate getBirthday() {
		return birthday;
	}

	public void setBirthday(LocalDate birthday) {
		this.birthday = birthday;
	}

	public String getNationality() {
		return nationality;
	}

	public void setNationality(String nationality) {
		this.nationality = nationality;
	}

	public String getBirthPlace() {
		return birthPlace;
	}

	public void setBirthPlace(String birthPlace) {
		this.birthPlace = birthPlace;
	}

	public String getYearsActive() {
		return yearsActive;
	}

	public void setYearsActive(String yearsActive) {
		this.yearsActive = yearsActive;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public List<StarLink> getStarLinks() {
		return starLinks;
	}

	public void setStarLinks(List<StarLink> starLinks) {
		this.starLinks = starLinks;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((name == null) ? 0 : name.hashCode());
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
		Star other = (Star) obj;
		if (name == null) {
			if (other.name != null)
				return false;
		} else if (!name.equals(other.name))
			return false;
		return true;
	}
		
}
