from django.views.generic import TemplateView,CreateView,FormView,View

from ecomapp.utils import Util

from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_str,force_bytes,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models  import Product,Cart,CartProduct,Customer,Order,CustomUser,Category

from django.shortcuts import redirect,render
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse

from .forms import OrderForm,CustomerRegistrationForm,CustomerLoginForm,ForgetPasswordForm,ResetPasswordForm,ChangePasswordForm

from django.urls import reverse_lazy,reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator




import requests # for epay
import xml.etree.ElementTree as ET



####just to handover the  the session wala cart_id to a real customer
class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)

        
class HomeView(EcomMixin,TemplateView):
    template_name="home.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        products=Product.objects.all().order_by("-view_count")
        
        paginator=Paginator(products,2)
        page_number=self.request.GET.get('page')
        prod_list=paginator.get_page(page_number)
        context["prod_list"]=prod_list

        context["products"]=prod_list
        context["categories"]=Category.objects.all()
        

        return context


class SearchView(TemplateView):
    template_name="home.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        key = self.request.GET.get('key')
        print(key)
        context["products"]=Product.objects.filter(title__icontains=key)
        context["categories"]=Category.objects.all()
        

        return context



    




    
    
class CategoricalProductView(EcomMixin,TemplateView):
    template_name="categoryproducts.html"
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        products=Product.objects.all()
        paginator=Paginator(products,2)
        page_number=self.request.GET.get('page')
        prod_list=paginator.get_page(page_number)
        context["prod_list"]=prod_list
        context["products"]=prod_list
    
        context["categories"]=Category.objects.all()

        return context


class AllProductView(EcomMixin,TemplateView):
    template_name="categoryproducts.html"
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category')
        category=Category.objects.get(id=category_id)
        products=Product.objects.filter(category=category).order_by("-id")
        context["categories"]=Category.objects.all()
        context["category"]=category

        paginator=Paginator(products,2)
        page_number=self.request.GET.get('page')
        prod_list=paginator.get_page(page_number)
        context["prod_list"]=prod_list
        context["products"]=prod_list
        context["no"]=len(context["products"])

        return context
    
class ProductInfoView(EcomMixin,TemplateView):
    template_name="productinfo.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        prod_id = self.kwargs.get('pk')
        product=Product.objects.get(id=prod_id)
        product.view_count+=1
        product.save()
        
        context["product"]=product
        return context
    
class AddToCartView(EcomMixin,TemplateView):
    template_name="cart.html"
    

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        prod_id = self.kwargs.get('pid')
        product=Product.objects.get(id=prod_id)
        cart_id=self.request.session.get("cart_id",None)

        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)

            
            check=cart_obj.cartproduct_set.filter(product=product)
            #product is in cart,just increast quantity
            if check.exists():
                cartproduct=check.first()
                cartproduct.quantity+=1
                cartproduct.subtotal+=product.selling_price
                cartproduct.save()
                cart_obj.total+=product.selling_price 
                cart_obj.save()
                

#product new for the cart
            else:
                cartproduct=CartProduct.objects.create(cart=cart_obj,product=product,rate=product.selling_price,quantity=1,subtotal=product.selling_price)
                cart_obj.total+=product.selling_price
                cart_obj.save()
                self.request.session["item"]+=1
                

   #saving cart in session         
        else:
            cart_obj=Cart.objects.create(total=0)
            self.request.session["cart_id"]=cart_obj.id
            cartproduct=CartProduct.objects.create(cart=cart_obj,product=product,rate=product.selling_price,quantity=1,subtotal=product.selling_price)
            cart_obj.total+=product.selling_price
            cart_obj.save()
            self.request.session["item"]=1
            print("naya baneko xa")
        return context
    
class CartView(EcomMixin,TemplateView):
    template_name="mycart.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get("cart_id",None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
        else:
            cart=None  

        context["cart"]=cart
         

        return context


#to alter product quantity
def plus(request,id):
    
    cp_obj=CartProduct.objects.get(id=id)
    cart_from_url=cp_obj.cart
    

    cp_obj.quantity+=1
    cp_obj.subtotal+=cp_obj.rate
    cp_obj.save()
    cart_from_url.total+=cp_obj.rate 
    cart_from_url.save()
  

    return redirect("ecomapp:showcart")





def minus(request,id):
    cp_obj=CartProduct.objects.get(id=id)
    cart_from_url=cp_obj.cart
    

    cp_obj.quantity-=1
    cp_obj.subtotal-=cp_obj.rate
    cp_obj.save()
    cart_from_url.total-=cp_obj.rate 
    cart_from_url.save()
    if cp_obj.quantity==0:
                cp_obj.delete()
                request.session["item"]-=1
    return redirect("ecomapp:showcart")

def remove(request,id):
    cp_obj=CartProduct.objects.get(id=id)
    cart_from_url=cp_obj.cart
    

    
    cart_from_url.total-=cp_obj.subtotal
    cart_from_url.save()

    cp_obj.delete()
    request.session["item"]-=1
    
    return redirect("ecomapp:showcart")



class CheckOutView(LoginRequiredMixin,EcomMixin,CreateView):
    login_url = 'ecomapp:login'
    
    template_name="checkout.html"
    form_class=OrderForm 
    success_url=reverse_lazy('ecomapp:home')

    def get_context_data(self, **kwargs ):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get('cart_id',None)

        if cart_id:
            cart=Cart.objects.get(id=cart_id)
        else:
            cart=None
        context['cart']=cart
        return  context
    
    def form_valid(self,form):
        cart_id=self.request.session.get('cart_id',None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
            form.instance.cart=cart
            form.instance.subtotal=cart.total 
            form.instance.discount=0
            form.instance.total=cart.total
            form.instance.order_status="order received"
            del self.request.session['cart_id']
            del self.request.session["item"]
            pm=form.cleaned_data.get("payment_method")
            order=form.save()
            if pm=="Esewa":
                return redirect(reverse("ecomapp:esewapayment") + "?o_id=" + str(order.id))





        else:
            redirect('ecomapp:home')

        return super().form_valid(form)
    


class EsewaRequestView(View):
    def get(self,request,*args,**kwargs):
        o_id=request.GET.get("o_id")
        order=Order.objects.get(id=o_id)
        
        context={
            "order":order
        }

        return render(request,"esewapayment.html",context)
    



# http://127.0.0.1:8000/?oid=order_29&amt=33.0&refId=0005CH2

def fintecherror(request):
    return  HttpResponse("Payment error aayo Feri prayas garnuhola")


class EsewaVerifyView(View):
    def get(self,request,*args,**kwargs):
        oid=request.GET.get("oid")
        amt=request.GET.get("amt")
        ref_id=request.GET.get("refId")
        url ="https://uat.esewa.com.np/epay/transrec"
        d = {
        'amt': amt,
        'scd': 'EPAYTEST',
        'rid': ref_id,
        'pid':oid,
        }
        resp = requests.post(url, d)
        inside=ET.fromstring(resp.content)
        status=inside[0].text.strip()  #removes white space from the status code 
        order_id=oid.split("_")[1]   #order_12 ko form ma hunxa ani  12 matra nikalne ho esbata
        order_obj=Order.objects.get(id=order_id)
        if status=="Success":
            order_obj.payment_completed=True
            order_obj.save()

            return redirect("/")
        else:
            
            return redirect("/esewapayment/?o_id")
    



class SignupView(CreateView):
    template_name="login.html"
    form_class=CustomerRegistrationForm
    success_url=reverse_lazy('ecomapp:home')
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["form"]=self.form_class
        context["purpose"]="Signup"


        return context
    
    def form_valid(self,form):
        email=form.cleaned_data.get("email")
        password=form.cleaned_data.get("password")
        user=CustomUser.objects.create_user(email,password)
        form.instance.user=user
        login(self.request,user)

        
        

        return super().form_valid(form)

def signout(request):
    logout(request)
    return redirect('ecomapp:home')


from django.contrib import messages
class LoginView(FormView):
    template_name="login.html"
    form_class=CustomerLoginForm
    success_url=reverse_lazy('ecomapp:home')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["form"]=self.form_class
        context["purpose"]="Login"


        return context


    def get_success_url(self):
        if "next" in self.request.GET:
            next=self.request.GET.get("next")
            return next
        else:
            return self.success_url

    


    def form_valid(self,form):
        email=form.cleaned_data.get("email")
        password=form.cleaned_data.get("password")
        user=authenticate(email=email,password=password)
        if user is not None and user.customer:
            login(self.request,user)
        else:
            messages.error(self.request,'Invalid Credentials')
            return redirect('ecomapp:login')


        
        

        return super().form_valid(form)
    

class ForgetPasswordView(FormView):
    template_name="passwordforget.html"
    form_class=ForgetPasswordForm
    success_url="/forget-password/?sent=yes"


    def form_valid(self,form):
        email=form.cleaned_data.get("email")
        

        user=CustomUser.objects.get(email=email)
       
        
        uid=urlsafe_base64_encode(force_bytes(user.id))
        token=PasswordResetTokenGenerator().make_token(user)
        link='http://localhost:8000/resetpassword/'+uid+'/'+token+"/"
        body="Click the link to reset your password"
        data={
                'subject':'Reset your password' ,
                'body' :link,
                'to_email':user.email
                
            }
        Util.send_mail(data)


        
        

        return super().form_valid(form)
    
class ResetPasswordView(FormView):
    template_name="passwordreset.html"
    form_class=ResetPasswordForm
    success_url="/login/"

    def form_valid(self, form):
        useridparam=self.kwargs.get("uid") ## getting from link
 ##decoding
        userid = force_str(urlsafe_base64_decode(useridparam))
        user=CustomUser.objects.get(id=userid)
        
        token=self.kwargs.get("token")
        
     ###3/////////////////////////////////////////////////
        ##### YAHA BUG XA MALAI FIX GARNA AAYENA

        #////////////////////////////////////////


        if user is not None: ## and PasswordResetTokenGenerator.check_token(user,token):
            password=form.cleaned_data.get("new_password")
            user.set_password(password)
            user.save()



        return super().form_valid(form)

class ChangePasswordView(FormView):
    template_name="passwordchange.html"
    form_class=ChangePasswordForm
    success_url="/login"


    
class ProfileView(LoginRequiredMixin,TemplateView):
    template_name="profile.html"
    login_url = 'ecomapp:login'

    def get_context_data(self, **kwargs):

       
        context= super().get_context_data(**kwargs)
        customer=self.request.user.customer
        context["customer"]=customer
        orderss=Order.objects.filter(cart__customer=customer)
        context["orders"]=orderss
        return context


        
# class 




    


class AboutView(TemplateView):
    template_name="about.html"

class ContactView(TemplateView):
    template_name="contact.html"




from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout,authenticate
from  rest_framework import status
from .serializers import LoginSerializer,UserRegistrationSerializer,ForgetPasswordSerializer,UserChangePasswordSerializer
from .serializers import AllProductsSerializer,CategoricalProductsSerializer,AddProductsSerializer,AddToCartSerializer
from .serializers import MyCartSerializer,CheckoutSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import BasicAuthentication

from rest_framework_simplejwt.tokens import RefreshToken



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }





class UserLoginSerializerView(APIView):
    
  
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
    
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None: 
              token=get_tokens_for_user(user)
                 
              cust=Customer.objects.get(user__email=email)
                   
              return Response({'token':token,'msg':'Login success'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST,)
    





class UserRegistrationSerializerView(APIView):
    def post(self, request):
        serializer =UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Create a new user object
            user = CustomUser(
                email=serializer.validated_data['email'],
               
            )
            user.set_password(serializer.validated_data['password'])
            user.save()

            # Create a new customer object
            customer = Customer(
                user=user,
                full_name=serializer.validated_data['full_name'],
                address=serializer.validated_data['address'],
                
            )
            customer.save()
            

            # Return success response
            return Response({'message': 'Customer signed up successfully.'}, status=status.HTTP_201_CREATED)
        else:
            # Return error response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ForgetPasswordSerializerView(APIView):
    def post(self,request):
        serializer=ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.validated_data['email']
            user=CustomUser.objects.get(email=email)
        
            
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://localhost:8000/resetpassword/'+uid+'/'+token+"/"
            body="Click the link to reset your password"
            data={
                    'subject':'Reset your password' ,
                    'body' :link,
                    'to_email':email
                    
                }
            Util.send_mail(data)
            return Response({'message': 'Link sent to email.'}, status=status.HTTP_201_CREATED)
        else:
            # Return error response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordSerializerView(APIView):
     permission_classes=[IsAuthenticated]
     def post(self,request):
          
          serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
          if serializer.is_valid(raise_exception=True):
               return Response({'msg':"Password change success"},status=status.HTTP_200_OK)
          return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ListProductSerializerView(APIView):
    def get(self,request,format=None):
        dataa=Product.objects.all()
        serializer=AllProductsSerializer(dataa,many=True)
        return Response(serializer.data)
    
class CategoricalListProductSerializerView(APIView):
    def get(self,request,format=None):
        search = self.request.query_params.get('category') 
        
        if search:
            dataa=Product.objects.filter(category__title__icontains=search)
            serializer=CategoricalProductsSerializer(dataa,many=True)
        return Response(serializer.data)
    
class AddProductSerializerView(APIView):
    serialier_class=AddProductsSerializer
    permission_classes=[IsAdminUser]
    def post(self,request,format=None):
        serializer=self.serialier_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            product=serializer.save()
            return Response({'message':"Data saved successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)


        

class AddToCartSerializerView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,format=None):
        serializer=AddToCartSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            product_id=serializer.validated_data['product_id']
            customerr=serializer.validated_data['customer']
            id=CustomUser.objects.get(email=customerr).id
            
            customer_id=Customer.objects.get(user__id=id).id
            customer=Customer.objects.get(user__id=id)
                       
            cart_id=Cart.objects.get(customer__id=customer_id).id
            

            product=Product.objects.get(id=product_id)


            # checking if the user already has a cart
            
            if cart_id:
                cart_obj=Cart.objects.get(id=cart_id)
                print("Yes exist garxa")
                # checking if the product already exists()
                check=cart_obj.cartproduct_set.filter(product=product)
                if check.exists():
                    print("Yes product cart maa xa")
                    cartproduct=check.first()
                    cartproduct.quantity+=1
                    cartproduct.subtotal+=product.selling_price
                    cartproduct.save()
                    cart_obj.total+=product.selling_price 
                    cart_obj.save()
                else:
                    print("cart ma xaina")
                    cartproduct=CartProduct.objects.create(cart=cart_obj,product=product,rate=product.selling_price,quantity=1,subtotal=product.selling_price)
                    cart_obj.total+=product.selling_price
                    cart_obj.save()



            #  if no cart exist,create one   
            else:
                print("naya banayeko cart")
                cart_obj=Cart.objects.create(total=0,customer=customer)
                cartproduct=CartProduct.objects.create(cart=cart_obj,product=product,rate=product.selling_price,quantity=1,subtotal=product.selling_price)
                cart_obj.total+=product.selling_price
                cart_obj.save()

                
            
            
            
            
            
            
            return Response("Data saved",status=status.HTTP_200_OK)

            
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)


class MyCartView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,format=None):

        
        email=request.user
        print(email)
        id=CustomUser.objects.get(email=email).id            
        customer_id=Customer.objects.get(user__id=id).id            
        dataa=Cart.objects.get(customer__id=customer_id)
        

        serializer=MyCartSerializer(dataa)
        
             
        
            
            
        return Response(serializer.data)


class CheckOutSerializerView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,format=None):
        serializer=CheckoutSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order_by=serializer.validated_data['order_by']
            shipping_address=serializer.validated_data['shipping_address']
            mobile=serializer.validated_data['mobile']
            payment_method=serializer.validated_data['payment_method']
            
            dropping_email=customerr=serializer.validated_data['email']
            email=request.user
            id=CustomUser.objects.get(email=email).id            
            customer_id=Customer.objects.get(user__id=id).id            
            cart=Cart.objects.get(customer__id=customer_id)
            order=Order(
                    cart=cart,
                    order_by=order_by,
                    shipping_address=shipping_address,
                    mobile=mobile,
                    email=email,
                    subtotal=cart.total,
                    discount=0,
                    total=cart.total,
                    order_status="Order Received",
                    
                    payment_method=payment_method
                    
            )
            order.save()
            return Response("Data saved",status=status.HTTP_200_OK)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)


        

        


    
        

