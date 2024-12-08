import logging
from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from hyrelater.models import CustomUser, Candidate, Employer, Agency

logger = logging.getLogger(__name__)

class LandingPageView(View):
    def get(self, request):
        return render(request, 'index.html')

class SignUpView(View):
    def get(self, request):
        context = {
            'current_year': datetime.now().year,
        }
        return render(request, 'signup.html', context)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            logger.error("Passwords do not match for user: %s", username)
            return redirect('signup')

        try:
            if user_type == 'candidate':
                user = CustomUser.objects.create_user(email=email, password=password, user_type=user_type)
                Candidate.objects.create(user=user)
            elif user_type == 'employer':
                user = CustomUser.objects.create_user(email=email, password=password, user_type=user_type)
                Employer.objects.create(user=user)  
            elif user_type == 'agency':
                user = CustomUser.objects.create_user(email=email, password=password, user_type=user_type)
                Agency.objects.create(user=user)  
            user.save()
            messages.success(request, "Signup Successful, Please Log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            logger.error("Signup error for user %s: %s", username, str(e))
            return redirect('signup')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'candidate':
                return redirect('candidate_dashboard')  
            elif user.user_type == 'employer':
                return redirect('employer_dashboard')  
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')
