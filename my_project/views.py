from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegister, RecipeForm
from .models import User, Recipe
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.


def base(request):
    return render(request, 'base.html')


def main(request):
    return render(request, 'main.html')


def sign_up(request):
    User.objects.all()  # получаем данные из БД
    if 'register' in request.POST:  # проверка какая кнопка была нажата
        form = UserRegister(request.POST)
        login_form = AuthenticationForm()  # создаем форму с данными
        if form.is_valid():  # проверка на правильность заполнения формы
            form.save()
            # username = form.cleaned_data['username']  # form.cleaned_data словарь, содержащий очищенные данные
            # password = form.cleaned_data['password1']
            # password2 = form.cleaned_data['password2']
            # email = form.cleaned_data['email']
            # age = form.cleaned_data['age']
            # if User.objects.filter(username=username).exists():
            #     form.add_error('username', 'Пользователь с таким именем уже существует')
            # elif password != password2:
            #     form.add_error('repeat_password', 'Пароли не совпадают')
            # else:
            #     user = User.objects.create(username=username, age=age, email=email,
            #                                password=password)  # сохраняем нового пользователя в базу данных
            #     user = authenticate(username=username, password=password)  # выполняем аутентификацию
            #     if user:
            user = form.save()
            login(request, user)  # autologging после регистрации пользователя
            return redirect('/main')  # Перенаправляет на главную страницу после регистрации
    elif 'login' in request.POST:
        form = UserRegister()
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('/main')
        else:
            login_form.add_error(None, 'Неверные логин или пароль')
    else:
        login_form = AuthenticationForm()
        form = UserRegister()  # если метод запроса не 'POST', то создаем пустую форму снова
    return render(request, 'login.html', {'form': form, 'login_form': login_form})


def log_out(request):
    logout(request)
    return redirect('/login')


def add_recipe(request):
    if request.method == "POST":  # проверка запроса на GET или POST
        form = RecipeForm(request.POST, request.FILES)  # создаем форму с данными
        if form.is_valid():  # проверка на правильность заполнения формы
            title = form.cleaned_data['title']  # form.cleaned_data словарь, содержащий очищенные данные
            description = form.cleaned_data['description']
            ingredients = form.cleaned_data['ingredients']
            instructions = form.cleaned_data['instructions']
            image = form.cleaned_data['image']
            recipe = Recipe(title=title, description=description, instructions=instructions, ingredients=ingredients,
                            image=image, user=request.user)
            recipe.save()
            return redirect('/lenta')

    else:
        form = RecipeForm()
    return render(request, 'add_recipe.html', {'form': form})


def lenta(request):
    recipes = Recipe.objects.all().order_by('created_at')
    recipes_on_page = request.GET.get('recipes_on_page', 3)  # делаем запрос на количество элементов на странице,
    # по умолчанию 3
    try:
        recipes_on_page = int(recipes_on_page)
        if recipes_on_page <= 0:
            recipes_on_page = 3
    except ValueError:
        recipes_on_page = 3

    # создаем пагинатор
    paginator = Paginator(recipes, recipes_on_page)  # указываем что будем размещать и количество

    page_number = request.GET.get('page')  # получаем номер страницы, на которую переходит пользователь

    page_obj = paginator.get_page(page_number)  # получаем посты для текущей страницы

    return render(request, 'lenta.html', {'page_obj': page_obj, 'recipes_on_page': recipes_on_page})


@login_required
def add_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user in recipe.favorites.all():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)
    return redirect('/lenta')


@login_required
def remove_favorites(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.favorites.remove(user)
    return redirect('/selected')


@login_required
def selected(request):
    user = request.user
    selected_recipe = Recipe.objects.filter(favorites=user)
    return render(request, 'selected.html', {'selected_recipe': selected_recipe})
