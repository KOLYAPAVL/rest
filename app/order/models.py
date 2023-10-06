from django.db import models
from django.utils.translation import gettext_lazy as l_
from model_utils import Choices

# Create your models here
class Order(models.Model):
    
    STATUS = Choices(
        (0, 'created', 'Создан'),
        (1, 'proccess', 'В работе'),
        (2, 'completed', 'Выполнен'),
        (3, 'canceled', 'Отменен'),
    )
    
    phone = models.CharField(
        l_('Номер телефона'),
        max_length=32,
    )
    name = models.CharField(
        l_('Имя покупателя'),
        max_length=128
    )
    created_at = models.DateTimeField(
        l_('Дата создания'),
        auto_now_add=True,
    )
    amount = models.FloatField(
        l_('Стоимость заказа'),
        default=0
    )
    promocode = models.ForeignKey(
        'promo.Promocode',
        on_delete=models.SET_NULL,
        verbose_name=l_('Промокод'),
        blank=True,
        null=True,
    )
    status = models.PositiveIntegerField(
        l_('Статус'),
        choices=STATUS,
        default=STATUS.created
    )
    
    class Meta:
        verbose_name = l_('Заказ')
        verbose_name_plural = l_('Заказы')
        
    def __str__(self):
        return str(self.id)
    
    def is_created(self):
        return self.status == self.STATUS.created
    
    def is_proccess(self):
        return self.status == self.STATUS.proccess
    
    @property
    def statuses(self):
        data = []
        if self.status == self.STATUS.canceled:
            return [{
                'active': True,
                'name': 'Отменен'
            }]
        for _ in self.STATUS:
            if _[0] != 3:
                if self.status >= _[0]:
                    data.append({
                        'active': True,
                        'name': _[1]
                    })
                else:
                    data.append({
                        'active': False,
                        'name': _[1]
                    })
        return data
        

class OrderItem(models.Model):
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name = l_('Заказ'),
        blank=False, null=False,
        related_name='items'
    )
    product = models.ForeignKey(
        'product.Product',
        on_delete=models.CASCADE,
        verbose_name = l_('Товар'),
        blank=False, null=False,
    )
    count = models.IntegerField(
        verbose_name=l_('Колличество'),
        default=1,
    )
    price = models.FloatField(
        verbose_name=l_('Цена'),
        default=0, null=False, blank=False
    )
    
    class Meta:
        verbose_name = l_('Позиция заказа')
        verbose_name_plural = l_('Позиции заказа')
    