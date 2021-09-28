#!/usr/bin/python3
"""Set Redis-commander password and Redis bind and protected-mode
directives.

Option:
    --bind=             unless provided, will ask interactively.
                            [localhost|all]
    --pass=             unless provided, will ask interactively.
                            WARNING: set good password if unprotected!
    --protected_mode=   unless provided, will ask interactively.
                            [yes|no]
"""

import sys
import getopt
import hashlib
import subprocess

from dialog_wrapper import Dialog


def usage(s=None):
    if s:
        print("Error:", s, file=sys.stderr)
    print(f"Syntax: {sys.argv[0]} [options]", file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)


def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=',
                                        'bind=', 'protected_mode='])
    except getopt.GetoptError as e:
        usage(e)

    password = ""
    bind = ""
    protected_mode = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--bind':
            bind = val
        elif opt == '--pass':
            password = val
        elif opt == '--protected_mode':
            protected_mode = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
             "Redis-commander 'admin' password",
             "Enter password for 'addmin' access to redis-commander UI")

    if not bind:
        d = Dialog('TurnKey Linux - First boot configuration')
        bind = d.menu(
            "Interface(s) for Redis to bind to",
            ("Inteface for Redis to bind to?\n\nIf you wish to securely"
             " allow remote connections using 'all', ensure the system"
             " firewall is enabled & block all traffic on port 6379,"
             " except for the desired remote IP(s).\n\nManually edit the"
             " config file to set a custom interface."),
            choices=(
                ("localhost", "Redis will not respond to remote computer"),
                ("all", "Redis will allow all connections")))
    if bind == "all":
        bind_ip = "0.0.0.0"
    else:
        bind_ip = "127.0.0.1"

    if not protected_mode:
        d = Dialog('TurnKey Linux - First boot configuration')
        protected_mode = d.yesno(
                'Keep protected-mode enabled?',
                "In protected  mode Redis only replies to queries from"
                " localhost. Clients connecting from other addresses will"
                " receive an error, noting why & how to configure Redis.\n"
                "\nUnless you set really good password, this is recommended",
                'Yes', 'No')

    protected_mode_str = {True: "yes", False: "no"}
    protected_mode = protected_mode_str[protected_mode]
    conf = "/etc/redis/redis.conf"
    redis_commander_conf = "/etc/init.d/redis-commander"
    subprocess.run(["sed", "-i", f"s|^bind .*|bind {bind_ip}|", conf])
    subprocess.run([
        "sed", "-i",
        f"s|^protected-mode .*|protected-mode {protected_mode}|",
        conf])
    subprocess.run([
        "sed", "-i",
        f"s|--http-auth-password=.*|--http-auth-password={password}|",
        redis_commander_conf])

    # restart redis and redis commander if running so change takes effect
    try:
        subprocess.run(["systemctl", "is-active",
                        "--quiet", "redis-server.service"])
        subprocess.run(["service", "redis-server", "restart"])
    except ExecError:
        pass

    try:
        subprocess.run(["systemctl", "is-active",
                        "--quiet", "redis-commander.service"])
        subprocess.run(["systemctl", "daemon-reload"])
        subprocess.run(["service", "redis-commander", "restart"])
    except ExecError:
        pass


if __name__ == "__main__":
    main()
