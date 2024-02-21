package com.cra.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.config.Customizer;

import com.cra.security.CustomAuthenticationProvider;

@Configuration
@EnableWebSecurity
@ComponentScan("com.cra.security")
public class SecurityConfig {
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity httpSecurity) throws Exception {
        httpSecurity.authorizeHttpRequests((requests) -> requests.anyRequest().authenticated());
        httpSecurity.httpBasic(Customizer.withDefaults());
		return httpSecurity.build();
    }

    @Autowired
    CustomAuthenticationProvider authenticationProvider;

    @Autowired
	public void configure(AuthenticationManagerBuilder builder) {
		builder.authenticationProvider(authenticationProvider);
	}
}
