from ecomapp import views
from django.urls import path
from ecomapp.views import UserLoginSerializerView,UserRegistrationSerializerView,ForgetPasswordSerializerView,ChangePasswordSerializerView
from ecomapp.views import ListProductSerializerView,CategoricalListProductSerializerView,AddProductSerializerView,AddToCartSerializerView
from django.urls import path

urlpatterns = [
    path('login/',UserLoginSerializerView.as_view(),name="login"),
    path('signup/',UserRegistrationSerializerView.as_view(),name="signup"),
    path('forget-password/',ForgetPasswordSerializerView.as_view(),name="forgetpassword"),
    path('change-password/',ChangePasswordSerializerView.as_view(),name="chagepw"),
    path('list-products/',ListProductSerializerView.as_view(),name="listproducts"),
    path('category-products/',CategoricalListProductSerializerView.as_view(),name="cat-prod-view"),
    path('add-products/',AddProductSerializerView.as_view(),name="add-prod"),
    path('add-to-cart/',AddToCartSerializerView.as_view(),name="addtocartserializer"),
    




 





    
]




# {
#     "email":"urllg@gmail.com",
#     "password":"Hello@123"
# }