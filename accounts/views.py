from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


from accounts.forms import AuthUserForm, RegisterUserForm


class SignUpView(generic.CreateView):
    model = User
    template_name = 'accounts/signup.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid
    

class LoginView(LoginView):
    model = User
    template_name = 'accounts/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('main_page')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main_page')

