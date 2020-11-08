'''Check Redis password'''

import os
import subprocess
from subprocess import PIPE

TITLE = "Check redis password"


def run():
    requirepass = subprocess.Popen(['turnkey-redis-pw', 'get'], stdout=PIPE)
    requirepass_out, requirepass_err = requirepass.communicate()
    if not requirepass_out:
        console.msgbox(TITLE,
                       "Something is wrong with redis configuration file,"
                       " please check your redis.conf")
    else:
        password = requirepass_out.decode()
        with open('/root/redis_password.txt', 'w') as fob:
            fob.write(password)
        console.msgbox(TITLE,
                       "Password is:\n\n{}\nIt has also been saved as"
                       " /root/redis_password.txt".format(password))
