package com.cra.script;

import com.entrust.toolkit.User;
import com.entrust.toolkit.credentials.CredentialCreator;
import com.entrust.toolkit.credentials.CredentialReader;
import com.entrust.toolkit.credentials.CredentialWriter;
import com.entrust.toolkit.credentials.FilenameProfileWriter;
import com.entrust.toolkit.util.AuthorizationCode;
import com.entrust.toolkit.util.ManagerTransport;
import com.entrust.toolkit.util.SecureStringBuffer;
import com.entrust.toolkit.x509.directory.JNDIDirectory;

// gets your Entrust credentials and writes them to a file
// Usage: java -classpath ../../../../../../libs/enttoolkit.jar --add-exports java.naming/com.sun.jndi.ldap=ALL-UNNAMED CreateCredential.java <manager IP> <manager port> <directory IP> <directory port> <refnum> <authcode> <epf name> <password>
public class CreateCredential {
    public static void main(String[] args) {
        try {
            String managerIP = args[0];
            int managerPort = Integer.parseInt(args[1]);
            String directoryIP = args[2];
            int directoryPort = Integer.parseInt(args[3]);
            SecureStringBuffer secureRefNum = new SecureStringBuffer(new StringBuffer(args[4]));
            AuthorizationCode secureAuthCode = new AuthorizationCode(new StringBuffer(args[5]));
            String epf = args[6];
            SecureStringBuffer securePassword = new SecureStringBuffer(new StringBuffer(args[7]));

            // Create a user object that has a connection to both the Security 
            // Manager and the Directory
            User user = new User();
            ManagerTransport transport = new ManagerTransport(managerIP, managerPort);
            JNDIDirectory directory = new JNDIDirectory(directoryIP, directoryPort);
            user.setConnections(directory, transport);

            // Set-up the user with a credential-writer that is used to write the 
            // user's Digital Identity to an Entrust file-based Digital Identity 
            // store
            CredentialWriter credentialWriter = new FilenameProfileWriter(epf);
            user.setCredentialWriter(credentialWriter);

            // Log-in the user with credential-reader that is used to create the 
            // user's Digital Identity in software (creates the User)
            CredentialReader credentialReader = new CredentialCreator(secureRefNum, secureAuthCode);
            user.login(credentialReader, securePassword);
            System.out.println("Done! ");
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
