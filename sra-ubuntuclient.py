#!/usr/bin/env python

import os
import subprocess
import apt
import sys,socket

def install():
    print "Running apt update"
    cache=apt.Cache()
    cache.update()
    cache.open(None);
    pkg1 = cache['openssh-server']
    pkg2 = cache['curl']
    pkg1.mark_install()
    pkg2.mark_install()
    cache.commit()

def ss_dwnld():
    print "Downloading Salt..."
    p = subprocess.Popen (["curl", "-L","https://bootstrap.saltstack.com","-o", "install_salt.sh", "--insecure"])
    if p.wait():
        sys.exit("Cannot download salt installation file!")
    p.communicate()

def ss_install():
    print "Installing Salt"
    p = subprocess.Popen(["sh", "install_salt.sh", "-P"])
    p.communicate()

def mod_crontab():
    with open("/etc/crontab", "a") as f:
     f.write("00 12 * * * salt-call state.highstate\n")
     f.close()

def mod_minion():
    os.chdir("/etc/salt")
    with open("minion", 'r') as file:
        data= file.readlines()
    data[16] = "master: srapulin01prsc.sisa.samsung.com\n"
    data[78] = "id: " + socket.gethostname() + "\n"
    data[466] = "hash_type: sha256 \n\n"
    with open("minion", 'w') as file:
        file.writelines(data)
    file.close()

def salt_call():
    p = subprocess.Popen(["salt-call", "state.apply", "sra-ubuntu15"])
    p.communicate()

def main():
    print "This script is designed to run on newly-imaged clients running Ubuntu 15.  "
#    install()
#    ss_dwnld()
#    ss_install()
#    mod_crontab()
    mod_minion()
    salt_call()
    print "The script is complete."

if __name__ == "__main__":
    main()

