package com.cra.script;

import java.security.Security;
import java.io.FileOutputStream;

import com.entrust.toolkit.security.provider.Entrust;
import iaik.security.provider.IAIK;
import com.entrust.toolkit.x509.directory.JNDIDirectory;
import iaik.x509.X509Certificate;

// gets a certificate from a directory and writes it to a file
// Usage: java -classpath ../../../../../../libs/enttoolkit.jar --add-exports java.naming/com.sun.jndi.ldap=ALL-UNNAMED GetCertificate.java <directory IP> <directory port> <ldapDN> <ldapAttribute> <filename>
public class GetCertificate {
    public static void main(String[] args) {
        try {
            Security.addProvider(new Entrust());
            Security.addProvider(new IAIK());
            String directoryIP = args[0];
            int directoryPort = Integer.parseInt(args[1]);
            String ldapDN = args[2];
            String ldapAttribute = args[3];
            String filename = args[4];

            JNDIDirectory directory = new JNDIDirectory(directoryIP, directoryPort);
            directory.connect();
            byte[][] certs = directory.getAttr(ldapDN, ldapAttribute);
            byte[] cert = certs[0];
            X509Certificate x509Cert = new X509Certificate(cert);

            FileOutputStream fos = new FileOutputStream(filename);
            x509Cert.writeTo(fos);
            directory.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
