from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from django.contrib.auth.hashers import check_password
from .models import Book, User, Order, CartItem
from .forms import BookForm, UserForm, OrderForm, CartItemForm


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('logform')
    form = UserForm()
    return render(request, 'register.html', {'form': form})


def check_login(request):
    login = request.POST.get('login')
    val = False
    if (authentificated(request)):
        val = (not (login == request.session['username'])) and (User.objects.filter(login__exact=login).exists())
    else:
        val = User.objects.filter(login__exact=login).exists()
    data = {'login_exists': val}
    return JsonResponse(data)


def check_email(request):
    email = request.POST.get('email')
    data = {'email_correct': False}
    try:
        validate_email(email)
        data['email_correct'] = True
    except:
        pass
    return JsonResponse(data)


def check_passwordlen(request):
    password = request.POST.get('password')
    data = {'password_correct': False}
    if len(password) >= 6:
        data['password_correct'] = True
    return JsonResponse(data)


def authentificated(request):
    return 'username' in request.session


def getrole(username):
    try:
        return User.objects.filter(login__exact=username).get().role
    except:
        return 'undefined'


def isUser(username):
    return getrole(username) == 'user'


def isAdmin(username):
    return getrole(username) == 'admin'


def logout(request):
    try:
        del request.session['username']
        del request.session['role']
        del request.session['id']
    except:
        pass
    return redirect('logform')


def login(request, template_name='login.html'):
    username = 'not logged in'
    if request.method == 'POST':
        try:
            username = request.POST['login']
            password = request.POST['password']

            query = User.objects.filter(login__exact=username)
            print(query.get().password)
            print("is: " + str(check_password(password, query.get().password)))
            print("ad")
            if check_password(password, query.get().password):
                print("here")
                request.session['username'] = username
                request.session['role'] = query.get().role
                request.session['id'] = query.get().id
                return redirect('index')

        except Exception as e:
            print(e)
            return redirect('logform')
    return redirect('logform')


def logform(request):
    return render(request, 'login.html')


class BookListView(ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'book_list'
    template_name = 'index.html'

    def get(self, request):
        paginate_by = request.GET.get('paginate_by', 10) or 10
        sort_by = request.GET.get('sort_by', 'name') or 'name'
        ordered_data = self.model.objects.order_by(sort_by)

        paginator = Paginator(ordered_data, paginate_by)
        page = request.GET.get('page')

        role = None
        isAuthentificated = 'username' in request.session
        if 'role' in request.session:
            role = request.session['role']

        try:
            paginated = paginator.get_page(page)
        except PageNotAnInteger:
            paginated = paginator.get_page(1)
        except EmptyPage:
            paginated = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {
            'DataPaginated': paginated,
            'paginate_by': paginate_by,
            'role': role,
            'isAuth': isAuthentificated,
        })


def create(request):
    if (authentificated(request) and
            (isUser(request.session['username']) or
             isAdmin(request.session['username']))):

        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
        form = BookForm()
        return render(request, 'create.html', {'form': form})
    return redirect('logform')


def edit(request, pk, template_name='edit.html'):
    if authentificated(request) and isAdmin(request.session['username']):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(request.POST or None, instance=book)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, template_name, {'form': form})
    return redirect('logform')


def delete(request, pk, template_name='delete.html'):
    if authentificated(request) and isAdmin(request.session['username']):
        book = get_object_or_404(Book, pk=pk)
        if request.method == 'POST':
            book.delete()
            return redirect('index')
        return render(request, template_name, {'object': book})
    return redirect('logform')


def cart(request, template_name='cart.html'):
    if authentificated(request):
        ids = []
        price = 0
        cart_items = CartItem.objects.filter(user_id__exact=request.session['id'])

        if request.method == 'POST':
            last_id = 0
            try:
                last_id = Order.objects.latest('id').id
            except:
                pass

            for item in cart_items:
                book = Book.objects.get(pk=item.book_id)
                price = price + float(book.price) * item.amount

            for item in cart_items:
                book = Book.objects.get(pk=item.book_id)
                ids.append(item.id)
                Order.objects.create(
                    order_number=last_id,
                    book_id=item.book_id,
                    user_id=request.session['id'],
                    amount=item.amount,
                    price=price
                )
            CartItem.objects.filter(id__in=ids).delete()
            return render(request, 'buy.html')

        for item in cart_items:
            book = Book.objects.get(pk=item.book_id)
            ids.append(book.id)
            price = price + float(book.price) * item.amount

        cb_list = zip(
            CartItem.objects.filter(user_id__exact=request.session['id']),
            Book.objects.filter(id__in=ids)
        )

        return render(request, template_name, {
            'list': cb_list,
            'price': price,
            'cart_len': len(cart_items)
        })
    return redirect('logform')


def add_to_cart(request, pk, template_name='order.html'):
    if authentificated(request):
        book = get_object_or_404(Book, pk=pk)
        if request.method == 'POST':
            amount = request.POST['amount']
            try:
                item = CartItem.objects.filter(
                    book_id__exact=book.id, user_id__exact=request.session['id']
                )
                CartItem.objects.filter(pk=item[0].id).update(
                    amount=item[0].amount + int(amount)
                )
            except:
                CartItem.objects.create(
                    amount=int(amount), book_id=book.id, user_id=request.session['id']
                )

            Book.objects.filter(pk=book.id).update(
                amount=(int(book.amount) - int(amount))
            )
            return redirect('index')
        return render(request, template_name, {'book': book})
    return redirect('logform')


def edit_user(request, template_name='edit_user.html'):
    if authentificated(request):
        user = get_object_or_404(User, pk=request.session['id'])
        user.password = ''
        form = UserForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, template_name, {'form': form})
    return redirect('index')


def orders(request, template_name='order_list.html'):
    if authentificated(request):
        user_orders = Order.objects.filter(user_id__exact=request.session['id'])
        orders = []
        if len(user_orders) > 0:
            order_dict = {}
            books = []
            order_id = user_orders[0].order_number
            for order in user_orders:
                book = {}
                if order_id == order.order_number:
                    book_inst = Book.objects.get(pk=order.book_id)
                    book['name'] = book_inst.name
                    book['amount'] = order.amount
                    books.append(book)
                else:
                    order_dict['id'] = order_id
                    order_dict['price'] = order.price
                    order_dict['books'] = books
                    orders.append(order_dict)
                    order_dict = {}
                    books = []
                    book = {}

                    book_inst = Book.objects.get(pk=order.book_id)
                    book['name'] = book_inst.name
                    book['amount'] = order.amount
                    books.append(book)

                    order_id = order.order_number
            if len(book) > 0:
                order_dict['id'] = order_id
                order_dict['price'] = order.price
                order_dict['books'] = books
                orders.append(order_dict)

        return render(request, template_name, {'orders': orders})
    return redirect('index')
