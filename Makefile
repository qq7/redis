WEBMIN_FW_TCP_INCOMING = 22 80 443 6379 12320 12321

COMMON_CONF += tkl-webcp
COMMON_OVERLAYS += tkl-webcp

include $(FAB_PATH)/common/mk/turnkey/nodejs.mk
include $(FAB_PATH)/common/mk/turnkey/nginx.mk
include $(FAB_PATH)/common/mk/turnkey.mk
