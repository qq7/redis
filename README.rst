Redis - Open Source, In-memory Data Structure Store
===================================================

`Redis`_ is used as a database, cache and message broker. It supports data 
structures such as strings, hashes, lists, sets, sorted sets 
with range queries, bitmaps, hyperloglogs and geospatial indexes 
with radius queries. Redis has built-in replication, Lua scripting, 
LRU eviction, transactions and different levels of on-disk persistence, 
and provides high availability via Redis Sentinel and automatic 
partitioning with Redis Cluster.

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- Redis configurations:

    - Installed from debian package repository (auto security updates).
    - Includes web based management tool `Redis-commander`_.
    - Complex Redis system password auto-generated on firstboot (security).
    - Confconsole plugin provided to view Redis system password (convenience).

- SSL support out of the box.
- Postfix MTA (bound to localhost) to allow sending of email from web
  applications (e.g., password recovery)

Credentials *(passwords set at first boot)*
-------------------------------------------

- Webmin, SSH: username **root**
- Redis-commander: username **admin**

.. _Redis: https://redis.io/
.. _TurnKey Core: https://www.turnkeylinux.org/core
.. _Redis-commander: https://github.com/joeferner/redis-commander
