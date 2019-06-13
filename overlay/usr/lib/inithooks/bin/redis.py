#!/usr/bin/python
"""Set Redis-commander password and Redis remote IP bind and protected-mode directives

Option:
    --ip_bind=         unless provided, will ask interactively
    --pass=            unless provided, will ask interactively
    --protected_mode=  disabled by-default
"""

import sys
import getopt
import hashlib

from executil import system, ExecError
from dialog_wrapper import Dialog


def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

DEFAULT_BIND = "0.0.0.0"

def validate_ip(ipaddr):
    if (ipaddr.count('.') != 3):
        return False
    parts = ipaddr.split('.')
    for part in parts:
        if not part.isdigit() or not (0 <= int(part) <= 255):
            return False
    return True

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'ip_bind=', 'protected_mode='])
    except getopt.GetoptError, e:
        usage(e)

    pass = ""
    ip_bind = ""
    protected_mode = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--ip_bind':
            ip_bind = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
             "Redis-commander password",
             "Enter password to access redis-commander UI")
    if not ip_bind:
        d = Dialog('TurnKey Linux - First boot configuration')
        while True:
            ip_bind = d.get_input(
                "IPv4 Address to access Redis",
                ("Enter IPv4 Address that will be allowed "
                 "to access the Redis instance."),
                 DEFAULT_BIND)
            if validate_ip(ip_bind):
                break
            d.msgbox("Invalid IPv4 Address",
                "\"{}\" is not a valid IPv4 address!".format(ip_bind))
            
    if not protected_mode:
        d = Dialog('TurnKey Linux - First boot configuration')
        protected_mode = d.yesno('Keep protected-mode enabled?',
                                 ("In this mode Redis only replies to queries from the loopback "
                                  "interfaces. Reply to other clients connecting from other addresses "
                                  "will receive an error, noting why & how to configure Redis. "
                                  "(disabled by-default)"),
                                  'Yes', 'No')

    protected_mode_string = { True: "yes", False: "no" }
    conf = "/etc/redis/redis.conf"
    redis_commander_conf = "/etc/init.d/redis-commander" 
    system("sed -i \"s|^bind .*|bind %s|\" %s" % (ip_bind, conf))
    system("""
            sed -i \"s|^protected-mode .*|protected-mode %s|\" %s""" 
% (protected_mode_string[protected_mode], conf))
    system("""
            sed -i \"s|--http-auth-password=.*|--http-auth-password=%s|\" %s""" 
% (password, redis_commander_conf))

    # restart redis and redis commander if running so change takes effect
    try:
        system("systemctl is-active --quiet redis-server.service")
        system("service redis-server restart")
    except ExecError, e:
        pass

    try:
        system("systemctl is-active --quiet redis-commander.service")
        system("systemctl daemon-reload")
        system("service redis-commander restart")
    except ExecError, e:
        pass


if __name__ == "__main__":
    main()
