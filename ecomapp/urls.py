from .views import HomeView,ContactView,AboutView,CategoricalProductView,AllProductView
from .views import ProductInfoView,AddToCartView,CategoricalProductView,CartView
from .views import CheckOutView,SignupView,LoginView,ProfileView,SearchView,EsewaRequestView,EsewaVerifyView
from .views import ForgetPasswordView,ResetPasswordView,ChangePasswordView
from ecomapp import views


from django.urls import path
app_name="ecomapp"
urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('about',AboutView.as_view(),name="about"),
    path('contact',ContactView.as_view(),name="contact"),
    path("categorical",CategoricalProductView.as_view(),name="categorical"),
    path("allproducts/<int:category>",AllProductView.as_view(),name="allproducts"),
    path("productinfo/<int:pk>",ProductInfoView.as_view(),name="productinfo"),
    path('add-to-cart/<int:pid>',AddToCartView.as_view(),name="addtocart"),
    path('showcart',CartView.as_view(),name="showcart"),
    path('plus/<int:id>',views.plus,name="plus"),
    path('minus/<int:id>',views.minus,name="minus"),
    path('remove/<int:id>',views.remove,name="remove"),
    path('checkout',CheckOutView.as_view(),name="checkout"),
    path('signup/',SignupView.as_view(),name="signup"),
    path('signout/',views.signout,name="signout"),
    path('login',LoginView.as_view(),name="login"),
    path('profile',ProfileView.as_view(),name="profile"),
    path('search',SearchView.as_view(),name="search"),
    path('esewapayment/',EsewaRequestView.as_view(),name="esewapayment"),
    path('esewaverify/',EsewaVerifyView.as_view(),name="esewaverify"),
    path('fintecherror',views.fintecherror,name="fintecherror"),
    path('epay-verify',EsewaVerifyView.as_view(),name="epayverify"),
    path('forget-password/',ForgetPasswordView.as_view(),name="forgetpassword"),
    path('resetpassword/<uid>/<token>/',ResetPasswordView.as_view(),name="resetpassword"),
    path('changepassword/',ChangePasswordView.as_view(),name="changepassword"),
    
    






    
]


