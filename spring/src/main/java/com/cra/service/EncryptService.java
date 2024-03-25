package com.cra.service;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;

import org.apache.commons.io.IOUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.entrust.toolkit.User;
import com.entrust.toolkit.KeyAndCertificateSource;
import com.entrust.toolkit.PKCS7EncodeStream;

import iaik.x509.X509Certificate;

@Service
public class EncryptService {
    @Autowired
    MinioService minioService;

    @Autowired
    CertificateService certificateService;

    public byte[] encrypt(User user, X509Certificate cert, String data) throws Exception {
        KeyAndCertificateSource kcs = new KeyAndCertificateSource();
        kcs.setEncryptionCertificate(cert);
        kcs.setSigningInfo(user.getSigningKey(), user.getVerificationCertificate());
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        PKCS7EncodeStream encoder = new PKCS7EncodeStream(kcs, outputStream, PKCS7EncodeStream.SIGN_AND_ENCRYPT);
        ByteArrayInputStream inputStream = new ByteArrayInputStream(data.getBytes());
        IOUtils.copy(inputStream, encoder);
        // must call close() on the encoder in order for the data to actually be written
        // to the outputstream!
        encoder.close();
        return outputStream.toByteArray();
    }

    public X509Certificate getEncryptionCert(String certName, String crlDN) throws Exception {
        InputStream is = minioService.getObject(certName);
        X509Certificate cert = new X509Certificate(is);
        is.close();
        cert.checkValidity();
        if (crlDN != null) {
            certificateService.checkIfCertIsRevoked(cert, crlDN);
        }
        return cert;
    }

}