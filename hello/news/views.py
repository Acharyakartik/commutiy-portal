from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import News
from member.models import Member


# =====================================================
# 🔐 HELPER: GET LOGGED-IN MEMBER
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
# 📰 NEWS LIST (SESSION BASED)
# =====================================================
def news_list(request):
    member = get_logged_in_member(request)
    if not member:
        return redirect('member:customer_login')

    published_news = News.objects.filter(
        status="published",
        created_by=member
    )
    unpublished_news = News.objects.exclude(
        status="published"
    ).filter(created_by=member)

    return render(request, "html_member/news_list.html", {
        "published_news": published_news,
        "unpublished_news": unpublished_news,
    })


# =====================================================
# ➕✏️ ADD + EDIT NEWS (SESSION BASED)
# =====================================================
def news_form(request, pk=None):
    member = get_logged_in_member(request)
    if not member:
        return redirect('member:customer_login')

    news = get_object_or_404(News, pk=pk) if pk else None

    # 🔐 ownership check
    if news and news.created_by != member:
        return redirect("news:news_list")

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        # category_id = request.POST.get("category")
        status = request.POST.get("status")
        image = request.FILES.get("image")

        if news:
            # UPDATE
            news.title = title
            news.content = content
            # news.category_id = category_id
            news.status = status
            news.updated_by = member

            if image:
                news.image = image

            if status == "published" and not news.published_at:
                news.published_at = timezone.now()
            elif status != "published":
                news.published_at = None

            news.save()

        else:
            # CREATE
            News.objects.create(
                title=title,
                content=content,
                # category_id=category_id,
                status=status,
                image=image,
                created_by=member,
                updated_by=member,
                published_at=timezone.now() if status == "published" else None,
            )

        return redirect("news:news_list")

    # categories = Category.objects.filter(is_active=True)

    return render(request, "html_member/news_form.html", {
        "news": news,
        # "categories": categories,
        "status_choices": News.STATUS_CHOICES,
    })


# =====================================================
# 🗑 DELETE NEWS (SESSION BASED)
# =====================================================
def news_delete(request, pk):
    member = get_logged_in_member(request)
    if not member:
        return redirect('member:login')

    news = get_object_or_404(News, pk=pk)

    if news.created_by != member:
        return redirect("news:news_list")

    news.delete()
    return redirect("news:news_list")
