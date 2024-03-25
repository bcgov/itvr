package com.cra.script;

import java.util.Iterator;

import com.entrust.toolkit.User;
import com.entrust.toolkit.credentials.CredentialReader;
import com.entrust.toolkit.credentials.FilenameProfileReader;
import com.entrust.toolkit.util.SecureStringBuffer;

import iaik.x509.X509Certificate;
import iaik.x509.V3Extension;

// Usage: java -classpath ../../../../../../libs/enttoolkit.jar --add-exports java.naming/com.sun.jndi.ldap=ALL-UNNAMED PrintEPFInfo.java <name of epf file> <password>
public class PrintEPFInfo {
    public static void main(String[] args) {
        try {
            String filename = args[0];
            String password = args[1];
            User user = new User();
            SecureStringBuffer securePassword = new SecureStringBuffer(new StringBuffer(password));
            CredentialReader credentialReader = new FilenameProfileReader(filename);
            user.login(credentialReader, securePassword);

            X509Certificate[] certs = user.getUserCertificates();
            for (int i = 0; i < certs.length; i++) {
                X509Certificate cert = certs[i];
                System.out.println("cert " + i);
                System.out.println("serial number: " + cert.getSerialNumber());
                System.out.println("name: " + cert.getIssuerX500Principal().toString());
                System.out.println("Not before: " + cert.getNotBefore());
                System.out.println("Not after: " + cert.getNotAfter());
                Iterator<?> extensions = cert.listExtensions().asIterator();
                while (extensions.hasNext()) {
                    V3Extension extension = (V3Extension) extensions.next();
                    System.out.println(extension.toString());
                }
                System.out.println(" ");
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
