package com.beezassistant.configurator.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class ScheduleSubmissionController {
	
	@RequestMapping("/schedulesubmission")
	public ModelAndView returnPage(){
		return new ModelAndView(
			"webpages/schedule-submission/index.html"
		);
	}
	
}
