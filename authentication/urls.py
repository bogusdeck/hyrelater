from django.urls import path
from .views import LandingPageView, SignUpView, LoginView, LogoutView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

# Tastypie API integration (if needed)
# Uncomment and use if JobResource and Tastypie are configured correctly.
# from tastypie.api import Api
# from core.api.resources import JobResource

# api = Api(api_name='v1')
# api.register(JobResource())

# urlpatterns += [
#     path('api/', include(api.urls)),
# ]
