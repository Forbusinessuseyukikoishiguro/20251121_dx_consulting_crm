from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import Client, Project, Handover, ProgressLog, EngineerHandoff


def dashboard(request):
    """ダッシュボード - 案件の統計情報を表示"""
    
    # ステータス別の案件数
    status_stats = Project.objects.values('status').annotate(count=Count('id'))
    
    # 今月の新規案件数
    this_month = timezone.now().replace(day=1)
    new_projects_count = Project.objects.filter(created_at__gte=this_month).count()
    
    # 進行中の案件数
    active_projects_count = Project.objects.filter(
        status__in=['hearing', 'proposal', 'quotation', 'negotiation', 'handover', 'in_progress']
    ).count()
    
    # 見積総額（進行中の案件）
    total_estimated = Project.objects.filter(
        status__in=['quotation', 'negotiation', 'handover', 'in_progress']
    ).aggregate(total=Sum('estimated_amount'))['total'] or 0
    
    # 最近の案件
    recent_projects = Project.objects.select_related('client').all()[:10]
    
    # エンジニアへの引継ぎ待ち
    pending_handoffs = EngineerHandoff.objects.filter(is_accepted=False).select_related('project')[:5]
    
    # 最近の活動記録
    recent_activities = ProgressLog.objects.select_related('project').all()[:10]
    
    context = {
        'status_stats': status_stats,
        'new_projects_count': new_projects_count,
        'active_projects_count': active_projects_count,
        'total_estimated': total_estimated,
        'recent_projects': recent_projects,
        'pending_handoffs': pending_handoffs,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'projects/dashboard.html', context)


def project_list(request):
    """案件一覧"""
    projects = Project.objects.select_related('client').all()
    
    # フィルタリング
    status = request.GET.get('status')
    if status:
        projects = projects.filter(status=status)
    
    search = request.GET.get('search')
    if search:
        projects = projects.filter(
            Q(title__icontains=search) |
            Q(client__company_name__icontains=search) |
            Q(consultation_content__icontains=search)
        )
    
    context = {
        'projects': projects,
        'status_choices': Project.STATUS_CHOICES,
        'current_status': status,
        'search_query': search,
    }
    
    return render(request, 'projects/project_list.html', context)


def project_detail(request, pk):
    """案件詳細"""
    project = get_object_or_404(Project.objects.select_related('client'), pk=pk)
    
    # 関連データを取得
    handovers = project.handovers.all()
    progress_logs = project.progress_logs.all()
    engineer_handoffs = project.engineer_handoffs.all()
    
    context = {
        'project': project,
        'handovers': handovers,
        'progress_logs': progress_logs,
        'engineer_handoffs': engineer_handoffs,
    }
    
    return render(request, 'projects/project_detail.html', context)


def client_list(request):
    """顧客一覧"""
    clients = Client.objects.annotate(
        project_count=Count('projects')
    ).all()
    
    # 検索機能
    search = request.GET.get('search')
    if search:
        clients = clients.filter(
            Q(company_name__icontains=search) |
            Q(contact_person__icontains=search) |
            Q(industry__icontains=search)
        )
    
    context = {
        'clients': clients,
        'search_query': search,
    }
    
    return render(request, 'projects/client_list.html', context)


def handover_list(request):
    """引継ぎ一覧"""
    handovers = Handover.objects.select_related('project', 'project__client').all()
    
    # フィルタリング
    handover_type = request.GET.get('type')
    if handover_type:
        handovers = handovers.filter(handover_type=handover_type)
    
    status = request.GET.get('status')
    if status == 'pending':
        handovers = handovers.filter(is_completed=False)
    elif status == 'completed':
        handovers = handovers.filter(is_completed=True)
    
    context = {
        'handovers': handovers,
        'handover_types': Handover.HANDOVER_TYPE_CHOICES,
        'current_type': handover_type,
        'current_status': status,
    }
    
    return render(request, 'projects/handover_list.html', context)


def engineer_handoff_list(request):
    """エンジニアバトンタッチ一覧"""
    handoffs = EngineerHandoff.objects.select_related('project', 'project__client').all()
    
    # 承認状況でフィルタ
    status = request.GET.get('status')
    if status == 'pending':
        handoffs = handoffs.filter(is_accepted=False)
    elif status == 'accepted':
        handoffs = handoffs.filter(is_accepted=True)
    
    context = {
        'handoffs': handoffs,
        'current_status': status,
    }
    
    return render(request, 'projects/engineer_handoff_list.html', context)
