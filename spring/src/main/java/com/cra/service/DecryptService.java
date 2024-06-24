package com.cra.service;

import java.io.ByteArrayInputStream;
import java.io.InputStream;

import javax.mail.Part;
import javax.mail.internet.MimeBodyPart;

import org.springframework.stereotype.Service;

import com.entrust.toolkit.User;
import iaik.smime.SMimeEncrypted;
import iaik.smime.SMimeSigned;
import iaik.smime.SMimeCompressed;

@Service
public class DecryptService {

    public String decrypt(User user, byte[] data) throws Exception {
        Part p;
        InputStream contentStream;

        contentStream = new ByteArrayInputStream(data);
        SMimeEncrypted encrypted = new SMimeEncrypted(contentStream);
        encrypted.decryptSymmetricKey(user);
        p = new MimeBodyPart(encrypted.getInputStream());
        contentStream = (InputStream) p.getContent();

        SMimeSigned signed = new SMimeSigned(contentStream);
        p = new MimeBodyPart(signed.getInputStream());
        contentStream = (InputStream) p.getContent();

        SMimeCompressed compressed = new SMimeCompressed(contentStream);
        p = new MimeBodyPart(compressed.getInputStream());
        String result = (String) p.getContent();

        return result;
    }
}