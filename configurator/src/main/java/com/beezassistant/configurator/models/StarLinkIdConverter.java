package com.beezassistant.configurator.models;

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;

import org.springframework.core.convert.converter.Converter;
import org.springframework.stereotype.Component;

@Component
public class StarLinkIdConverter implements Converter<String, StarLinkId> {

	@Override
    public StarLinkId convert(String source) {
        String[] parts = source.split("__");
        StarLinkId starLinkId = new StarLinkId();
        starLinkId.setStarName(parts[0]);
        try {
            starLinkId.setLink(
                    URLDecoder.decode(
                            parts[1],
                            StandardCharsets.UTF_8.toString()
                    )
            );
        } 
        catch (UnsupportedEncodingException e) {
            starLinkId = null;
        }
        return starLinkId;
    }
	
}
