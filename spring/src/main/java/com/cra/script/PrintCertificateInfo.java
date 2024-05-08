package com.cra.script;

import java.security.Security;
import java.util.Iterator;
import java.io.FileInputStream;

import com.entrust.toolkit.security.provider.Entrust;

import iaik.security.provider.IAIK;
import iaik.x509.V3Extension;
import iaik.x509.X509Certificate;

// Usage: java -classpath ../../../../../../libs/enttoolkit.jar --add-exports java.naming/com.sun.jndi.ldap=ALL-UNNAMED PrintCertificateInfo.java <name of certificate file>
public class PrintCertificateInfo {
    public static void main(String[] args) {
        try {
            Security.addProvider(new Entrust());
            Security.addProvider(new IAIK());
            String filename = args[0];
            FileInputStream fis = new FileInputStream(filename);
            X509Certificate cert = new X509Certificate(fis);
            System.out.println("serial number: " + cert.getSerialNumber());
            System.out.println("name: " + cert.getIssuerX500Principal().toString());
            System.out.println("Not before: " + cert.getNotBefore());
            System.out.println("Not after: " + cert.getNotAfter());
            Iterator<?> extensions = cert.listExtensions().asIterator();
            while (extensions.hasNext()) {
                V3Extension extension = (V3Extension) extensions.next();
                System.out.println(extension.toString());
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
