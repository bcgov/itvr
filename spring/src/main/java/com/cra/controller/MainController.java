package com.cra.controller;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.context.SecurityContextHolder;

import com.entrust.toolkit.User;
import iaik.x509.X509Certificate;

import com.cra.service.EncryptService;
import com.cra.service.DecryptService;

@RestController
public class MainController {
    @Autowired
    EncryptService encryptService;

    @Autowired
    DecryptService decryptService;

    @GetMapping("/encrypt")
    public ResponseEntity<byte[]> encrypt(@RequestBody Map<String, String> data) {
        try {
            User user = (User) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
            X509Certificate cert = encryptService.getEncryptionCert(data.get("certificate"), data.get("crlDN"));
            byte[] encryptedData = encryptService.encrypt(user, cert, data.get("toEncrypt"));
            return new ResponseEntity<byte[]>(encryptedData, HttpStatus.OK);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return new ResponseEntity<byte[]>(HttpStatus.INTERNAL_SERVER_ERROR);
    }

    @GetMapping("/decrypt")
    public ResponseEntity<String> decrypt(@RequestBody byte[] data) {
        try {
            User user = (User) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
            String decryptedData = decryptService.decrypt(user, data);
            return new ResponseEntity<String>(decryptedData, HttpStatus.OK);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return new ResponseEntity<String>(HttpStatus.INTERNAL_SERVER_ERROR);
    }
}