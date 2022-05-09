# ITVR Services

## CRA Encryption

Install the Entrust software by double clicking the setup.exe file supplied by the CRA. There are no requirements, other the available disk space, for this step.

The software needs to be configured with a valid user profile. I found the best approach for this is search for `Entrust` within the windows universal search. You will see an option for creating an Entrust Profile. Enter the key and secret that CRA provided in the form. You will be prompted to create a password. The software requires you to authenticate every now and then. However, the password has nothing to do with encrypting and decrypting a file.

### To encrypt a file

- Right click it in the file explorer.
- Choose the encrypting option.
- Enter password if necessary.
- Follow the promps, However make sure you check the box for encrypting for a specific person.
- In the search form enter the following user: `CRA ARC FTP`.
- Click through all the submits

## To decrypt a file

If this step fails it is most likely due to the file not being encrypted for the user trying to decrypt it.

- Right click it in the file explorer.
- Choose the decrypt option.
- Enter password if necessary.

### Automation

The Entrust executables for encrypting and decrypting can be found here:

> C:\Program Files (x86)\Common Files\Entrust\ESP

- eeencrypt.exe
- deencrypt.exe

## CRA Wage Requests
