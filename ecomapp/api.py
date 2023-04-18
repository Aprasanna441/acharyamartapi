from ecomapp import views
from django.urls import path
from ecomapp.views import UserLoginSerializerView,UserRegistrationSerializerView,ForgetPasswordSerializerView,ChangePasswordSerializerView
from ecomapp.views import ListProductSerializerView,CategoricalListProductSerializerView
from django.urls import path

urlpatterns = [
    path('login/',UserLoginSerializerView.as_view(),name="login"),
    path('signup/',UserRegistrationSerializerView.as_view(),name="signup"),
    path('forget-password/',ForgetPasswordSerializerView.as_view(),name="forgetpassword"),
    path('change-password/',ChangePasswordSerializerView.as_view(),name="chagepw"),
    path('list-products/',ListProductSerializerView.as_view(),name="listproducts"),
    path('category-products/',CategoricalListProductSerializerView.as_view(),name="cat-prod-view")



 





    
]


