from django.contrib import admin
from .models import Client, Project, Handover, ProgressLog, EngineerHandoff


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_person', 'industry', 'company_size', 'created_at']
    list_filter = ['industry', 'company_size', 'created_at']
    search_fields = ['company_name', 'contact_person', 'email']
    date_hierarchy = 'created_at'


class HandoverInline(admin.TabularInline):
    model = Handover
    extra = 0
    fields = ['handover_type', 'handover_to', 'handover_date', 'is_completed']


class ProgressLogInline(admin.TabularInline):
    model = ProgressLog
    extra = 0
    fields = ['log_date', 'activity_type', 'content', 'next_action']


class EngineerHandoffInline(admin.TabularInline):
    model = EngineerHandoff
    extra = 0
    fields = ['engineer_name', 'handoff_date', 'is_accepted']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'status', 'estimated_amount', 'start_date', 'created_at']
    list_filter = ['status', 'created_at', 'start_date']
    search_fields = ['title', 'client__company_name', 'consultation_content']
    date_hierarchy = 'created_at'
    inlines = [HandoverInline, ProgressLogInline, EngineerHandoffInline]
    
    fieldsets = (
        ('基本情報', {
            'fields': ('client', 'title', 'status')
        }),
        ('相談・提案内容', {
            'fields': ('consultation_content', 'proposal_content', 'estimated_amount')
        }),
        ('スケジュール', {
            'fields': ('start_date', 'end_date')
        }),
    )


@admin.register(Handover)
class HandoverAdmin(admin.ModelAdmin):
    list_display = ['project', 'handover_type', 'handover_to', 'handover_date', 'is_completed']
    list_filter = ['handover_type', 'is_completed', 'handover_date']
    search_fields = ['project__title', 'handover_to', 'handover_content']
    date_hierarchy = 'handover_date'


@admin.register(ProgressLog)
class ProgressLogAdmin(admin.ModelAdmin):
    list_display = ['project', 'log_date', 'activity_type', 'created_by']
    list_filter = ['activity_type', 'log_date']
    search_fields = ['project__title', 'content', 'next_action']
    date_hierarchy = 'log_date'


@admin.register(EngineerHandoff)
class EngineerHandoffAdmin(admin.ModelAdmin):
    list_display = ['project', 'engineer_name', 'handoff_date', 'budget', 'is_accepted']
    list_filter = ['is_accepted', 'handoff_date']
    search_fields = ['project__title', 'engineer_name', 'technical_scope']
    date_hierarchy = 'handoff_date'
    
    fieldsets = (
        ('基本情報', {
            'fields': ('project', 'engineer_name', 'handoff_date', 'is_accepted')
        }),
        ('技術要件', {
            'fields': ('technical_scope', 'current_status', 'client_requirements')
        }),
        ('予算・スケジュール', {
            'fields': ('budget', 'timeline')
        }),
        ('備考', {
            'fields': ('special_notes',)
        }),
    )
