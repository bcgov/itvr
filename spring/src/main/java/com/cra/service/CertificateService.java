package com.cra.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.entrust.toolkit.x509.directory.JNDIDirectory;

import iaik.x509.X509CRL;
import iaik.x509.X509Certificate;

@Service
public class CertificateService {
    @Value("${DIRECTORY_IP}")
    private String directoryIP;

    @Value("${DIRECTORY_PORT}")
    private int directoryPort;

    public void checkIfCertIsRevoked(X509Certificate cert, String crlDN) throws Exception {
        JNDIDirectory directory = new JNDIDirectory(directoryIP, directoryPort);
        directory.connect();
        X509CRL[] crls = directory.getCRLs(crlDN, false);
        for (int i = 0; i < crls.length; i++) {
            X509CRL crl = crls[i];
            if (crl.isRevoked(cert)) {
                throw new Exception("certificate has been revoked!");
            }
        }
    }
}
