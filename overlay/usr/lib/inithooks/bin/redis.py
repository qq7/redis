#!/usr/bin/python3
"""Set Redis-commander password and Redis remote IP bind and protected-mode
directives.

Option:
    --ip_bind=         unless provided, will ask interactively
    --pass=            unless provided, will ask interactively
    --protected_mode=  disabled by-default
"""

import sys
import getopt
import hashlib
import subprocess

from dialog_wrapper import Dialog

DEFAULT_BIND = "127.0.0.1"


def usage(s=None):
    if s:
        print("Error:", s, file=sys.stderr)
    print("Syntax: %s [options]" % sys.argv[0], file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)


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
                                       ['help', 'pass=',
                                        'ip_bind=', 'protected_mode='])
    except getopt.GetoptError as e:
        usage(e)

    password = ""
    ip_bind = ""
    protected_mode = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--ip_bind':
            ip_bind = val
        elif opt == '--pass':
            password = val
        elif opt == 'protected_mode':
            protected_mode = val

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
                ("Enter IPv4 Address that will be allowed"
                 " to access the Redis instance."),
                DEFAULT_BIND)
            if validate_ip(ip_bind):
                break
            d.msgbox(
                "Invalid IPv4 Address",
                "\"{}\" is not a valid IPv4 address!".format(ip_bind))

    if not protected_mode:
        d = Dialog('TurnKey Linux - First boot configuration')
        protected_mode = d.yesno(
                'Keep protected-mode enabled?',
                ("In this mode Redis only replies to queries from the loopback"
                 " interfaces. Reply to other clients connecting from other"
                 " addresses will receive an error, noting why & how to"
                 " configure Redis. (disabled by-default)"),
                'Yes', 'No')

    protected_mode_string = {True: "yes", False: "no"}
    conf = "/etc/redis/redis.conf"
    redis_commander_conf = "/etc/init.d/redis-commander"
    subprocess.run(["sed", "-i", "s|^bind .*|bind %s|" % ip_bind, conf])
    subprocess.run([
        "sed", "-i",
        "s|^protected-mode .*|protected-mode %s|" %
        protected_mode_string[protected_mode],
        conf])
    subprocess.run([
        "sed", "-i",
        "s|--http-auth-password=.*|--http-auth-password=%s|" %
        password, redis_commander_conf])

    # restart redis and redis commander if running so change takes effect
    try:
        subprocess.run(["systemctl", "is-active",
                        "--quiet", "redis-server.service"])
        subprocess.run(["service", "redis-server", "restart"])
    except ExecError as e:
        pass

    try:
        subprocess.run(["systemctl", "is-active",
                        "--quiet", "redis-commander.service"])
        subprocess.run(["systemctl", "daemon-reload"])
        subprocess.run(["service", "redis-commander", "restart"])
    except ExecError as e:
        pass


if __name__ == "__main__":
    main()
