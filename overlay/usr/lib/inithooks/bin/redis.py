#!/usr/bin/python
"""Set Redis password and range

Option:
    --range=    unless provided, will ask interactively
    --pass=     unless provided, will ask interactively

"""

import sys
import getopt

from executil import system, ExecError
from dialog_wrapper import Dialog

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

DEFAULT_RANGE = 127.0.0.1

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'range='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    range = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--range':
            range = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "Redis Password",
            "Enter new password for the Redis instance.")
    if not range:
        d = Dialog('TurnKey Linux - First boot configuration')
        range = d.get_input(
            "GitLab Domain",
            "Enter the range that could access the Redis instance.",
            DEFAULT_RANGE)
    
    conf = "/etc/couchdb/local.ini"
    
    system("sed -i \"s|^admin =.*|admin = %s|\" %s" % (hashpass, conf))

    # restart couchdb if running so change takes effect
    try:
        system("systemctl is-active --quiet redis.service")
        system("service redis restart")
    except ExecError, e:
        pass


if __name__ == "__main__":
    main()

