from django.contrib import admin, messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse
from member.models import City, Country, Member, MemberDetail, MemberPasswordResetToken, State


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

    def _build_reset_link(self, token):
        path = reverse("member:reset_password_with_token", args=[token])
        base_url = getattr(settings, "SITE_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
        return f"{base_url}{path}"

    def _send_credentials_email(self, member, reset_link):
        if not member.email_id:
            return False, "Member email not available"

        subject = "Your Account Is Approved - Set Your Password"
        message = (
            f"Hello {member.first_name},\n\n"
            "Your account request has been approved.\n"
            f"Username: {member.username}\n"
            "For security, password is not sent in email.\n"
            "Use this one-time link to set your password:\n"
            f"{reset_link}\n\n"
            "This link will expire and can be used only once."
        )

        try:
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [member.email_id],
                reply_to=[settings.REPLY_TO_EMAIL],
            )
            sent = email.send(fail_silently=False)
            if sent > 0:
                return True, None
            return False, "Email backend returned 0 sent emails"
        except Exception as exc:
            return False, f"{exc.__class__.__name__}: {exc}"

    def _approve_and_notify(self, member, approver):
        member.approve(approver=approver)
        ttl_minutes = int(getattr(settings, "PASSWORD_RESET_TOKEN_MINUTES", 30))
        token_obj = MemberPasswordResetToken.create_for_member(member, ttl_minutes=ttl_minutes)
        reset_link = self._build_reset_link(token_obj.token)
        sent, err = self._send_credentials_email(member, reset_link)
        return {
            "username": member.username,
            "set_password_link": reset_link,
            "email_sent": sent,
            "email_error": err,
        }

    @admin.action(description="Approve selected members and send credentials")
    def approve_selected(self, request, queryset):
        approved_count = 0
        email_count = 0
        email_errors = []
        for member in queryset:
            if member.approval_status == "Approved":
                continue
            result = self._approve_and_notify(member, request.user)
            approved_count += 1
            if result["email_sent"]:
                email_count += 1
            elif result["email_error"]:
                email_errors.append(
                    f"Member {member.member_no} ({member.email_id}): {result['email_error']}"
                )

        self.message_user(
            request,
            f"Approved {approved_count} member(s). Credentials email sent to {email_count} member(s).",
        )
        if email_errors:
            for err in email_errors[:5]:
                self.message_user(request, err, level=messages.ERROR)

    @admin.action(description="Mark selected members as Not Approved")
    def mark_not_approved(self, request, queryset):
        count = 0
        for member in queryset:
            member.mark_not_approved(approver=request.user)
            count += 1
        self.message_user(request, f"Marked {count} member(s) as Not Approved.")

    def save_model(self, request, obj, form, change):
        # If superadmin changes approval to Approved from change form,
        # generate credentials, save to DB, and send email immediately.
        if change and obj.pk:
            previous = Member.objects.filter(pk=obj.pk).values("approval_status").first()
            previous_status = previous["approval_status"] if previous else None
            if previous_status != "Approved" and obj.approval_status == "Approved":
                result = self._approve_and_notify(obj, request.user)
                self.message_user(
                    request,
                    (
                        "Member approved. "
                        f"Username: {result['username']} | "
                        f"Set Password Link: {result['set_password_link']}"
                    ),
                    level=messages.SUCCESS,
                )
                if not result["email_sent"] and result["email_error"]:
                    self.message_user(
                        request,
                        f"Credentials email failed: {result['email_error']}",
                        level=messages.ERROR,
                    )
                return

        super().save_model(request, obj, form, change)

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
