from django.conf import settings
from django.db import models
from django.db.models.manager import Manager
from django.db.models.signals import post_delete
from django.dispatch import receiver

from mailadmin.templatetags.permissions import has_permission


class DomainManager(Manager):
    def for_user(self, user):
        query_set = self.get_queryset()
        if has_permission({'user': user}, 'admin'):
            return query_set
        else:
            return query_set.filter(pk__in=[domain.pk for domain in user.useradditions.domains.all()])


class Domain(models.Model):
    objects = DomainManager()
    name = models.CharField(max_length=100, default='')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def aliases(self):
        return Alias.objects.filter(account__domain=self.pk)


class Account(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    quota = models.IntegerField(default=100)
    active = models.BooleanField(default=True)
    redirectTarget = models.CharField(max_length=200, blank=True)
    catchAll = models.BooleanField()
    enableAutoReply = models.BooleanField()
    autoReplyText = models.TextField(blank=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, default=None)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, parent_link=True, default=None, null=True)

    def __str__(self):
        return "{0}@{1}".format(self.name, self.domain.name)


class Alias(models.Model):
    name = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "{0}@{1}".format(self.name, self.account.domain.name)


class Redirect(models.Model):
    name = models.CharField(max_length=100)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, default=None, null=True)
    target = models.CharField(max_length=300, default='')

    def __str__(self):
        return "{0}@{1}".format(self.name, self.domain.name)


class Mailinglist(models.Model):
    name = models.CharField(max_length=100)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, default=None, related_name='mailinglists')
    accounts = models.ManyToManyField(Account, related_name='mailinglists')

    def __str__(self):
        return "{0}@{1}".format(self.name, self.domain.name)


class ExternalReceiver(models.Model):
    name = models.CharField(max_length=200)
    mailing_list = models.ForeignKey(Mailinglist, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.name


class UserAdditions(models.Model):
    ROLES = (
        ('0', 'User'),
        ('1', 'Privileged'),
        ('2', 'Domain admin'),
        ('4', 'Admin')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    roles = models.CharField(max_length=10, choices=ROLES, blank=False, default=0)
    domains = models.ManyToManyField(Domain, related_name='administrators', blank=True)


@receiver(post_delete, sender=Account)
def post_account_delete(sender, instance, *args, **kwargs):
    if instance.user:
        instance.user.delete()
