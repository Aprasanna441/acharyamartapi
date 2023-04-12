from ecomapp import views
from django.urls import path
from ecomapp.views import UserLoginSerializerView

from django.urls import path
app_name="ecomapp"
urlpatterns = [
          path('login/',UserLoginSerializerView.as_view(),name="login"),
 





    
]


