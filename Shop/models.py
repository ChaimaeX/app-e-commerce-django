from urllib import request
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
# Create your models here.
# j ai catre table maintenant produit , users , commandes , productCommande, //


class category(models.Model):
     name = models.IntegerField()

class Produit(models.Model):
     """
     une facture associet a plusieur produit
     une produit associet a un facture
     # """
     category =models.TextField(max_length=100)
     # img = models.ImageField()
     name = models.TextField(max_length=32)
     image = models.ImageField(upload_to= 'static/img',blank=True)
     quantity = models.IntegerField()
     price = models.DecimalField(max_digits =10, decimal_places=2)
     new_price = models.DecimalField(max_digits =10, decimal_places=2,default=0)
     total = models.DecimalField(max_digits =10 , decimal_places=2,null=True)
     TauxRemise = models.IntegerField()
     descreption =models.TextField(max_length=200)
     # preferer
     class Meta:
          verbose_name ="Produit"
          verbose_name_plural ="Produits"
          

     def _str_(self):
         return f"{self.name}"
     
     @property
     def get_total(self):
        total = self.quantity *self.price
        return total
     
class  Facture(models.Model):
    
     client = models.ForeignKey(User, on_delete=models.CASCADE)
     commande_date_time = models.DateTimeField(auto_now_add=True)
     total =  models.DecimalField(max_digits =10 , decimal_places=2)# Exemple avec 10 chiffres au maximum et 2 chiffres après la virgule
     last_update_date = models.DateTimeField(null = True, blank=True)
     confirmer = models.BooleanField(default=False)
     Adresse = models.CharField(max_length=132,null=True)
     ville = models.CharField(max_length=132,null=True)
     telephone = models.IntegerField(null=True)

     class Meta:
          verbose_name = "Facture"
          verbose_name_plural ="Factures"

     def _str_(self):
         return f"{self.client}"
     


class CommandeProduct(models.Model):

     facture = models.ForeignKey(Facture, related_name='commande_products', on_delete=models.CASCADE)
     produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
     prix_achat = models.DecimalField(max_digits =10 , decimal_places=2)
     quantity_achat = models.IntegerField()
     total_a = models.DecimalField(max_digits =10 , decimal_places=2)
    

     class Meta:
          verbose_name = "commande"
          verbose_name_plural ="commandes"
     
     def get_total(self):
        total_a = self.prix_achat *self.quantity_achat
        return total_a
     
class Contact(models.Model):
    name = models.TextField(max_length=32)
    email = models.EmailField()
    subj = models.TextField(max_length=32)
    message = models.TextField(max_length=200)

    class Meta:
          verbose_name = "message"
          verbose_name_plural ="messages"

    def _str_(self):
         return f"{self.email}"