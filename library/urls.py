from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('books/', list_books, name="list_books"),
    path("books_detail/<int:pk>/", BookDetail.as_view(), name="book_detail"),
    path('', home, name='home'),
    path('login/', login_view, name='login_view'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:book_id>', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:book_id>', remove_item, name='remove_item'),
    path('reduce_item/<int:book_id>', reduce_item, name='reduce_item'),
    path('add_more_books/<int:book_id>', add_more_books, name='add_more_books'),
    path('blogs/', blog, name='blogs'),
    path('more/', author, name='more'),
    path('author_books/<int:author_id>/books/', author_books, name='author_books'),
    path('profile/', profile_view, name='profile_view'),
    path('profile/update/', profile_update, name='profile_update'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('restore_password/', restore_password, name='restore_password')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
