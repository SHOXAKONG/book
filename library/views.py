from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from .models import *
from .forms import LoginForm, RegistrationForm, ProfileForm, ForgotPasswordForm, RestorePassword
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from .service import send_html_email, send_email_in_thread


class BookDetail(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    context_object_name = 'book'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'book/book_detail.html'
    context_object_name = 'author'


def author(request):
    author = Author.objects.all()
    return render(request, 'authors/more.html', {
        "more": author
    })


def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'blogs/blogs.html', {
        "blogs": blogs
    })


def list_books(request):
    search = request.GET.get("search", "")
    filter_ = request.GET.get("order", "-id")

    books = Book.objects.all()

    if search:
        books = books.filter(
            Q(title__icontains=search)
        )
    books = books.order_by(filter_)

    return render(request, "book/books.html", {
        "books": books,
        "search": search,
        "filter_": filter_,
    })


# def create_book(request):
#     if request.method == 'GET':
#         form = BookForm()
#     else:
#         form = BookForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             book = Book.objects.create(
#                 title=data['title'],
#                 author=data['author'],
#                 count=data['count']
#             )
#             return redirect('books')
#
#     return render(request, 'book/book-create.html', {
#         "form": form,
#     })


def home(request):
    return render(request, 'main/home.html', )


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            messages.error(request, 'Username or Password is incorrect')
        return render(request, 'login/login.html', {
            "form": form
        })
    form = LoginForm()
    return render(request, 'login/login.html', {
        "form": form
    })


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_view')
        return render(request, 'login/register.html', {
            "form": form
        })
    form = RegistrationForm()
    return render(request, 'login/register.html', {
        "form": form
    })


def logout_view(request):
    logout(request)
    return redirect('login_view')


@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user_id=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    return render(request, 'cart/cart.html', {
        "cart_items": cart_items,
        "total_price": total_price
    })


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_id = request.user
    cart_item, created = Cart.objects.get_or_create(user=user_id, book=book)
    if not created:
        cart_item.book_count += 1
        cart_item.save()

    return redirect('list_books')


@login_required
def remove_item(request, book_id):
    cart_item = get_object_or_404(Cart, book_id=book_id, user_id=request.user)
    cart_item.delete()

    return redirect('cart_detail')


@login_required
def reduce_item(request, book_id):
    cart_item = get_object_or_404(Cart, book_id=book_id, user=request.user)
    if cart_item.book_count > 1:
        cart_item.book_count -= 1
        cart_item.save()
        return redirect('cart_detail')
    cart_item.delete()
    return redirect('cart_detail')


@login_required
def add_more_books(request, book_id):
    cart_item = get_object_or_404(Cart, book_id=book_id, user=request.user)
    book = get_object_or_404(Book, id=book_id)
    try:
        if cart_item.book_count + 1 > book.count:
            return redirect('cart_detail')
        cart_item.book_count += 1
        cart_item.save()
        return redirect('cart_detail')
    except ValidationError:
        messages.error(request, 'Not enough in stock')


def author_books(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = Book.objects.filter(author_id=author_id)
    return render(request, 'book/author_books.html', {
        "author": author,
        "book": books
    })


@login_required
def profile_view(request):
    user = get_user(request)
    return render(request, 'users/profile.html', {
        "user": user
    })

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            change_password = form.cleaned_data.get('change_password')
            if change_password:
                user.set_password(change_password)
                update_session_auth_hash(request, user)
            user.save()
            return redirect('profile_view')
    form = ProfileForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                send_email_in_thread(user.email, user)
                return render(request, 'reset_password/password_reset_confirm.html')
            form.add_error('email', 'User not found')  # Optional error handling
        return render(request, 'reset_password/reset_password.html', {"form": form})
    form = ForgotPasswordForm()
    return render(request, 'reset_password/reset_password.html', {"form": form})


def restore_password(request):
    if request.method == 'POST':
        form = RestorePassword(request.POST)
        if form.is_valid():
            form.update()
            return render(request, 'reset_password/password_reset_complete.html', {"form" : form})
        return render(request, 'reset_password/password_reset_email.html', {"form" : form })
    form = RestorePassword()
    return render(request, 'reset_password/password_reset_email.html', {"form": form})