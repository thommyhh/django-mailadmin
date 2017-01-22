from django.forms import Form, ModelForm
from django.forms.models import ModelChoiceField

from .models import *


class DomainForm(ModelForm):
    class Meta:
        model = Domain
        fields = ['name', 'active']


class DomainEditForm(DomainForm):
    class Meta(DomainForm.Meta):
        exclude = ['name']


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['domain', 'name', 'password', 'active', 'quota', 'enableAutoReply', 'autoReplyText', 'catchAll',
                  'redirectTarget']


class AccountEditForm(AccountForm):
    class Meta(AccountForm.Meta):
        exclude = ['domain', 'name']

    def __init__(self, *args, **kwargs):
        AccountForm.__init__(self, *args, **kwargs)
        # make the password field not required in the editing form
        self.fields['password'].required = False

    def save(self, commit=True):
        if self.instance.password == '':
            '''
            If the password is empty, reset the old password form the database
            '''
            account = Account.objects.get(pk=self.instance.pk)
            self.instance.password = account.password
        AccountForm.save(self, commit)


class AliasForm(ModelForm):
    class Meta:
        model = Alias
        fields = ['name', 'account']


class MailinglistForm(ModelForm):
    class Meta:
        model = Mailinglist
        fields = ['domain', 'name']


class MailinglistAddAccountForm(Form):
    instance = None  # type Mailinglist

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        Form.__init__(self, *args, **kwargs)
        self.fields['account'] = ModelChoiceField(
            self.instance.domain.account_set.exclude(mailinglists=self.instance), empty_label='')


class AccountAddAliasForm(ModelForm):
    class Meta:
        model = Alias
        fields = ['account', 'name']


class AccountAddMailinglistForm(Form):
    instance = None  # type Account

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        Form.__init__(self, *args, **kwargs)
        self.fields['mailing_list'] = ModelChoiceField(
            self.instance.domain.mailinglists.exclude(accounts=self.instance), empty_label='')


class ExternalReceiverForm(ModelForm):
    class Meta:
        model = ExternalReceiver
        fields = ['mailing_list', 'name']


class RedirectForm(ModelForm):
    class Meta:
        model = Redirect
        fields = ['domain', 'name', 'target']
