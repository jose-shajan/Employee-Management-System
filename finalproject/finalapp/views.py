from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect

from .models import EmployeeModel
from .forms import EmployeeForm

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def index(request):

    employees = EmployeeModel.objects.all()

    return render(request, 'dashboard.html', {'employees': employees})


def register(request):

    form = UserCreationForm()

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/login/')

    return render(request, 'register.html', {'form': form})


def user_login(request):

    form = AuthenticationForm()

    if request.method == "POST":

        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            next_url = request.GET.get('next')

            if next_url:
                return redirect(next_url)

            return redirect('/dashboard/')

    return render(request, 'login.html', {'form': form})


def user_logout(request):

    logout(request)

    return redirect('/login/')

@login_required()
def add_employee(request):

    form = EmployeeForm()

    if request.method == "POST":

        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            return redirect('/dashboard/')

    return render(request, 'add_employee.html', {'form': form})

def single_employee(request, id):

    employee = EmployeeModel.objects.get(id=id)

    return render(request, 'single_employee.html', {'employee': employee})


@login_required()
def update_employee(request, id):

    employee = EmployeeModel.objects.get(id=id)

    form = EmployeeForm(instance=employee)

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            request.FILES,
            instance=employee
        )

        if form.is_valid():

            form.save()

            return redirect('/dashboard/')

    return render(request, 'update_employee.html', {'form': form})

@login_required()
def delete_employee(request, id):

    employee = EmployeeModel.objects.get(id=id)

    employee.delete()

    return redirect('/dashboard/')