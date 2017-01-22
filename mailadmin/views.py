from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import *


class BaseView(MultipleObjectMixin, TemplateView):
    domain = None  # type Domain

    def __init__(self, model):
        TemplateView.__init__(self)
        self.model = model

    def get(self, request, *args, **kwargs):
        try:
            self.domain = Domain.objects.get(name__exact=kwargs['domain'])
        except KeyError:
            self.domain = None
        return TemplateView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return {
            'sidebar_active': self.get_sidebar_active(),
            'domain': self.domain,
            'menu_section': self.get_menu_section()
        }

    def get_sidebar_active(self):
        return True

    def get_menu_section(self):
        if self.model is None:
            return ''
        return self.model.__name__


class PermissionBasedView(AccessMixin, BaseView):
    def get_permission_and_object(self, **kwargs):
        return None, None

    def has_permission(self, **kwargs):
        (permission, obj) = self.get_permission_and_object(**kwargs)
        if permission is None:
            return False
        return self.request.user.has_perm(permission, obj)

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(**kwargs):
            return self.handle_no_permission()
        return super(PermissionBasedView, self).dispatch(request, *args, **kwargs)


class LoginView(BaseView):
    http_method_names = ['get', 'post']

    def __init__(self):
        BaseView.__init__(self, None)
        self.template_name = 'Account/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.redirect_user_to_permitted_view(request.user)
        return BaseView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        authentication_form = AuthenticationForm(request, data=request.POST)
        if authentication_form.is_valid():
            user = authentication_form.get_user()  # type: User
            login(request, user)
            return self.redirect_user_to_permitted_view(user)
        else:
            return BaseView.get(self, request, *args, **kwargs)

    def redirect_user_to_permitted_view(self, user):
        # where to redirect the user
        if user.has_perm('domain_admin'):
            redirect_url = reverse('mailAdmin:domainIndex')
        else:
            split_user_name = user.username.split('@')
            account = Account.objects.get(name__exact=split_user_name[0],
                                          domain__name__exact=split_user_name[1])  # type: Account
            redirect_url = reverse('mailAdmin:accountEdit', args=[account.domain.name, account.name])

        return HttpResponseRedirect(redirect_url)

    def get_sidebar_active(self):
        return False


class LogoutView(BaseView):
    http_method_names = 'get'

    def __init__(self):
        BaseView.__init__(self, None)

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('mailAdmin:login'))


class IndexView(LoginRequiredMixin, PermissionBasedView, BaseView):
    redirect_field_name = None

    def __init__(self, model):
        BaseView.__init__(self, model)
        self.model = model
        self.template_name = model.__name__ + '/index.html'

    def get_context_data(self, **kwargs):
        context_data = BaseView.get_context_data(self, **kwargs)
        if self.model == Domain:
            context_data['domains'] = Domain.objects.for_user(self.request.user).order_by('name')
            return context_data
        return context_data

    def get_sidebar_active(self):
        if self.model == Domain:
            return False
        else:
            return self.request.user.has_perm('privileged')

    def get_permission_and_object(self, **kwargs):
        if self.model == Domain:
            return ('domain_admin', None)
        elif self.model in (Account, Alias, Mailinglist, Redirect):
            return ('domain_admin', Domain.objects.get(name__exact=kwargs['domain']))

        return super(IndexView, self).get_permission_and_object(**kwargs)


class EditView(LoginRequiredMixin, PermissionBasedView, BaseView):
    redirect_field_name = None
    http_method_names = ['get', 'post']
    form = None

    def __init__(self, model):
        BaseView.__init__(self, model)
        self.model = model
        self.template_name = model.__name__ + '/edit.html'

    def get(self, request, *args, **kwargs):
        if self.model == Domain:
            self.form = DomainEditForm(instance=Domain.objects.get(name__exact=kwargs['domain']))
        elif self.model == Account:
            self.form = AccountEditForm(instance=Account.objects.get(name__exact=kwargs['account'], domain__name__exact=kwargs['domain']))
        return BaseView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.model == Domain:
            self.form = DomainEditForm(data=request.POST, instance=Domain.objects.get(name__exact=kwargs['domain']))
            if self.form.is_valid():
                domain = self.form.save()
                return HttpResponseRedirect(reverse('mailAdmin:domainEdit', args=(domain.name,)))
        elif self.model == Account:
            self.form = self.form = AccountEditForm(data=request.POST, instance=Account.objects.get(name__exact=kwargs['account'], domain__name__exact=kwargs['domain']))
            if self.form.is_valid():
                self.form.save()
                account = self.form.instance
                try:
                    user = User.objects.get(username__exact=account.name + '@' + account.domain.name)
                    if request.POST['password'] != '':
                        user.set_password(request.POST['password'])
                        user.save()
                except ObjectDoesNotExist:
                    User.objects.create_user(account.name + '@' + account.domain.name, password=request.POST['password'])
                return HttpResponseRedirect(reverse('mailAdmin:accountEdit', args=(account.domain.name, account.name)))
        return BaseView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = BaseView.get_context_data(self, **kwargs)
        context_data['form'] = self.form

        if self.model == Account:
            context_data['account'] = Account.objects.get(name__exact=kwargs['account'], domain__name__exact=kwargs['domain'])
        return context_data

    def get_menu_section(self):
        if self.model == Account:
            return 'Account_Settings'
        return BaseView.get_menu_section(self)

    def get_sidebar_active(self):
        return self.request.user.has_perm('privileged')

    def get_permission_and_object(self, **kwargs):
        if self.model == Domain:
            return ('domain_admin', Domain.objects.get(name__exact=kwargs['domain']))
        elif self.model == Account:
            return ('user', Account.objects.get(name__exact=kwargs['account'], domain__name__exact=kwargs['domain']))

        return super(EditView, self).get_permission_and_object(**kwargs)


class NewView(LoginRequiredMixin, PermissionBasedView, BaseView):
    redirect_field_name = None
    http_method_names = ['get', 'post']
    form = None

    def __init__(self, model):
        BaseView.__init__(self, model)
        self.template_name = model.__name__ + '/new.html'

    def get(self, request, *args, **kwargs):
        if self.model == Domain:
            self.form = DomainForm()
        elif self.model == Account:
                self.form = AccountForm()
        elif self.model == Alias:
            self.form = AliasForm()
        elif self.model == Mailinglist:
            self.form = MailinglistForm()
        elif self.model == Redirect:
            self.form = RedirectForm()
        return BaseView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.model == Domain:
            self.form = DomainForm(request.POST)
            if self.form.is_valid():
                domain = self.form.save()
                return HttpResponseRedirect(reverse('mailAdmin:domainAccounts', args=(domain.name,)))
        elif self.model == Account:
            self.form = AccountForm(request.POST)
            if self.form.is_valid():
                account = self.form.save()  # type: Account
                try:
                    User.objects.get(username__exact=account.name + '@' + account.domain.name)
                except ObjectDoesNotExist:
                    user = User.objects.create_user(account.name + '@' + account.domain.name, password=request.POST['password'])
                    account.user = user
                    account.save()
                return HttpResponseRedirect(reverse('mailAdmin:domainAccounts', args=(account.domain.name,)))
        elif self.model == Alias:
            self.form = AliasForm(request.POST)
            if self.form.is_valid():
                alias = self.form.save()
                return HttpResponseRedirect(reverse('mailAdmin:domainAliases', args=(alias.account.domain.name,)))
        elif self.model == Mailinglist:
            self.form = MailinglistForm(request.POST)
            if self.form.is_valid():
                mailing_list = self.form.save()
                return HttpResponseRedirect(reverse('mailAdmin:domainLists', args=(mailing_list.domain.name,)))
        elif self.model == Redirect:
            self.form = RedirectForm(request.POST)
            if self.form.is_valid():
                redirect = self.form.save()
                return HttpResponseRedirect(reverse('mailAdmin:domainRedirects', args=(redirect.domain.name,)))
        return BaseView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = BaseView.get_context_data(self, **kwargs)
        context_data['form'] = self.form
        if self.model == Domain:
            context_data['domain'] = self.form.instance
            context_data['menu_section'] = 'Settings'
        else:
            context_data['domain'] = Domain.objects.get(name__exact=kwargs['domain'])
        if self.model == Account:
            context_data['menu_section'] = 'Account'
        elif self.model == Alias:
            context_data['menu_section'] = 'Alias'
        elif self.model == Redirect:
            context_data['menu_section'] = 'Redirect'
        return context_data

    def get_sidebar_active(self):
        return not self.model == Domain

    def get_permission_and_object(self, **kwargs):
        if self.model == Domain:
            return 'admin', None
        elif self.model in (Account, Alias, Mailinglist, Redirect):
            return 'domain_admin', Domain.objects.get(name__exact=kwargs['domain'])

        return super(NewView, self).get_permission_and_object(**kwargs)


class DeleteView(LoginRequiredMixin, PermissionBasedView, BaseView):
    redirect_field_name = None
    http_method_names = ['get', 'post']

    def __init__(self, model):
        BaseView.__init__(self, model)
        self.template_name = model.__name__ + '/delete.html'

    def post(self, request, *args, **kwargs):
        redirect_url = None
        domain = Domain.objects.get(name__exact=kwargs['domain'])
        if self.model == Domain:
            domain.delete()
            redirect_url = reverse('mailAdmin:domainIndex')
        elif self.model == Account:
            account = Account.objects.get(domain=domain.pk, name__exact=kwargs['account'])
            account.delete()
            redirect_url = reverse('mailAdmin:domainAccounts', args=(domain.name,))
        elif self.model == Alias:
            alias = Alias.objects.get(account__domain=domain, name__exact=kwargs['alias'])
            alias.delete()
            redirect_url = reverse('mailAdmin:domainAliases', args=(domain.name,))
        elif self.model == Mailinglist:
            mailing_list = Mailinglist.objects.get(domain=domain.pk, name__exact=kwargs['list'])
            mailing_list.delete()
            redirect_url = reverse('mailAdmin:domainLists', args=(domain.name,))
        elif self.model == Redirect:
            redirect = Redirect.objects.get(domain=domain.pk, name=kwargs['redirect'])
            redirect.delete()
            redirect_url = reverse('mailAdmin:domainRedirects', args=(domain.name,))

        return HttpResponseRedirect(redirect_url)

    def get_context_data(self, **kwargs):
        context_data = BaseView.get_context_data(self, **kwargs)

        if self.model == Account:
            context_data['account'] = Account.objects.get(domain=self.domain, name=kwargs['account'])
        elif self.model == Alias:
            context_data['alias'] = Alias.objects.get(account__domain=self.domain, name__exact=kwargs['alias'])
        elif self.model == Mailinglist:
            context_data['list'] = Mailinglist.objects.get(domain=self.domain, name=kwargs['list'])
        elif self.model == Redirect:
            context_data['redirect'] = Redirect.objects.get(domain=self.domain, name=kwargs['redirect'])

        return context_data

    def get_permission_and_object(self, **kwargs):
        if self.model == Domain:
            return 'admin', None
        elif self.model in (Account, Alias, Mailinglist, Redirect):
            print('request permission for "domain_admin" and domain "%s"' % kwargs['domain'])
            print(Domain.objects.get(name__exact=kwargs['domain']))
            return 'domain_admin', Domain.objects.get(name__exact=kwargs['domain'])

        return super(DeleteView, self).get_permission_and_object(**kwargs)


class SubModelMixing(MultipleObjectMixin):
    sub_model = None

    def get_menu_section(self):
        return self.model.__name__ + '_' + self.sub_model.__name__


class SubModelIndexView(SubModelMixing, IndexView):
    def __init__(self, model, sub_model):
        IndexView.__init__(self, model)
        self.sub_model = sub_model
        self.template_name = model.__name__ + '/' + sub_model.__name__ + '/index.html'

    def get_context_data(self, **kwargs):
        context_data = BaseView.get_context_data(self, **kwargs)

        if self.model == Mailinglist and self.sub_model in (Account, ExternalReceiver):
            context_data['list'] = Mailinglist.objects.get(name__exact=kwargs['list'], domain=self.domain)
        elif self.model == Account and self.sub_model in (Alias, Mailinglist):
            context_data['account'] = Account.objects.get(name__exact=kwargs['account'], domain=self.domain)

        return context_data

    def get_permission_and_object(self, **kwargs):
        if self.model == Account and self.sub_model == Alias:
            return 'privileged', Account.objects.get(name__exact=kwargs['account'], domain__name__exact=kwargs['domain'])
        elif self.model == Account and self.sub_model == Mailinglist:
            return 'domain_admin', Domain.objects.get(name__exact=kwargs['domain'])
        elif self.model == Mailinglist:
            return 'domain_admin', Domain.objects.get(name__exact=kwargs['domain'])

        return super(SubModelIndexView, self).get_permission_and_object(**kwargs)


class SubModelAddView(LoginRequiredMixin, PermissionBasedView, SubModelMixing, BaseView):
    redirect_field_name = None
    http_method_names = ['get', 'post']
    form = None

    def __init__(self, model, sub_model):
        BaseView.__init__(self, model)
        self.sub_model = sub_model
        self.template_name = model.__name__ + '/' + sub_model.__name__ + '/add.html'

    def get(self, request, *args, **kwargs):
        if self.model == Mailinglist and self.sub_model == Account:
            self.form = MailinglistAddAccountForm(instance=Mailinglist.objects.get(name__exact=kwargs['list']))
        elif self.model == Mailinglist and self.sub_model == ExternalReceiver:
            self.form = ExternalReceiverForm()
        elif self.model == Account and self.sub_model == Alias:
            self.form = AccountAddAliasForm()
        elif self.model == Account and self.sub_model == Mailinglist:
            self.form = AccountAddMailinglistForm(instance=Account.objects.get(name__exact=kwargs['account'], domain__name__exact=kwargs['domain']))
        return BaseView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        redirect_url = None
        if self.model == Mailinglist and self.sub_model == Account:
            mailing_list = Mailinglist.objects.get(name__exact=kwargs['list'])  # type: Mailinglist
            self.form = MailinglistAddAccountForm(instance=mailing_list, data=request.POST)  #type: MailinglistAddAccountForm
            if self.form.is_valid():
                mailing_list.accounts.add(self.form.cleaned_data['account'])
                mailing_list.save()
                redirect_url = reverse('mailAdmin:mailinglistAccounts', args=(mailing_list.domain.name, mailing_list.name))
        elif self.model == Mailinglist and self.sub_model == ExternalReceiver:
            mailing_list = Mailinglist.objects.get(name__exact=kwargs['list'])  # type: Mailinglist
            self.form = ExternalReceiverForm(request.POST)
            if self.form.is_valid():
                self.form.save()
                redirect_url = reverse('mailAdmin:mailinglistExternals', args=(mailing_list.domain.name, mailing_list.name))
        elif self.model == Account and self.sub_model == Alias:
            account = Account.objects.get(name__exact=kwargs['account'], domain__name__exact=kwargs['domain'])
            self.form = AccountAddAliasForm(data=request.POST)
            if self.form.is_valid():
                self.form.save()
                redirect_url = reverse('mailAdmin:accountAliases', args=(account.domain.name, account.name))
        elif self.model == Account and self.sub_model == Mailinglist:
            account = Account.objects.get(name__exact=kwargs['account'], domain__name__exact=kwargs['domain'])
            self.form = AccountAddMailinglistForm(instance=account, data=request.POST)
            if self.form.is_valid():
                account.mailinglists.add(self.form.cleaned_data['mailing_list'])
                account.save()
                redirect_url = reverse('mailAdmin:accountMailinglists', args=(account.domain.name, account.name))

        if redirect_url is not None:
            return HttpResponseRedirect(redirect_url)
        else:
            return BaseView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = BaseView.get_context_data(self, **kwargs)
        context_data['domain'] = Domain.objects.get(name__exact=kwargs['domain'])
        context_data['form'] = self.form

        if self.model == Mailinglist and self.sub_model in (Account, ExternalReceiver):
            context_data['list'] = Mailinglist.objects.get(name__exact=kwargs['list'], domain=self.domain.pk)
        elif self.model == Account and self.sub_model in (Alias, Mailinglist):
            context_data['account'] = Account.objects.get(name__exact=kwargs['account'], domain=self.domain)

        return context_data

    def get_menu_section(self):
        return BaseView.get_menu_section(self) + '_' + self.sub_model.__name__

    def get_permission_and_object(self, **kwargs):
        if self.model == Account and self.sub_model == Alias:
            return 'privileged', Account.objects.get(name__exact=kwargs['account'], domain__name__exact=kwargs['domain'])
        elif self.model == Account and self.sub_model == Mailinglist:
            return 'domain_admin', Domain.objects.get(name__exact=kwargs['domain'])
        elif self.model == Mailinglist:
            return 'domain_admin', Domain.objects.get(name__exact=kwargs['domain'])

        return super(SubModelAddView, self).get_permission_and_object(**kwargs)


class SubModelRemoveView(LoginRequiredMixin, PermissionBasedView, SubModelMixing, BaseView):
    http_method_names = ['get', 'post']

    def __init__(self, model, sub_model):
        BaseView.__init__(self, model)
        self.sub_model = sub_model
        self.template_name = self.template_name = model.__name__ + '/' + sub_model.__name__ + '/remove.html'

    def post(self, request, *args, **kwargs):
        redirect_url = None

        if self.model == Mailinglist:
            mailing_list = Mailinglist.objects.get(name__exact=kwargs['list'])  # type: Mailinglist
            if self.sub_model == Account:
                account = Account.objects.get(pk=kwargs['account'], domain__name__exact=kwargs['domain'])
                mailing_list.accounts.remove(account)
                mailing_list.save()
                redirect_url = reverse('mailAdmin:mailinglistAccounts', args=(mailing_list.domain.name, mailing_list.name))
            elif self.sub_model == ExternalReceiver:
                external_receiver = ExternalReceiver.objects.get(pk=kwargs['external_receiver'])
                external_receiver.delete()
                redirect_url = reverse('mailAdmin:mailinglistExternals', args=(mailing_list.domain.name, mailing_list.name))
        elif self.model == Account:
            if self.sub_model == Alias:
                alias = Alias.objects.get(pk=kwargs['alias'])
                alias.delete()
                redirect_url = reverse('mailAdmin:accountAliases', args=(alias.account.domain.name, alias.account.name))
            elif self.sub_model == Mailinglist:
                account = Account.objects.get(name__exact=kwargs['account'], domain__name__exact=kwargs['domain'])
                mailing_list = Mailinglist.objects.get(pk=kwargs['mailing_list'])  # type: Mailinglist
                account.mailinglists.remove(mailing_list)
                account.save()
                redirect_url = reverse('mailAdmin:accountMailinglists', args=(account.domain.name, account.name))

        if redirect_url is not None:
            return HttpResponseRedirect(redirect_url)
        else:
            return BaseView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = BaseView.get_context_data(self, **kwargs)

        if self.model == Mailinglist:
            context_data['list'] = Mailinglist.objects.get(name__exact=kwargs['list'], domain=self.domain.pk)
            if self.sub_model == Account:
                context_data['account'] = Account.objects.get(pk=kwargs['account'])
            elif self.sub_model == ExternalReceiver:
                context_data['external_receiver'] = ExternalReceiver.objects.get(pk=kwargs['external_receiver'])
        elif self.model == Account:
            context_data['account'] = Account.objects.get(name__exact=kwargs['account'], domain=self.domain.pk)
            if self.sub_model == Alias:
                context_data['alias'] = Alias.objects.get(pk=kwargs['alias'])
            elif self.sub_model == Mailinglist:
                context_data['mailing_list'] = Mailinglist.objects.get(pk=kwargs['mailing_list'])
        return context_data

    def get_permission_and_object(self, **kwargs):
        if self.model == Account and self.sub_model == Alias:
            return 'privileged', Account.objects.get(name__exact=kwargs['account'], domain__name__exact=kwargs['domain'])
        elif self.model == Account and self.sub_model == Mailinglist:
            return 'domain_admin', Domain.objects.get(name__exact=kwargs['domain'])
        elif self.model == Mailinglist:
            return 'domain_admin', Domain.objects.get(name__exact=kwargs['domain'])

        return super(SubModelRemoveView, self).get_permission_and_object(**kwargs)
