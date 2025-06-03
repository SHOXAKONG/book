from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ChoiceField(models.TextChoices):
    HORROR = 'horror', 'Horror'
    DRAMA = 'drama', 'Drama'
    DETECTIVE = 'detective', 'Detective'
    THRILLER = 'thriller', 'Thriller'
    HISTORICAL = 'historical', 'Historical'
    FANTASY = 'fantasy', 'Fantasy'
    NOVEL = 'novel', 'Novel'

class Author(models.Model):
    author_image = models.ImageField(upload_to='author_image/')
    fullname = models.CharField(max_length=200)
    about = models.TextField(null=True, blank=True)
    date_birth = models.DateField()

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.fullname

class Book(models.Model):
    cover_image = models.ImageField(upload_to='book_covers/')
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)  # Increased max_digits for flexibility
    count = models.PositiveIntegerField(default=1)  # Ensuring non-negative count
    genre = models.CharField(choices=ChoiceField.choices, max_length=20)  # Added max_length
    about = models.TextField()
    add_to_cart = models.BooleanField(default=False)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return f"{self.title} by {self.author.fullname}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    took_date = models.DateField(default=timezone.now)
    book_count = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart'

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.book.title}"

    def total_price(self):
        return self.book.price * self.book_count

class Status(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'

class OrderDetail(models.Model):
    quantity_sold = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    order_date = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, max_length=20)

    class Meta:
        db_table = 'order_details'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_details = models.ManyToManyField(OrderDetail)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=30)
    about = models.TextField()
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/')

    class Meta:
        db_table = 'blog'
        ordering = ['-id']

    def __str__(self):
        return self.title

def time_default():
    return timezone.now() + timedelta(minutes=10)

class Code(models.Model):
    code_number = models.CharField(max_length=200)
    user = models.ForeignKey(User, models.CASCADE, related_name='code_user')
    expired_data = models.DateTimeField(default=time_default)