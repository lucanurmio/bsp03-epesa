# bsp03-epesa
Epesa is a shorthand for Encrypted Python Email Sending App, and refers to the BSP3 of Luca Nurmio.
# Overview
Each of the python files represents a different email client, however all 4 of them are based on "app.py". Each is only designed to receive emails sent out by an instance of itself.
## How to send emails
The host file of the OS must contain the following entries:

```
127.0.0.1  lmail.test
127.0.0.1  smtp.lmail.test
127.0.0.1  pop3.lmail.test
```

An mail server must be running locally, with port 25 for SMTP and 110 for POP3. The mail server must contain the domain ´lmail.test´ as well as email users (addresses) with that domain. These email users will be able to send emails to each other.
### For "appGNUPG.py"
GNU Privacy Guard (GNUPG) must be installed and at least 1 PGP profile must be created with it.

For sending emails, the public key fingerprint of the profile must be entered in the email client. For retrieving emails, GNUPG will directly ask the user for the passphrase.
### For "appPGPy.py"
There must be at least 2 .asc files located in the same directory as the email client. One of the files must be a public key and the other one must be its private key.

For sending emails, the public key filename must be entered in the email client. For retrieving emails, the private key filename as well as the passphrase must be entered.

The files "jerrys\_public\_key.asc" (public key) and "jerrys\_secret\_key.asc" (private key) have been provided as examples. The passphrase is "jerryjeremy".
### For "appSmail.py"
There must be at least 2 .pem files located in the same directory as the email client. One of the files must be a certificate and the other one must be its keypair.

For sending emails, the certificate filename must be entered in the email client. For retrieving emails, the certificate filename as well as the keypair filename must be entered.

The file "jerry.pem" (certificate) and "jerry\_key.pem" (keypair) have been provided as examples.
## Remarks
The mail server used for testing was an "Apache James" mail server. The OS this was tested on is Ubuntu, which has GNUPG pre-installed by default.
