WEBMIN_FW_TCP_INCOMING = 22 80 443 12320 12321

COMMON_CONF += nodejs-install tkl-webcp
COMMON_OVERLAYS += tkl-webcp nginx

include $(FAB_PATH)/common/mk/turnkey.mk
