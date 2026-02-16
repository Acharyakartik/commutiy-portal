from django.contrib import admin
from member.models import Member,MemberDetail
# Register your models here.

# Member admin
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return True
    search_fields = ['member_no', 'first_name', 'middle_name', 'surname', 'email_id', 'education']
    list_display = (
        'member_no',
        'first_name',
        'middle_name',
        'surname',
        'username',
        'phone_no',
        'email_id',
        'marital_status',
        'education',
        'status',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'gender')
    list_per_page = 10
    list_max_show_all = 200

    class Media:
        css = {
            "all": ("admin_custom/news_changelist.css",)
        }
    
# MemberDetail admin
@admin.register(MemberDetail)
class MemberDetailAdmin(admin.ModelAdmin):
    list_display = (
        'member_id',
        'member_no',
        'first_name',
        'surname',
        'date_of_birth',
        'age',
        'gender',
        'occupation',
        'email_id',
        'marital_status',
        'education',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
    )
    list_filter = ('gender', 'member_no')  # optional filters
    
    readonly_fields = (
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
    )

    # Enable searching by MemberDetail fields AND related Member fields
    search_fields = (
        'first_name',
        'surname',
        'email_id',
        'education',
        'member_no__member_no',        # search by Member number
        'member_no__first_name',       # search by Member first name
        'member_no__surname',          # search by Member surname
    )

    # Enable autocomplete for member_no
    # autocomplete_fields = ['member_no']
    raw_id_fields = ['member_no']
    list_per_page = 10
    list_max_show_all = 200

    class Media:
        css = {
            "all": ("admin_custom/news_changelist.css",)
        }
