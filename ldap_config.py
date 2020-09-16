import ldap
#from django_auth_ldap.config import LDAPSearch, NestedGroupOfNamesType
import logging, logging.handlers

logfile = "/opt/netbox/logs/django-ldap-debug.log"
my_logger = logging.getLogger('django_auth_ldap')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(   logfile, maxBytes=2048 * 500, backupCount=5)
my_logger.addHandler(handler)

AUTH_LDAP_SERVER_URI = 'ldap://192.168.0.100'

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0
}

AUTH_LDAP_BIND_DN = "CN=netboxsa,OU=Groups,DC=shliss,DC=ru"
AUTH_LDAP_BIND_PASSWORD = "ZAQ12wsx"

LDAP_IGNORE_CERT_ERRORS = True

from django_auth_ldap.config import LDAPSearch

AUTH_LDAP_USER_SEARCH = LDAPSearch("DC=shliss,DC=ru", ldap.SCOPE_SUBTREE, "sAMAccountName=%(user)s")

#AUTH_LDAP_USER_DN_TEMPLATE = None

#AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,OU=Groups,DC=shliss,DC=ru"

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

AUTH_LDAP_GROUP_SEARCH = LDAPSearch("dc=shliss,dc=ru", ldap.SCOPE_SUBTREE, "(objectClass=Group)")

# Simple group restrictions
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
AUTH_LDAP_REQUIRE_GROUP = "CN=netbox_active,OU=Groups,DC=shliss,DC=ru"
#AUTH_LDAP_DENY_GROUP = "cn=disabled,ou=django,ou=groups,dc=example,dc=com"
#AUTH_LDAP_ALWAYS_UPDATE_USER = True

#AUTH_LDAP_MIRROR_GROUPS = True

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "CN=netbox_active,OU=Groups,DC=shliss,DC=ru",
    "is_staff": "CN=netbox_staff,OU=Groups,DC=shliss,DC=ru",
    "is_superuser": "CN=netbox_superuser,OU=Groups,DC=shliss,DC=ru"
}
AUTH_LDAP_FIND_GROUP_PERMS = True

AUTH_LDAP_CACHE_TIMEOUT = 3600

#AUTH_LDAP_CACHE_GROUPS = True
AUTHENTICATION_BACKENDS = [
            'django_auth_ldap.backend.LDAPBackend',
                'django.contrib.auth.backends.ModelBackend',
]

