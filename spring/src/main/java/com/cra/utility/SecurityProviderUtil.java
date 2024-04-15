package com.cra.utility;

import java.security.Security;
import com.entrust.toolkit.security.provider.Entrust;
import iaik.security.provider.IAIK;

public class SecurityProviderUtil {

    public static void addCustomSecurityProviders() {
        Security.insertProviderAt(new Entrust(), 1);
        Security.insertProviderAt(new IAIK(), 2);
    }

    public static void removeCustomSecurityProviders() {
        Security.removeProvider("Entrust");
        Security.removeProvider("IAIK");
    }

}
