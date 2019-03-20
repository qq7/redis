#!/bin/bash -e

. /etc/default/inithooks

[ -e $INITHOOKS_CONF ] && . INITHOOKS_CONF

# $INITHOOKS_PATH/bin/redis.py 

PASS=$(mcookie)$(mcookie)$(mcookie)$(mcookie)$(mcookie)

sed -ri "s/(# )?requirepass .*./requirepass $PASS/" pass
