from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Member
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from .forms import MemberDetailForm
from .models import Member, MemberDetail
from django.contrib import messages
from django.http import JsonResponse

def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Member.objects.get(username=username)

            if user.check_password(password):
                # Save the correct primary key in session
                request.session['member_no'] = user.member_no

                # AJAX response
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success', 'message': f"Welcome {user.username}!"})

                # Normal redirect
                messages.success(request, f"Welcome {user.username}!")
                return redirect('member:dashboard')

            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': "Invalid password"})
                messages.error(request, "Invalid password")

        except Member.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': "Username not found"})
            messages.error(request, "Username not found")

    return render(request, 'html_member/login.html')



def dashboard(request):
    # 🔐 Get logged-in member_no from session
    member_no = request.session.get('member_no')

    if not member_no:
        # Session expired or user not logged in
        return redirect('member:login')  # replace with your login URL name

    try:
        # 👤 Fetch logged-in member
        member = Member.objects.get(member_no=member_no)
    except Member.DoesNotExist:
        # Somehow session has invalid member_no
        return render(request, 'member/dashboard.html', {
            'message': 'No Member record exists for your login. Contact admin.'
        })

    # 📊 Member summary with count of details
    members = (
        Member.objects
        .filter(member_no=member_no)
        .annotate(detail_count=Count('details'))
    )

    # 📄 Fetch member details linked to member_no
    member_details = MemberDetail.objects.filter(member_no=member)

    context = {
        'members': members,
        'member_details': member_details,
        'total_members': members.count(),
        'total_details': member_details.count(),
        'total_all': members.count()  + member_details.count(),
    }

    return render(request, 'html_member/dashboard.html', context)



def member_detail_add(request):
    # Get logged-in member using session
    member_no = request.session.get('member_no')
    if not member_no:
        return redirect('member:customer_login')  # user not logged in

    try:
        member_instance = Member.objects.get(member_no=member_no)
    except Member.DoesNotExist:
        # Should rarely happen, but just in case
        return redirect('member:login')

    if request.method == 'POST':
        form = MemberDetailForm(request.POST)
        if form.is_valid():
            member_detail = form.save(commit=False)

            # Auto-assign the logged-in member
            member_detail.member_no = member_instance

            # Auto-fill names from Member
            # Set audit fields
            member_detail.created_by = request.user
            member_detail.updated_by = request.user

            # Save the record
            member_detail.save()

            # AJAX response
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Member detail saved successfully!'
                })

            # Normal redirect after save
            return redirect('dashboard')
        else:
            # Form invalid - handle AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                })

    else:
        # GET request
        form = MemberDetailForm()

    return render(request, 'html_member/member_detail_add.html', {
        'form': form,
        'member': member_instance
    })


def profile(request):
    return render(request, 'html_member/profile.html')


def logout_view(request):
    request.session.flush()
    return redirect('html_member/login/')

   
