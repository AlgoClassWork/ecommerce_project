from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name='Изображение', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    stock = models.PositiveIntegerField(verbose_name='Остаток на складе')
    available = models.BooleanField(default=True , verbose_name='Доступен')

    def __str__(self):
        return self.name
    

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name='Товар')
    text = models.TextField(verbose_name='Отзыв')
    rating = models.IntegerField( 
        validators=(MinValueValidator(1), MaxValueValidator(5)),
        verbose_name='Оценка')

    def __str__(self):
        return f'Отзыв на {self.product.name}'
    

class Order(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    products = models.TextField(verbose_name='Состав заказа')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая стоимость')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')

    def __str__(self):
        return f'Заказ #{self.id}'