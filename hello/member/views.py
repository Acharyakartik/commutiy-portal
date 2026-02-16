from django.shortcuts import render, redirect
from django.db.models import Count
from django.http import JsonResponse

from .models import Member, MemberDetail
from .forms import MemberDetailForm, MemberForm


def _abs_media_url(request, file_field):
    if not file_field:
        return None
    try:
        return request.build_absolute_uri(file_field.url)
    except Exception:
        return None


def _serialize_member(member, request):
    return {
        "member_no": member.member_no,
        "username": member.username,
        "first_name": member.first_name,
        "middle_name": member.middle_name,
        "surname": member.surname,
        "full_name": f"{member.first_name} {member.middle_name or ''} {member.surname}".strip(),
        "phone_no": member.phone_no,
        "email_id": member.email_id,
        "date_of_birth": member.date_of_birth.isoformat() if member.date_of_birth else None,
        "age": member.age,
        "gender": member.gender,
        "gender_label": member.get_gender_display(),
        "occupation": member.occupation,
        "marital_status": member.marital_status,
        "marital_status_label": member.get_marital_status_display() if member.marital_status else None,
        "education": member.education,
        "status": member.status,
        "profile_image_url": _abs_media_url(request, member.profile_image),
        "created_at": member.created_at.isoformat() if member.created_at else None,
        "updated_at": member.updated_at.isoformat() if member.updated_at else None,
    }


def _serialize_member_detail(detail, request):
    if not detail:
        return None
    return {
        "member_id": detail.member_id,
        "first_name": detail.first_name,
        "middle_name": detail.middle_name,
        "surname": detail.surname,
        "full_name": f"{detail.first_name} {detail.middle_name or ''} {detail.surname}".strip(),
        "email_id": detail.email_id,
        "date_of_birth": detail.date_of_birth.isoformat() if detail.date_of_birth else None,
        "age": detail.age,
        "gender": detail.gender,
        "gender_label": detail.get_gender_display(),
        "occupation": detail.occupation,
        "marital_status": detail.marital_status,
        "marital_status_label": detail.get_marital_status_display() if detail.marital_status else None,
        "education": detail.education,
        "profile_image_url": _abs_media_url(request, detail.profile_image),
        "created_at": detail.created_at.isoformat() if detail.created_at else None,
        "updated_at": detail.updated_at.isoformat() if detail.updated_at else None,
    }


def get_logged_in_member(request):
    member_no = request.session.get('member_no')
    if not member_no:
        return None
    try:
        return Member.objects.get(member_no=member_no)
    except Member.DoesNotExist:
        return None


def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            member = Member.objects.get(username=username)

            if member.check_password(password):
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


def member_detail_add(request):
    member = get_logged_in_member(request)
    if not member:
        return redirect('member:customer_login')

    if request.method == 'POST':
        form = MemberDetailForm(request.POST, request.FILES)

        if form.is_valid():
            member_detail = form.save(commit=False)
            member_detail.member_no = member
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


def member_edit(request):
    member = get_logged_in_member(request)
    if not member:
        return redirect('member:customer_login')

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = member.user if member.user else None
            obj.save()
            return redirect('member:profile')
    else:
        form = MemberForm(instance=member)

    return render(request, 'html_member/member_edit.html', {
        'form': form,
        'member': member,
    })


def member_detail_edit(request, member_id):
    member = get_logged_in_member(request)
    if not member:
        return redirect('member:customer_login')

    try:
        member_detail = MemberDetail.objects.get(member_id=member_id, member_no=member)
    except MemberDetail.DoesNotExist:
        return redirect('member:dashboard')

    if request.method == 'POST':
        form = MemberDetailForm(request.POST, request.FILES, instance=member_detail)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = member
            obj.save()
            return redirect('member:profile')
    else:
        form = MemberDetailForm(instance=member_detail)

    return render(request, 'html_member/member_detail_edit.html', {
        'form': form,
        'member': member,
        'member_detail': member_detail,
    })


def profile(request):
    member = get_logged_in_member(request)
    if not member:
        return redirect('member:customer_login')

    from news.models import News
    from marketplace.models import BnsModel

    member_details_qs = MemberDetail.objects.filter(member_no=member)
    latest_detail = member_details_qs.order_by('-created_at').first()
    latest_news = News.objects.filter(created_by=member).order_by('-created_at').first()
    latest_listing = BnsModel.objects.filter(created_by=member).order_by('-created_at').first()

    return render(request, 'html_member/profile.html', {
        'member': member,
        'detail_count': member_details_qs.count(),
        'news_count': News.objects.filter(created_by=member).count(),
        'listing_count': BnsModel.objects.filter(created_by=member).count(),
        'latest_detail': latest_detail,
        'latest_news': latest_news,
        'latest_listing': latest_listing,
    })


def profile_api(request):
    if request.method != 'GET':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    member = get_logged_in_member(request)
    if not member:
        return JsonResponse({'detail': 'Authentication required'}, status=401)

    from news.models import News
    from marketplace.models import BnsModel

    details_qs = MemberDetail.objects.filter(member_no=member).order_by('-created_at')
    latest_detail = details_qs.first()
    latest_news = News.objects.filter(created_by=member).order_by('-created_at').first()
    latest_listing = BnsModel.objects.filter(created_by=member).order_by('-created_at').first()

    response = {
        'member': _serialize_member(member, request),
        'counts': {
            'details': details_qs.count(),
            'news': News.objects.filter(created_by=member).count(),
            'listings': BnsModel.objects.filter(created_by=member).count(),
        },
        'latest_detail': _serialize_member_detail(latest_detail, request),
        'latest_news': {
            'id': latest_news.id,
            'title': latest_news.title,
            'slug': latest_news.slug,
            'status': latest_news.status,
            'status_label': latest_news.get_status_display(),
            'category': latest_news.category.name if latest_news.category else None,
            'created_at': latest_news.created_at.isoformat() if latest_news.created_at else None,
        } if latest_news else None,
        'latest_listing': {
            'id': latest_listing.id,
            'title': latest_listing.title,
            'slug': latest_listing.slug,
            'status': latest_listing.status,
            'status_label': latest_listing.get_status_display(),
            'listing_type': latest_listing.listing_type,
            'listing_type_label': latest_listing.get_listing_type_display(),
            'price': latest_listing.price,
            'created_at': latest_listing.created_at.isoformat() if latest_listing.created_at else None,
            'image_url': _abs_media_url(request, latest_listing.image),
        } if latest_listing else None,
    }
    return JsonResponse(response)


def memberjson(request):
    return render(request, 'html_member/member.json')


def logout_view(request):
    request.session.flush()
    return render(request, 'html_member/login.html')
