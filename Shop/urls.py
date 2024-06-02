from django.shortcuts import render
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
     path('' ,views.HomeView.as_view() , name='Home'),
     path('Shop' ,views.shopView.as_view() , name='shop'),
     path('detail/<int:pk>' ,views.datailProduct.as_view() , name='detail'),
     path('Chekout' ,views.chekoutView.as_view() , name='Chekout'),
     path('confirmer' ,views.confirmerView.as_view() , name='confirmer'),
     path('Login' ,views.loginView.as_view() , name='Login'),
     path('sign_up' ,views.signUpView.as_view() , name='sign_up'),
     path('remercie' ,views.remercieView.as_view() , name='remercie'),
     path('user-logout', views.user_logout, name="user-logout"),
     path('dashboard/', views.dashboardView, name='dashboard'),
     path('dashboard/post/', views.post_dashboard, name='post_dashboard'),
     path('facture/<int:pk>', views.InvoiceVisualizationView.as_view(), name="facture"),
     path('facture-pdf/<int:pk>', views.get_invoice_pdf, name="facture-pdf"),
     path('Stock', views.StockView.as_view(), name="Stock"),
     path('up-produit', views.upProduit.as_view(), name="up-produit"),
     path('Ajouter_Produit', views.addProduit.as_view(), name="Ajouter_Produit"),
     path('contact', views.contact.as_view(), name="contact"),
     path('List-User', views.ListUserView.as_view(), name="List-User"),
     path('messages', views.MessagesView.as_view(), name="messages"),
     path('Facture-All', views.get_FactureAll_pdf, name="Facture-All"),
     path('about_Us', views.aboutView.as_view(), name="about_Us"),
     


    
    



] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
