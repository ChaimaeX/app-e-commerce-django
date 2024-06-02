import datetime
from django.conf import settings
from django.db.models import Count, Sum
# from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from . forms import CreateUserForm, LoginForm,get_facture
import pdfkit
from django.template.loader import get_template

from django.db.models.functions import ExtractMonth, ExtractQuarter

from django.contrib.auth.decorators import login_required

# - Authentication models and functions

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.utils import timezone

class HomeView(View):
     template_name = "Home.html"
     paginate_by = 6

     def get(self, request, *args, **kwargs):
        item_name = request.GET.get('item-name', '').strip()

        # Fetching products
        if item_name:
            product_objects = Produit.objects.filter(title__icontains=item_name)
        else:
            product_objects = Produit.objects.all()
       
        if request.user.is_authenticated:
            isAutentifiend = True
        else:
            isAutentifiend = False
        
        # Pagination
        paginator = Paginator(product_objects, self.paginate_by)
        page_number = request.GET.get('page')
        product_page = paginator.get_page(page_number)

        context = {
            'product_page': product_page,
            'item_name': item_name,
            'isAutentifiend':isAutentifiend,
        }
        return render(request, self.template_name, context)
class shopView(View):
    template_name="Shop.html"
    paginate_by = 12
  
    def get(self, request, *args, **kwargs):

        item_name = request.GET.get('item-name', '').strip()

        # Fetching products
        if item_name:
            product_objects = Produit.objects.filter(title__icontains=item_name)
        else:
            product_objects = Produit.objects.all()

        # Pagination
        paginator = Paginator(product_objects, self.paginate_by)
        page_number = request.GET.get('page')
        product_page = paginator.get_page(page_number)

        if request.user.is_authenticated:
            isAutentifiend = True
        else:
            isAutentifiend = False
        
        context = {
            'product_page': product_page,
            'item_name': item_name,
            'isAutentifiend': isAutentifiend,
        }
        return render(request, self.template_name,context)
    
class datailProduct(View):
    templates_name = "detail.html"
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = Produit.objects.get(pk=pk)
        category = product.category
        produits = Produit.objects.filter(category=category)
        if request.user.is_authenticated:
            isAutentifiend = True
        else:
            isAutentifiend = False
        
        context={
            'product':product,
            'produits': produits,
            'isAutentifiend':isAutentifiend,
        }
        return render(request, self.templates_name,context)
    



class chekoutView(View):
    template_name = 'chekout.html'

    def get_context_data(self):
        context = {}
        context['is_authenticated'] = self.request.user.is_authenticated
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        print(context)
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        items=[]  
        try:
            if request.user.is_authenticated:
                user_id = request.user.id
                item = request.POST.getlist('product')
                quantity = request.POST.getlist('qte')
                total = request.POST.get('total')
                print(user_id, item, quantity, total)
            
                request.session['item'] = item
                request.session['quantity'] = quantity
                request.session['total'] = total
                return redirect('confirmer')
                
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la création de la commande: {e}")
        return render(request, self.template_name)
    
class confirmerView(View):
    template_name = 'confirmer.html'
    def get(self, request, *args, **kwargs):
        
        user_id = request.user.id
        client = User.objects.get(pk=user_id)
        context={
            'client':client
        }
        
        return render(request, self.template_name,context)
    
    def post(self, request, *args, **kwargs):
       items=[]  
       try:
        if request.user.is_authenticated:
           user_id = request.user.id
           phone = request.POST.get('phone')
           ville = request.POST.get('ville')
           address = request.POST.get('address')
           item = request.session.get('item')
           quantity = request.session.get('quantity')
           total = request.session.get('total')
           import re
           nombre = int(re.search(r'\d+', total).group())
           commande = {
                      'client_id': user_id,
                      'total': nombre,
                      'Adresse' : address,
                      'ville' : ville,
                      'telephone' : phone

                 }
           created = Facture.objects.create(**commande)
           for item, qte in zip(item, quantity):
                          id_list = item.split(',')
                          quantity_list = qte.split(',')
                         
           if created:
                 
                 for id_str, quantity in zip(id_list, quantity_list):
                            produit = Produit.objects.get(pk=int(id_str))
                            total_a = produit.price * int(quantity)
                            data = CommandeProduct(
                                facture = created,
                                produit = produit,
                                prix_achat = produit.price,
                                quantity_achat = int(quantity),
                                total_a = total_a,
                               

                            )
                            items.append(data)
                 creer = CommandeProduct.objects.bulk_create(items)
                 if creer :
                    # messages.success(request,'data saved')
                    return redirect('remercie')
                #  else:
                #       messages.error(request,'Erreur')
               
          
        # else:
        #     messages.warning(request, 'Login first')
       except Exception as e:
            messages.error(request, f"Erreur: {e}")
       return render(request, self.template_name)
    
class loginView(View):
    template_name ="login.html"
    
    def get(self,request,*args,**kwargs):
       
        return render(request,self.template_name) 
    
    def post(self, request, *args, **kwargs):
          form = LoginForm()
          form = LoginForm(request, data=request.POST)

          if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if  user.is_authenticated and user.is_superuser:
                   auth.login(request, user)
                   return redirect('dashboard')
                else:
                    auth.login(request, user)
                    # messages.success(request, 'Connexion réussie.')
                    return redirect('Home')
            else:
                messages.error(request, 'Informations de connexion incorrectes.')
          else:
           messages.error(request, 'Formulaire invalide. Veuillez réessayer.')
          return render(request,self.template_name)  
     
class signUpView(View):
     template_name ="login.html"
     def get(self,request,*args,**kwargs):
        form = CreateUserForm()
        context = {'registerform':form}
        return render(request,self.template_name, context=context)
     def post(self, request, *args, **kwargs):
            form = CreateUserForm()
            #   partie sign up
            form = CreateUserForm(request.POST)

            if form.is_valid():

                   form.save()
            
              
                #    messages.success(request,'data saved seccessfully..')
                   return redirect("Login")
              
            context = {'registerform':form}

            return render(request,self.template_name , context=context)   
     
class remercieView(View):
     template_name ="remircement.html"
     def get(self,request,*args,**kwargs):
        # id = request.user.id
        # users = User.objects.get(pk=id)
        # context={'users':users}
        return render(request,self.template_name)
     
def user_logout(request):

    auth.logout(request)

    return redirect("Home")

@login_required
def dashboardView(request):
        template_name ="dashboard.html"
        factures = Facture.objects.all()
        cpt = 0
        from datetime import datetime
    
        factures = Facture.objects.all().order_by('-commande_date_time')
        mois_demande = datetime.now().month
        factures_par_mois = Facture.objects.filter(
         commande_date_time__month=mois_demande
         ).annotate(
         nombre=Count('id'),
         total_month=Sum('total')
        )
        nombre_total_factures = factures_par_mois.aggregate(Sum('nombre'))['nombre__sum']
        somme_montants_mois_demande = factures_par_mois.aggregate(Sum('total_month'))['total_month__sum']
        message_count = Contact.objects.count()
        # message_count = 0
        user_count = User.objects.count()
        context = {
        'nombre_total_factures': nombre_total_factures,
        'somme_montants_mois_demande': somme_montants_mois_demande,
        'message_count':message_count,
        'user_count':user_count,
        'factures':factures,
         
        }
        
       
        return render(request,template_name,context)
    
@login_required
def post_dashboard(request):
    cpt=0
    if request.method == 'POST':
        from datetime import datetime
        mois_demande = datetime.now().month
        factures_par_mois = Facture.objects.filter(
         commande_date_time__month=mois_demande
         ).annotate(
         nombre=Count('id'),
         total_month=Sum('total')
        )
        nombre_total_factures = factures_par_mois.aggregate(Sum('nombre'))['nombre__sum']
        somme_montants_mois_demande = factures_par_mois.aggregate(Sum('total_month'))['total_month__sum']
        message_count = Contact.objects.count()
        user_count = User.objects.count()
        context = {
        'nombre_total_factures': nombre_total_factures,
        'somme_montants_mois_demande': somme_montants_mois_demande,
        'message_count':message_count,
        'user_count':user_count,
         
        }
        if 'id_modified' in request.POST:
   
            
            paid = request.POST.get('modified')

            try: 

                obj = Facture.objects.get(id=request.POST.get('id_modified'))
                items=[]
                if paid == 'True':

                    for produit_commande in obj.commandeproduct_set.all():  # Correction de l'attribut
                           produit = produit_commande.produit
                           quantite_commandee = produit_commande.quantity_achat  # Correction de l'attribut
                
                             # Diminuer la quantité en stock du produit
                           if  produit.quantity >=  quantite_commandee: 
                                 pass
                           else:
                               items.append(produit.name)
                               
                    if len(items) == 0:
                        for produit_commande in obj.commandeproduct_set.all():  # Correction de l'attribut
                           produit = produit_commande.produit
                           quantite_commandee = produit_commande.quantity_achat 
                           produit.quantity -= quantite_commandee
                           produit.save()
                        obj.confirmer = True
                        obj.save() 
                        messages.success(request,  ("Confirmation effectuée avec succès."))
                    else:
                          
                          if cpt <= 3 :
                              cpt += 1
                              print(cpt)
                              messages.error(request, f"Attention : la quantité en stock des produits suivants est insuffisante : {', '.join(items)}")


        
                else:

                    messages.error(request,  ("Impossible d'effectuer cette modification.")) 
         
                

                 
            except Exception as e:   
                  messages.error(request, f"Désolé, l'erreur suivante s'est  {e}.")  
         
        
         # deleting an invoice    

        if 'id_supprimer' in request.POST:

            try:

                obj = Facture.objects.get(pk=request.POST.get('id_supprimer'))

                obj.delete()

                messages.success(request, ("La suppression a réussi."))   

            except Exception as e:

                messages.error(request, f"Désolé, l'erreur suivante s'est  {e}.") 
        
    return redirect('dashboard')          
 
  

class InvoiceVisualizationView(View):
    """ This view helps to visualize the invoice """

    template_name = 'facture.html'

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        
        context = get_facture(pk)

        return render(request, self.template_name,context)
    
def get_invoice_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    pk = kwargs.get('pk')

    context = get_facture(pk)

    # get html file
    template = get_template('facture-pdf.html')

    # render html with context variables
    html = template.render(context)

    # options of pdf format 
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }

    try:
        # generate pdf 
        pdf = pdfkit.from_string(html, False, options)

        # create http response with pdf
        response = HttpResponse(pdf, content_type='application/pdf')

        # specify file name for the PDF
        response['Content-Disposition'] = 'attachment; filename="facture.pdf"'
        
        return response

    except Exception as e:
        # handle exceptions
        return HttpResponse(f'An error occurred: {e}', status=500)

from datetime import datetime

def get_FactureAll_pdf(request, *args, **kwargs):
    # Récupérer les dates de début et de fin depuis les paramètres de requête
    if request.GET:
     start_date_str = request.GET.get('start_date')
     end_date_str = request.GET.get('end_date')

      # Convertir les chaînes de date en objets datetime
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Filtrer les factures entre la date de début et la date de fin
    commandes = Facture.objects.filter(commande_date_time__range=(start_date, end_date)).select_related('client').prefetch_related('commande_products__produit').all()
    
    sommes = Facture.objects.filter(confirmer=True, commande_date_time__range=(start_date, end_date))
    totalAll = sommes.aggregate(total=Sum('total'))['total'] or 0  # Somme totale des factures

    commandes_list = []

    for commande in commandes:
      if commande.confirmer:
        client = commande.client
        ville = commande.ville
        telephone = commande.telephone
        date = commande.commande_date_time
        email = client.email
        total_c = commande.total
        produits_commande = []

        for commande_produit in commande.commande_products.all():
            produit_nom = commande_produit.produit.name
            produits_commande.append({
                'produit_nom': produit_nom,
            })

        commandes_list.append({
            'nom_client': client.username,
            'ville': ville,
            'telephone': telephone,
            'email': email,
            'date': date,
            'total_c': total_c,
            'produits_commande': produits_commande,
        })
   
    # context['date'] = datetime.now()
    context = {
        'commandes_list': commandes_list,
        'totalAll': totalAll,
        'start_date': start_date_str,
        'end_date': end_date_str,
    }

    template = get_template('Invoce_All-pdf.html')
    html = template.render(context)

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }

    pdf = pdfkit.from_string(html, False, options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename='facture.pdf'"

    return response

class StockView(View):
    """ consulter le stock """
    template_name = 'stock.html'
    product = Produit.objects.all()
    context={
        'product':product,
    }
    def get(self, request, *args, **kwargs):
        product = Produit.objects.all() 
        
        for produit in product:
            if produit.quantity < 5 :
                messages.warning(request,f"la qauntite de {produit.name} presque finie, il est inferieur  a cinq produit")
           
        self.context['product'] = product
        return render(request, self.template_name,self.context)
    
    def post(self, request, *args, **kwargs):
      product = Produit.objects.all() 
       
      if request.POST.get('id_sup'):
        try:
          
           obj = Produit.objects.get(pk= request.POST.get('id_sup'))

           obj.delete()
           messages.success(request, ("The deletion was successful."))   
           product = Produit.objects.all()
           self.context['product'] = product
     
        except Exception as e:
          messages.error(request, f"Sorry, error is : {e}.")  
        
      return render(request, self.template_name,self.context)
    
class upProduit(View):
    product = Produit.objects.all()
    template_name='upProduit.html'
    context ={
        'product':product
    }
    def get(self,request,*args,**kwargs):
        
         return render(request,self.template_name,self.context)  
      
    def post(self,request,*args,**kwargs):
        print(request.POST.get('update'))
        id = request.POST.get('update')
        if request.POST.get('update'):
            obj = Produit.objects.get(pk= request.POST.get('update'))
            self.context['product'] = obj
        else:
         try:
            title = request.POST.get('title')
            NewPrice = request.POST.get('NewPrice')
            price = request.POST.get('price')
            qantite = request.POST.get('qantite')
            total = request.POST.get('total')
            category = request.POST.get('category')
            TauxRemise = request.POST.get('remise')
            image = request.FILES.get('image')
            obj_secondaire =self.context['product']
            print(obj_secondaire.id)
            if not TauxRemise:
                NewPrice = 0
                TauxRemise = 0
            else:
                NewPrice = float(price) - int(TauxRemise) / 100 * float(price)
                total = NewPrice * int(qantite)
            
            obj = Produit.objects.get(pk=obj_secondaire.id)
        #   ila user madkhalch l image f update tb9a la  image l9dima
           
            obj.category = category
            obj.name = title
            obj.quantity = qantite
            obj.price = price
            obj.new_price = NewPrice
            obj.total = total
            obj.TauxRemise = TauxRemise
            if image: 
             obj.image = image
    
            # Sauvegarder les modifications
            obj.save()
            self.context['product'] = obj
            messages.success(request, 'Produit mis à jour avec succès.')
            return redirect('Stock')
           
         except Exception as e :
             messages.error(request, 'Une erreur s\'est produite lors de la mise à jour du produit : {}'.format(str(e)))
         
        return render(request,self.template_name,self.context)
    
class addProduit(View):

    """ add un produit tout sumplement dans un navigateur """
    template_name = 'addProduct.html'
    def get(self,request,*args,**kwargs):
        return render(request, self.template_name)
    def post(self,request,*args,**kwargs):
        # if request.POST.get('update'):

        try: 
            name = request.POST.get('title')
            price = request.POST.get('price')
            TauxRemise = request.POST.get('remise')
            quantity = request.POST.get('qantite')
            category = request.POST.get('category')
            image =  request.FILES.get('image')
            category = request.POST.get('category')
            promo = request.POST.get('promo')
            total = request.POST.get('total')
            descreption = request.POST.get('description')

            # if not promo :
            #     promo = False
            if not TauxRemise:
                NewPrice = 0
                TauxRemise = 0
            else:
                NewPrice = float(price) - int(TauxRemise) / 100 * float(price)
                total = NewPrice * int(quantity)

            print(image)
            add_produit={
                'category':category,
                'name':name,
                'image':image,
                'quantity':quantity,
                'price': price,
                'new_price': NewPrice,
                'total':total,
                'descreption':descreption,
                'TauxRemise':TauxRemise,
            }
            created = Produit.objects.create(**add_produit)
            if created:
                  messages.success(request,'data saved seccessfully..')
            else:
                  messages.error(request , 'Sorry Quantite insufisont ..')
           
        except Exception as e:
               messages.error(request,f"Error ....{e}")
        
        return render(request, self.template_name)
        
class contact(View):
     template_name="contact.html"
     def get(self,request,*args,**kwargs):
        return render(request, self.template_name)

     def post(self,request,*args,**kwargs):
        # if request.POST.get('update'):

        try: 
            name = request.POST.get('name')
            email = request.POST.get('email')
            subj = request.POST.get('subj')
            message = request.POST.get('message')
           
            print(name)
            add_message={
                'name':name,
                'email':email,
                'subj':subj,
                'message': message,
                
            }
            created = Contact.objects.create(**add_message)
            if created:
                  messages.success(request,'message envoye..')
            else:
                  messages.error(request , 'Sorry il ya un problem ..')
           
        except Exception as e:
               messages.error(request,f"Error ....{e}")
        
        return render(request, self.template_name)
     
class ListUserView(View):
    template_name="ListUser.html"
    users = User.objects.all()
    context = {'users': users}

    def get(self,request,*args,**kwargs):
        
        return render(request, self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        if request.POST.get('id_sup'):
         try:
          
           obj = User.objects.get(pk= request.POST.get('id_sup'))

           obj.delete()
           messages.success(request, ("La suppression a été effectuée avec succès."))   
           users = User.objects.all()
           self.context['users'] = users
           
         except User.DoesNotExist:
            messages.error(request, "User does not exist.")
     
         except Exception as e:
          messages.error(request, f"Sorry, error is : {e}.")
        return render(request, self.template_name,self.context)
class MessagesView(View):
     template_name="messages.html"
     messgs = Contact.objects.all()
     context = {'messgs': messgs}

     def get(self,request,*args,**kwargs):
        return render(request, self.template_name,self.context)
     
     def post(self,request,*args,**kwargs):
        if request.POST.get('id_sup'):
         try:
          
           obj = Contact.objects.get(pk= request.POST.get('id_sup'))

           obj.delete()
           messages.success(request, ("La suppression a été effectuée avec succès."))   
           messgs = Contact.objects.all()
           self.context['messgs'] = messgs
           
         except User.DoesNotExist:
            messages.error(request, "Le message n'existe pas.")
     
         except Exception as e:
          messages.error(request, f"Sorry, error is : {e}.")
        return render(request, self.template_name,self.context)
class aboutView(View):
     template_name="about.html"
     def get(self,request,*args,**kwargs):
        return render(request, self.template_name)