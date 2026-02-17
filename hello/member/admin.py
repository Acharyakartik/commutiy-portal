from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings

from member.models import City, Country, Member, MemberDetail, State


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country")
    list_filter = ("country",)
    search_fields = ("name", "country__name")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("country", "state")
    search_fields = ("name", "state__name", "country__name")
    list_per_page = 10


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ["member_no", "first_name", "middle_name", "surname", "email_id", "education", "username"]
    list_display = (
        "member_no",
        "first_name",
        "surname",
        "phone_no",
        "email_id",
        "approval_status",
        "status",
        "username",
        "country",
        "state",
        "city",
        "approved_by",
        "approved_at",
        "created_at",
    )
    list_filter = ("approval_status", "status", "gender", "country", "state")
    readonly_fields = ("approved_by", "approved_at", "created_at", "updated_at")
    actions = ["approve_selected", "mark_not_approved"]
    list_per_page = 10
    list_max_show_all = 200

    def _send_credentials_email(self, member, raw_password):
        if not member.email_id:
            return False

        subject = "Your Member Login Credentials"
        message = (
            f"Hello {member.first_name},\n\n"
            "Your account request has been approved.\n"
            f"Username: {member.username}\n"
            f"Password: {raw_password}\n\n"
            "Please login and change your password after first login."
        )

        try:
            sent = send_mail(
                subject,
                message,
                getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
                [member.email_id],
                fail_silently=False,
            )
            return sent > 0
        except Exception:
            return False

    @admin.action(description="Approve selected members and send credentials")
    def approve_selected(self, request, queryset):
        approved_count = 0
        email_count = 0
        for member in queryset:
            if member.approval_status == "Approved":
                continue
            raw_password = member.approve(approver=request.user)
            approved_count += 1
            if self._send_credentials_email(member, raw_password):
                email_count += 1

        self.message_user(
            request,
            f"Approved {approved_count} member(s). Credentials email sent to {email_count} member(s).",
        )

    @admin.action(description="Mark selected members as Not Approved")
    def mark_not_approved(self, request, queryset):
        count = 0
        for member in queryset:
            member.mark_not_approved(approver=request.user)
            count += 1
        self.message_user(request, f"Marked {count} member(s) as Not Approved.")

    class Media:
        css = {
            "all": ("admin_custom/news_changelist.css",)
        }


@admin.register(MemberDetail)
class MemberDetailAdmin(admin.ModelAdmin):
    list_display = (
        "member_id",
        "member_no",
        "first_name",
        "surname",
        "date_of_birth",
        "age",
        "gender",
        "occupation",
        "email_id",
        "marital_status",
        "education",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )
    list_filter = ("gender", "member_no")
    readonly_fields = (
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )
    search_fields = (
        "first_name",
        "surname",
        "email_id",
        "education",
        "member_no__member_no",
        "member_no__first_name",
        "member_no__surname",
    )
    raw_id_fields = ["member_no"]
    list_per_page = 10
    list_max_show_all = 200

    class Media:
        css = {
            "all": ("admin_custom/news_changelist.css",)
        }

