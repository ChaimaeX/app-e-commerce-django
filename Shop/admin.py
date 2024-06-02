from django.contrib import messages
from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Produit)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity','price','total']

    # def changelist_view(self, request, extra_context=None):
    #     low_stock_products = Produit.objects.filter(quantity__lte=5)
    #     if low_stock_products.exists():
    #         message = "Attention : Certains produits ont un stock bas : " + ", ".join([produit.name for produit in low_stock_products])
    #         print(message)
    #         self.message_user(request, message, level='ERROR')
    #     return super().changelist_view(request, extra_context=extra_context)

class AdminUsers(admin.ModelAdmin):
    list_display = ('CompletName' ,'gmail','Adresse','telephone')

class AdminFacture(admin.ModelAdmin):
    list_display= ('client','commande_date_time','total','confirmer','Adresse','ville','telephone')
    
    def save_model(self, request, obj, form, change):
        try:
            obj.save()  # Appel de la méthode save() du modèle Commande
        except ValidationError as e:
            # Ajouter un message d'erreur à afficher dans la page d'administration
            self.message_user(request, f"Erreur lors de l'enregistrement de la commande : {e}", level=messages.ERROR)
        except Exception as e:
            # Gérer d'autres exceptions
            self.message_user(request, f"Une erreur s'est produite lors de l'enregistrement de la commande : {e}", level=messages.ERROR)


class AdminCoPro(admin.ModelAdmin):
    list_display= ('facture','produit','quantity_achat','total_a')


admin.site.register(Facture,AdminFacture)
# admin.site.register(Produit,AdminProduct)
admin.site.register(CommandeProduct,AdminCoPro)
