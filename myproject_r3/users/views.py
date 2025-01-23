from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UserChangeForm,PasswordChangeForm
from django.views import View
from .models import Region,UserProfile
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .forms import RegionForm,UserChangeForm
import requests
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings


class TopView(TemplateView):
    template_name = 'users/top.html'

class LoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

class LogoutView(LoginRequiredMixin,LogoutView):
    template_name = 'users/top.html'

class SignupView(View):
    def get(self,request):
        form = UserCreationForm()
        return render(request,'users/signup.html',{'form':form})
    
    def post(self,request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('signup_complete')
        return render(request,'users/login.html',{'form':form})
    
class Signup_CompleteView(TemplateView):
    template_name = 'users/signup_complete.html'

class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'users/profile.html'

class ProfileEditView(LoginRequiredMixin,UpdateView):
    form_class = UserChangeForm
    second_form_class = PasswordChangeForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'password_form' not in context:
            context['password_form'] = self.second_form_class(user=self.request.user)
        return context
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST,instance=self.object)
        password_form = self.second_form_class(user=request.user,data=request.POST)

        if 'old_password' in request.POST:
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request,password_form.user)
                messages.success(request,"パスワードを変更しました。")
                return redirect(self.success_url)
            else:
                messages.error(request,"パスワードの変更に失敗しました。")
                return self.render_to_response(self.get_context_data(form=form,password_form=password_form))
    
        else:
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.instance)
                return self.form_valid(form)
            else:
                messages.error(request,"情報の保存に失敗しました。")
                return self.render_to_response(self.get_context_data(form=form,password_form=password_form))
        
    def form_valid(self,form):
        messages.success(self.request,"情報を保存しました。")
        return redirect(self.success_url)

@login_required    
def region_register_view(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        print("User:", request.user)
        print("Profile Exists:", UserProfile.objects.filter(user=request.user).exists())

        if form.is_valid():
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)

            user_profile.region = form.cleaned_data['region']
            user_profile.save()

            return redirect('item_list')
        
    else:
        form = RegionForm()
    return render(request,'users/region_register.html',{'form':form})

def get_weather_data(region_name):
    api_key = settings.API_KEY
    url = f'http://api.openweathermap.org/data/2.5/weather?q={region_name}&appid={api_key}&lang=ja&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_weather_for_user(user):
    if user.is_authenticated:
        user_region = user.userprofile.region
        if user_region:
            return get_weather_data(user_region.name)
    return None

