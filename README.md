# Seans Explorer Encryption
This is just a small python script that is meant to be used to encrypt files and folders for me to protect my important documents. The encryption used is the python cryptography Fernet which guarantees that the encrypted files will not be legible without the key to decrypt them.

## Build
To build an executable for this if you do not have a python interpreter on your desired machine, simply go to the base directory of this repository and run the "build.sh" file.
** Note this depends on you having conda installed with an environment called "default" that has pyinstaller and cryptography installed.