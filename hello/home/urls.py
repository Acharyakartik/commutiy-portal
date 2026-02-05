from django.urls import path
from home import views
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Contact

app_name = "home"
urlpatterns = [
    # ======================
    # CUSTOMER (NO LOGIN)
    # ======================
     path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('aboutus/', views.aboutus, name='about'),
    
    path('contact/', views.contact, name='contact'),
    

    


    # ======================
    # ADMIN (CUSTOM DASHBOARD)
    # ======================
    # path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]


# ======================
# CUSTOMER (NO LOGIN)
# ======================

def index(request):
    return render(request, "customer/index.html")


def home(request):
    return render(request, "customer/home.html")


def aboutus(request):
    return render(request, "customer/about.html")


def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            desc=request.POST.get("desc"),
            date=datetime.today()
        )
    return render(request, "customer/contact.html")


# ======================
# CLIENT (LOGIN REQUIRED)
# ======================

@login_required(login_url='/client/login/')
def client_dashboard(request):
    if not request.user.groups.filter(name='Client').exists():
        return render(request, "client/dashboard.html")
