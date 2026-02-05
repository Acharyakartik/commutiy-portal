from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Contact
from django.shortcuts import redirect


# =========================
# CUSTOMER VIEWS (PORT 8000)
# NO LOGIN REQUIRED
# =========================
# api_view(['GET'])
def react_index(request):
    return render(request, "index.html")


def member(request):
    return render(request, "customer/login.html")
    return render(request, "index.html")


def home(request):
    return render(request, "home.html")


def aboutus(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            desc=request.POST.get("desc"),
            date=datetime.today()
        )
    return render(request, "contact.html")





