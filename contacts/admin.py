from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submission_type', 'product', 'submitted_at')
    list_filter = ('submission_type', 'submitted_at')
    search_fields = ('name', 'email', 'product__name')
    readonly_fields = ('name', 'email', 'phone', 'message', 'submission_type', 'product', 'submitted_at')

    def has_add_permission(self, request):
        return False # Nobody should be able to add submissions from the admin

    def has_delete_permission(self, request, obj=None):
        return True # Allow deletion if needed
