package com.cra.script;

import com.entrust.toolkit.User;
import com.entrust.toolkit.credentials.CredentialReader;
import com.entrust.toolkit.credentials.CredentialWriter;
import com.entrust.toolkit.credentials.FilenameProfileReader;
import com.entrust.toolkit.credentials.FilenameProfileWriter;
import com.entrust.toolkit.util.ManagerTransport;
import com.entrust.toolkit.util.SecureStringBuffer;
import com.entrust.toolkit.x509.directory.JNDIDirectory;

// Usage: java -classpath ../../../../../../libs/enttoolkit.jar --add-exports java.naming/com.sun.jndi.ldap=ALL-UNNAMED UpdateEPFKeys.java <manager IP> <manager port> <directory IP> <directory port> <name of epf file> <password> <name of new epf file>
public class UpdateEPFKeys {
    public static void main(String[] args) {
        try {
            String managerIP = args[0];
            int managerPort = Integer.parseInt(args[1]);
            String directoryIP = args[2];
            int directoryPort = Integer.parseInt(args[3]);
            String filename = args[4];
            String password = args[5];
            String newFilename = args[6];

            User user = new User();
            JNDIDirectory directory = new JNDIDirectory(directoryIP, directoryPort);
            ManagerTransport transport = new ManagerTransport(managerIP, managerPort);
            user.setConnections(directory, transport);
            SecureStringBuffer securePassword = new SecureStringBuffer(new StringBuffer(password));
            CredentialReader credentialReader = new FilenameProfileReader(filename);
            CredentialWriter credentialWriter = new FilenameProfileWriter(newFilename);
            user.setCredentialWriter(credentialWriter);
            user.login(credentialReader, securePassword);
            user.updateAllKeys();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
