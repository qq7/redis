#!/usr/bin/python
"""Set Redis-commander password and Redis bind and protected-mode directives

Option:
    --range=    unless provided, will ask interactively
    --password=     unless provided, will ask interactively
    --protected_mode= disabled by-default
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

DEFAULT_RANGE = "0.0.0.0"


def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'password=', 'range='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    range = ""
    protected_mode = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--range':
            range = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
             "Redis-commander password",
             "Enter password to access redis-commander UI")
    if not range:
        d = Dialog('TurnKey Linux - First boot configuration')
        range = d.get_input(
            "IP Range to access Redis",
            ("Enter IP range that would be allowed"
             "to access the Redis instance."),
             DEFAULT_RANGE)
    if not protected_mode:
        d = Dialog('TurnKey Linux - First boot configuration')
        protected_mode = d.yesno('Keep protected-mode enabled?',
                                 ("In this mode Redis only replies to queries from the loopback interfaces, and reply to other clients connecting from other" 
                                  "addresses with an error, explaining what is"
"happening and how to configure Redis properly. (disabled by-default)"),
                                  'Yes', 'No')

    protected_mode_string = { True: "yes", False: "no" }
    conf = "/etc/redis/redis.conf"
    redis_commander_conf = "/etc/init.d/redis-commander" 
    system("sed -i \"s|^bind .*|bind %s|\" %s" % (range, conf))
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
