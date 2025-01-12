from django.shortcuts import render,redirect
from django.views import View
from .models import MenuItem,Category,OrderModel
from django.core.mail import send_mail
class Index(View):
    def get(self,request,*args, **kwargs):
        return render(request,'LB/index.html')
class Order(View):
    def get(self,request,*args,**kwargs):
        starters=MenuItem.objects.filter(category__name__contains='Starters')
        main_course=MenuItem.objects.filter(category__name__contains='Main Course')
        beverages=MenuItem.objects.filter(category__name__contains='Beverages')
        desserts=MenuItem.objects.filter(category__name__contains='Desserts')
        context={
            'starters':starters,
            'main_course':main_course,
            'desserts':desserts,
            'beverages':beverages
        }
        return render(request,'LB/order.html',context)
    def post(self,request,*args,**kwargs):
        name=request.POST.get('name')
        email=request.POST.get('email')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zip_code=request.POST.get('zip_code')

        order_items={
            'items': []
        }
        items=request.POST.getlist('items[]')
        for item in items:
            menu_item=MenuItem.objects.get(pk__contains=int(item))
            item_data={
                'id':menu_item.pk,
                'name':menu_item.name,
                'price':menu_item.price
            }
            order_items['items'].append(item_data)
        price=0
        item_ids=[]
        for item in order_items['items']:
            price+=item['price']
            item_ids.append(item['id'])
        order=OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,              
            
        )
        order.items.add(*item_ids)
        body=('Thank you for you order! Your food is being made and will be deliverd soon\n'
              f'Your total:{price}\n'
              'Enjoy your food')
        send_mail(
            "Thank you for your order!",
            body,
            'noreply@lunchbox.com',
            [email],
            fail_silently=False
        )
        context={
            'items':order_items['items'],
            'price':price
        }
        return redirect('order-confirmation',pk=order.pk)
class OrderConfirmation(View):
    def get(self,request,pk,*args,**kwargs):
        order=OrderModel.objects.get(pk=pk)
        context={
            'pk':order.pk,
            'items':order.items,
            'price':order.price,
        }
        return render(request,'LB/order_confirmation.html',context)
    def post(self,request,pk,*args, **kwargs):
        print(request.body)

class OrderPayConfirmation(View):
    def get(self,request,*args, **kwargs):
        return render(request,'LB/order_pay_confirmation.html')