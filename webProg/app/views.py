from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .models import Book, User
from .forms import BookForm, UserForm


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('logform')
    form = UserForm()

    return render(request, 'register.html', {'form': form})


def authentificate(request):
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
    except:
        pass
    return redirect('logform')


def login(request, template_name='login.html'):
    username = 'not logged in'
    if request.method == 'POST':
        try:
            username = request.POST['login']
            password = request.POST['password']

            query = User.objects.filter(login__exact=username, password__exact=password)

            request.session['username'] = username
            request.session['role'] = query.get().role

            return redirect('index')
        except Exception as e:
            return redirect('logform')

    return redirect('logform')


def logform(request):
    return render(request, 'login.html')


class BookListView(ListView):
    model = Book
    paginate_by = 3
    context_object_name = 'book_list'
    template_name = 'index.html'

    def get(self, request):
        paginate_by = request.GET.get('paginate_by')
        data = self.model.objects.all()

        paginator = Paginator(data, paginate_by)
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
        return render(request, self.template_name,
                      {
                          'DataPaginated': paginated,
                          'paginate_by': paginate_by,
                          'role': role,
                          'isAuth': isAuthentificated,
                      })


def create(request):
    if authentificate(request) and (isUser(request.session['username']) or isAdmin(request.session['username'])):

        role = None
        isAuthentificated = 'username' in request.session
        if 'role' in request.session:
            role = request.session['role']

        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
        form = BookForm()

        return render(request, 'create.html', {'form': form, 'role': role,
                                               'isAuth': isAuthentificated})
    return redirect('logform')


def edit(request, pk, template_name='edit.html'):
    if authentificate(request) and isAdmin(request.session['username']):

        role = None
        isAuthentificated = 'username' in request.session
        if 'role' in request.session:
            role = request.session['role']

        book = get_object_or_404(Book, pk=pk)
        form = BookForm(request.POST or None, instance=book)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, template_name, {'form': form, 'role': role,
                                               'isAuth': isAuthentificated})
    return redirect('logform')


def delete(request, pk, template_name='delete.html'):
    if authentificate(request) and isAdmin(request.session['username']):

        role = None
        isAuthentificated = 'username' in request.session
        if 'role' in request.session:
            role = request.session['role']

        book = get_object_or_404(Book, pk=pk)
        if request.method == 'POST':
            book.delete()
            return redirect('index')
        return render(request, template_name, {'object': book, 'role': role,
                                               'isAuth': isAuthentificated})
    return redirect('logform')


"""def profile(request, pk, template_name='profile.html'):
    if authentificate(request) and (isUser(request.session['username']) or isAdmin(request.session['username'])):

        role = None
        isAuthentificated = 'username' in request.session
        if 'role' in request.session:
            role = request.session['role']

        user = get_object_or_404(User, pk=pk)
        form = UserForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, template_name, {'form': form, 'role': role,
                                               'isAuth': isAuthentificated})
    return redirect('logform')"""


def profile(request, template_name='profile.html'):
    if authentificate(request) and (isUser(request.session['username']) or isAdmin(request.session['username'])):

        role = None
        isAuthentificated = 'username' in request.session
        if 'role' in request.session:
            role = request.session['role']

        if request.method == 'POST':
            form = UserForm(instance=request.session['username'])

            if form.is_valid():
                form.save()
                return redirect('index')
            return render(request, template_name, {'form': form, 'role': role,
                                                   'isAuth': isAuthentificated})
    return redirect('logform')
