from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist

from mailadmin.models import Account, Domain


class MailadminAuthenticationBackend(ModelBackend):
    def has_perm(self, user_obj, perm, obj=None):
        granted = None
        try:
            if perm == 'admin':
                if int(user_obj.useradditions.roles) == 4:
                    granted = True
            elif perm == 'domain_admin':
                if int(user_obj.useradditions.roles) >= 2:
                    granted = True
                    if int(user_obj.useradditions.roles) == 2 and type(obj) == Domain and obj not in user_obj.useradditions.domains.all():
                        # if the user is "only" domain admin we need to check access for a given domain, if any.
                        granted = False
            elif perm == 'privileged':
                if int(user_obj.useradditions.roles) >= 1:
                    granted = True
                    if int(user_obj.useradditions.roles) == 1 and type(obj) == Account:
                        # if the user is "only" privileged and need to check access for the given account, if any.
                        if obj.user != user_obj:
                            granted = False
            elif perm == 'user':
                if int(user_obj.useradditions.roles) >= 0:
                    granted = True
                    if type(obj) == Account:
                        if int(user_obj.useradditions.roles) < 2 and obj.user != user_obj:
                            granted = False
        except ObjectDoesNotExist:
            if perm == 'user':
                granted = True

        if granted is not None:
            return granted

        return super(MailadminAuthenticationBackend, self).has_perm(user_obj, perm, obj)
