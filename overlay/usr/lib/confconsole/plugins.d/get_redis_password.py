''' Helper script for redis password '''

import os
import subprocess

from subprocess import PIPE

TITLE = "Check redis password"

def run():
    requirepass = subprocess.Popen(['turnkey-redis-pw', 'get'], stdout= subprocess.PIPE)
    requirepass_out, requirepass_err = requirepass.communicate() 
    if not requirepass_out:
        console.msgbox(TITLE, "Something is wrong with redis configuration file, please check your redis.conf")        
    else:
        f = open ('/root/redis_password.txt', 'w+')
        f.write(requirepass_out)
        console.msgbox(TITLE, "Password is: {}\nsaved as /root/redis_password.txt".format(requirepass_out))
