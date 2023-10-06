from django.shortcuts import render
from django.views.generic import View
from product.models import Product
from order.models import Order, OrderItem
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.http import (
    JsonResponse, HttpResponseRedirect,
    HttpResponseNotFound
)
from promo.models import Promocode
from django.views.generic.list import ListView

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class Cart(View):
    template_name = 'order/cart.html'

    def get(self, request):
        return render(request, self.template_name, {
            'page': 'cart'
        })

    @csrf_exempt
    def post(self, request):
        if request.POST.get('action'):
            promocode = request.POST.get('promo')
            if promocode:
                promocode = Promocode.objects.filter(code=promocode).first()
            else:
                promocode = None
                
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            
            total = 0
            products = []
            for key in request.POST:
                if not key == 'promo':
                    id = key.replace('product_', '')
                    if id.isnumeric():
                        id = int(id)
                        count = int(request.POST[key])
                        product = Product.objects.filter(id=id).first()
                        if product:
                            total += product.price * count
                            products.append({'product': product, 'count': count})
            
            o = Order.objects.create(
                name=name,
                phone=phone,
                amount=total-(
                    (promocode.discount / 100)*total if promocode else 0
                ),
                promocode=promocode,
            )
            for product in products:
                OrderItem.objects.create(
                    product=product['product'],
                    count=product['count'],
                    order=o,
                    price=product['product'].price,
                )
                
            return HttpResponseRedirect('/order/{}'.format(o.id))
                    
        data = json.loads(request.body)
        if 'action' in data:
            if data['action'] == 'promo':
                return JsonResponse({
                    'success': Promocode.objects.filter(code=data.get('code')).exists()
                })
        
        promo = Promocode.objects.filter(code=data.get('promocode')).first()
        items = data.get('items')
        context = []
        total = 0
        for item in items:
            product = Product.objects.filter(id=item.get('id')).first()
            if product:
                count = int(item['count'])
                price = product.price * count
                context.append({
                    'product': product,
                    'count': count,
                    'price': price,
                })
                total += price

        discount_amount = total * (promo.discount / 100) if promo else 0
        total_with_discount = total - discount_amount
                
        return render(request, 'order/cart_detail.html', {
            'items': context,
            'total': total,
            'promo': promo,
            'discount_amount': discount_amount,
            'total_with_discount': total_with_discount
        })


class OrderDetail(View):
    
    def get(self, request, pk):
        o = Order.objects.filter(pk=pk).first()
        if not o:
            return HttpResponseNotFound('Заказ не найден')
        
        return render(request, 'order/order.html', {
            'object': o,
        })


@method_decorator(csrf_exempt, name='dispatch')
class Orders(ListView):
    model = Order
    template_name = 'order/orders.html'
    
    def get_queryset(self, *args, **kwargs):
        return self.model.objects.all().exclude(
            status__in=[
                Order.STATUS.completed,
                Order.STATUS.canceled,
            ],
        ).order_by('-id')
        
    def post(self, request):
        data = json.loads(request.body)
        object = self.model.objects.filter(id=data['id']).first()
        if not object:
            return JsonResponse({
                'success': False
            })
        if data['action'] == 'PROCCESS':
            object.status = Order.STATUS.proccess
            object.save()
            return JsonResponse({
                'success': True
            })
        elif data['action'] == 'COMPLETE':
            object.status = Order.STATUS.completed
            object.save()
            return JsonResponse({
                'success': True
            })
        elif data['action'] == 'CANCEL':
            object.status = Order.STATUS.canceled
            object.save()
            return JsonResponse({
                'success': True
            })
        if not object:
            return JsonResponse({
                'success': False
            })
            