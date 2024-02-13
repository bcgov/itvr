package com.cra.security;

import com.cra.service.MinioService;

import java.io.InputStream;
import java.util.ArrayList;

import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.core.Authentication;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;

import com.entrust.toolkit.User;
import com.entrust.toolkit.credentials.CredentialReader;
import com.entrust.toolkit.util.SecureStringBuffer;
import com.entrust.toolkit.credentials.StreamProfileReader;

@Component
public class CustomAuthenticationProvider implements AuthenticationProvider {
    @Autowired
    MinioService minioService;

    @Override
    public Authentication authenticate(Authentication authentication) {
        try {
            String epfName = authentication.getName();
            String password = authentication.getCredentials().toString();
            InputStream is = minioService.getObject(epfName);
            CredentialReader credentialReader = new StreamProfileReader(is);
            SecureStringBuffer securePassword = new SecureStringBuffer(new StringBuffer(password));
            User user = new User();
            user.login(credentialReader, securePassword);
            is.close();
            // todo: check user certificates against CRLs
            return new UsernamePasswordAuthenticationToken(user, null, new ArrayList<>());
        } catch (Exception ex) {
            ex.printStackTrace();
            return null;
        }
    }

    @Override
    public boolean supports(Class<?> authentication) {
        return authentication.equals(UsernamePasswordAuthenticationToken.class);
    }
}
