#!/usr/bin/env python3.4
#python3-rsa
import os, rsa

key_file = str(os.getenv("HOME"))+"/.ssh/id_rsa"
pub_key_file = str(os.getenv("HOME"))+"/.ssh/id_rsa.pub"

if os.path.isfile(key_file) and os.path.isfile(pub_key_file):
#    with open(key_file, 'rb') as priv_file:
#        key_data = priv_file.read()
#        print(key_data)
    key = rsa.PrivateKey.load_pkcs1(key_file, format='PEM')
#    key = rsa.PrivateKey.load_pkcs1(key_file, format='DER')
    print(key)
#        with open(pub_key_file, 'rb') as pub_file:
#        pub_key_data = pub_file.read()
#    pub_key = rsa.PublicKey.load_pkcs1(pub_key_data)
else:
    subprocess.Popen(["notify-send", "FreeRDP message:", "SSH keys not found. Run the following command in the terminal: ssh-keygen -t rsa"], stdout=subprocess.PIPE)
    exit()
