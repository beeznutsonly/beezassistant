package com.beezassistant.configurator.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class AddAdminUpdateController {
	
	@RequestMapping("addadminupdate")
	public ModelAndView returnPage() {
		return new ModelAndView("webpages/addadminupdate/index.html");
	}
	
}
