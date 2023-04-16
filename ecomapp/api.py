from ecomapp import views
from django.urls import path
from ecomapp.views import UserLoginSerializerView,UserRegistrationSerializerView

from django.urls import path

urlpatterns = [
    path('login/',UserLoginSerializerView.as_view(),name="login"),
    path('signup/',UserRegistrationSerializerView.as_view(),name="signup"),


 





    
]


