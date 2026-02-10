from django.shortcuts import render, redirect
from django.db.models import Count
from django.http import JsonResponse

from .models import Member, MemberDetail
from .forms import MemberDetailForm


# =====================================================
# 🔐 HELPER: GET LOGGED-IN MEMBER FROM SESSION
# =====================================================
def get_logged_in_member(request):
    member_no = request.session.get('member_no')
    if not member_no:
        return None
    try:
        return Member.objects.get(member_no=member_no)
    except Member.DoesNotExist:
        return None


# =====================================================
# 🔑 MEMBER LOGIN (SESSION-BASED)
# =====================================================
def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            member = Member.objects.get(username=username)

            if member.check_password(password):
                # ✅ SAVE MEMBER_NO IN SESSION
                request.session['member_no'] = member.member_no

                return JsonResponse({
                    'status': 'success',
                    'message': f'Welcome {member.username}'
                })

            return JsonResponse({
                'status': 'error',
                'message': 'Invalid password'
            })

        except Member.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Username not found'
            })

    return render(request, 'html_member/login.html')


# =====================================================
# 📊 DASHBOARD
# =====================================================
def dashboard(request):
    member = get_logged_in_member(request)
    if not member:
        return redirect('member:customer_login')

    members = (
        Member.objects
        .filter(member_no=member.member_no)
        .annotate(detail_count=Count('details'))
    )

    member_details = MemberDetail.objects.filter(member_no=member)

    context = {
        'member': member,
        'members': members,
        'member_details': member_details,
        'total_members': members.count(),
        'total_details': member_details.count(),
        'total_all': members.count() + member_details.count(),
    }

    return render(request, 'html_member/dashboard.html', context)


# =====================================================
# ➕ ADD MEMBER DETAIL (SESSION SAFE)
# =====================================================
def member_detail_add(request):
    member = get_logged_in_member(request)
    if not member:
        return redirect('member:customer_login')

    if request.method == 'POST':
        form = MemberDetailForm(request.POST)

        if form.is_valid():
            member_detail = form.save(commit=False)

            # ✅ AUTO ASSIGN MEMBER
            member_detail.member_no = member

            # ✅ AUDIT FROM SESSION
            member_detail.created_by = member
            member_detail.updated_by = member

            member_detail.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Member detail saved successfully'
            })

        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        })

    form = MemberDetailForm()
    return render(request, 'html_member/member_detail_add.html', {
        'form': form,
        'member': member
    })


# =====================================================
# 👤 PROFILE
# =====================================================
def profile(request):
    member = get_logged_in_member(request)
    if not member:
        return redirect('member:customer_login')

    return render(request, 'html_member/profile.html', {
        'member': member
    })


# =====================================================
# 📄 JSON PAGE
# =====================================================
def memberjson(request):
    return render(request, 'html_member/member.json')


# =====================================================
# 🚪 LOGOUT
# =====================================================
def logout_view(request):
    request.session.flush()
    return render(request , 'html_member/login.html')



