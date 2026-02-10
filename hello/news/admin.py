from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import News

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ("name", "is_active", "created_at")
#     prepopulated_fields = {"slug": ("name",)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin): # Rename class to NewsAdmin to avoid conflict with model name
    list_display = (
        "title",
        # "category",
        "status",
        "created_by",
        "created_at",
        "action_buttons",
    )

    list_filter = (
        "status",
        # "category",
    )

    search_fields = ("title", "content")
    ordering = ("-created_at",)

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")

    def action_buttons(self, obj):
        edit_url = reverse("admin:news_news_change", args=[obj.id])
        delete_url = reverse("admin:news_news_delete", args=[obj.id])

        return format_html(
            '''
            <a class="button" style="padding:2px 5px; background:#447e9b; color:white; border-radius:4px;" href="{}">Edit</a>
            <a class="button" style="padding:2px 5px; background:#ba2121; color:white; border-radius:4px;" href="{}">Delete</a>
            ''',
            edit_url,
            delete_url
        )

    action_buttons.short_description = "Actions"
    
def save_model(self, request, obj, form, change):
        try:
            member_profile = request.user.member
            if not obj.pk:
                obj.created_by = member_profile
            obj.updated_by = member_profile
        except AttributeError:
            # Fallback if the user is an admin but has no Member profile
            # You can leave it as None or handle it as a validation error
            pass 
            
        super().save_model(request, obj, form, change)