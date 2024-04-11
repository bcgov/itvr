package com.cra;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import java.security.Security;
import com.entrust.toolkit.security.provider.Entrust;
import iaik.security.provider.IAIK;

@SpringBootApplication
public class CRAApplication {
  public static void main(String[] args) {
    Security.addProvider(new Entrust());
    Security.addProvider(new IAIK());
    SpringApplication.run(CRAApplication.class, args);
  }
}