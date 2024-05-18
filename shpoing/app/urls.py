from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
import seler


urlpatterns = [
    
    path('',views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views. ProductDetailView.as_view(), name='product-detail'),

#CART START
    # 1-Add to cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    # 2-Show data from the database
    path('cart/',views.show_cart,name='showcart'),
    # 3-Plus cart
    path('pluscart/',views.plus_cart),
    # 4-Minus cart
    path('minuscart/',views.minus_cart),
    # 5-Remove cart
    path('removecart/',views.remove_cart),
#CART END

    path('buy/<int:id>', views.buy_now, name='buy-now'),

#PROFILE START
    path('profile/', views.ProfileView.as_view(), name='profile'),
#PROFILE END

    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

#AUTHENTICATION START
    # 1-Registration
    path('registration/', views.CustomerRegistrationView.as_view(), name="customerregistration"),
    # 2-Login
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    # 3-Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    # 4-password change
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',
        form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    # 5-password reset
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',
        form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html')
        ,name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'
        ,form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html')
        ,name='password_reset_complete'),
    path('seler/',include('seler.urls'),name='seler'),
    path('regis/',views.regis,name='regis'),
#AUTHENTICATION END

   


   
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)