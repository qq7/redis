''' Helper script for redis password '''

import os
import subprocess

from subprocess import PIPE

TITLE = "Check redis password"

def run():
    requirepass = subprocess.Popen(['grep', '^requirepass', '/etc/redis/redis.conf'], stdout= subprocess.PIPE)
    requirepass_out, requirepass_err = requirepass.communicate() 
    try:
        password = requirepass_out.split(' ')[1]    
    except IndexError:
        console.msg(TITLE, "Something is wrong with redis configuration file, please check your redis.conf")        
 
    if password:
        f = open ('/root/redis_password.txt', 'w+')
        f.write(password)
        console.msgbox(TITLE, "Password is saved as /home/root/redispw %s" % requirepass_out)
