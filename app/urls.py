from django.urls import path
from django.urls import path
from . import views
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [

    # =======================AI Agent=================
    path('ai-chat/', views.ai_chat, name='ai_chat'),

    # ================== HOME / PRODUCT ==================
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>/', views.ProductDetailsView.as_view(), name='product-detail'),

    # ================== CHECKOUT / PAYMENT ==================
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('orders/', views.orders, name='orders'),

 # Razorpay integration
    path('create-payment/', views.CreatePaymentView.as_view(), name='create_payment'),
    path('razorpay-callback/', views.PaymentCallBackView.as_view(), name='razorpay_callback'),


    # ================== CART ==================
    path('cart/', views.show_cart, name='showcart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('remove-cart/<int:id>/', views.remove_cart, name='remove_cart'),
    path('pluscart/', views.plus_cart, name='plus_cart'),
    path('minuscart/', views.minus_cart, name='minus_cart'),

    # ================== BUY NOW / PROFILE / ADDRESS ==================
    path('buy-now/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('delete-address/<int:id>/', views.delete_address, name='delete_address'),

    # ================== CATEGORIES ==================
    path('necklace/', views.necklace, name='necklace'),
    path('necklace/<slug:data>/', views.necklace, name='necklacedata'),
    path('earrings/', views.earrings, name='earrings'),
    path('earrings/<str:data>/', views.earrings, name='earringsdata'),
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<str:data>/', views.topwear, name='topweardata'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<str:data>/', views.bottomwear, name='bottomweardata'),

    # ================== LOGIN / LOGOUT ==================
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='app/login.html',
            authentication_form=LoginForm,
            redirect_authenticated_user=True
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # ================== PASSWORD CHANGE ==================
    path(
        'passwordchange/',
        auth_views.PasswordChangeView.as_view(
            template_name='app/passwordchange.html',
            form_class=MyPasswordChangeForm,
            success_url='/passwordchangedone/'
        ),
        name='passwordchange'
    ),
    path(
        'passwordchangedone/',
        auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),
        name='passwordchangedone'
    ),

    # ================== PASSWORD RESET ==================
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='app/password_reset.html',
            form_class=MyPasswordResetForm
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='app/password_reset_confirm.html',
            form_class=MySetPasswordForm
        ),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),
        name='password_reset_complete'
    ),

    # ================== REGISTER ==================
    path('register/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
