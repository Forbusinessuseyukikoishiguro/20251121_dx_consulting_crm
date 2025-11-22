from django.db import models
from django.utils import timezone


class Client(models.Model):
    """顧客情報"""
    company_name = models.CharField('会社名', max_length=200)
    contact_person = models.CharField('担当者名', max_length=100)
    email = models.EmailField('メールアドレス', blank=True)
    phone = models.CharField('電話番号', max_length=20, blank=True)
    industry = models.CharField('業種', max_length=100, blank=True)
    company_size = models.CharField('企業規模', max_length=50, blank=True)
    created_at = models.DateTimeField('登録日', default=timezone.now)
    
    class Meta:
        verbose_name = '顧客'
        verbose_name_plural = '顧客'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.company_name


class Project(models.Model):
    """案件管理"""
    STATUS_CHOICES = [
        ('inquiry', '初回相談'),
        ('hearing', 'ヒアリング中'),
        ('proposal', '提案作成中'),
        ('quotation', '見積提示'),
        ('negotiation', '商談中'),
        ('handover', 'エンジニア引継ぎ'),
        ('in_progress', '実施中'),
        ('completed', '完了'),
        ('on_hold', '保留'),
        ('lost', '失注'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects', verbose_name='顧客')
    title = models.CharField('案件名', max_length=200)
    status = models.CharField('ステータス', max_length=20, choices=STATUS_CHOICES, default='inquiry')
    consultation_content = models.TextField('ご相談内容', blank=True)
    proposal_content = models.TextField('提案内容', blank=True)
    estimated_amount = models.DecimalField('見積金額（円）', max_digits=10, decimal_places=0, null=True, blank=True)
    start_date = models.DateField('開始予定日', null=True, blank=True)
    end_date = models.DateField('完了予定日', null=True, blank=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    
    class Meta:
        verbose_name = '案件'
        verbose_name_plural = '案件'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.client.company_name} - {self.title}'


class Handover(models.Model):
    """引継ぎ記録"""
    HANDOVER_TYPE_CHOICES = [
        ('staff_notsu', '@Staff_Notsuさんへの引継ぎ'),
        ('uragami', '浦上泰弘さんへの引継ぎ'),
        ('engineer', 'その他エンジニアへの引継ぎ'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='handovers', verbose_name='案件')
    handover_type = models.CharField('引継ぎ先', max_length=20, choices=HANDOVER_TYPE_CHOICES)
    handover_to = models.CharField('引継ぎ先担当者名', max_length=100)
    handover_date = models.DateTimeField('引継ぎ日時', default=timezone.now)
    handover_content = models.TextField('引継ぎ内容')
    technical_requirements = models.TextField('技術要件', blank=True)
    notes = models.TextField('備考', blank=True)
    is_completed = models.BooleanField('引継ぎ完了', default=False)
    
    class Meta:
        verbose_name = '引継ぎ記録'
        verbose_name_plural = '引継ぎ記録'
        ordering = ['-handover_date']
    
    def __str__(self):
        return f'{self.project.title} - {self.get_handover_type_display()}'


class ProgressLog(models.Model):
    """進捗記録"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='progress_logs', verbose_name='案件')
    log_date = models.DateTimeField('記録日時', default=timezone.now)
    activity_type = models.CharField('活動種別', max_length=100, 
        choices=[
            ('meeting', '打ち合わせ'),
            ('phone', '電話'),
            ('email', 'メール'),
            ('proposal', '提案作成'),
            ('quotation', '見積作成'),
            ('presentation', 'プレゼン'),
            ('other', 'その他'),
        ]
    )
    content = models.TextField('内容')
    next_action = models.TextField('次回アクション', blank=True)
    created_by = models.CharField('記録者', max_length=100, default='担当者')
    
    class Meta:
        verbose_name = '進捗記録'
        verbose_name_plural = '進捗記録'
        ordering = ['-log_date']
    
    def __str__(self):
        return f'{self.project.title} - {self.log_date.strftime("%Y-%m-%d")}'


class EngineerHandoff(models.Model):
    """エンジニアへのバトンタッチ記録"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='engineer_handoffs', verbose_name='案件')
    engineer_name = models.CharField('エンジニア名', max_length=100)
    handoff_date = models.DateTimeField('バトンタッチ日時', default=timezone.now)
    technical_scope = models.TextField('技術的な対応範囲')
    current_status = models.TextField('現在の状況')
    client_requirements = models.TextField('顧客要件')
    timeline = models.TextField('スケジュール', blank=True)
    budget = models.DecimalField('予算（円）', max_digits=10, decimal_places=0, null=True, blank=True)
    special_notes = models.TextField('特記事項', blank=True)
    is_accepted = models.BooleanField('エンジニア承認済み', default=False)
    
    class Meta:
        verbose_name = 'エンジニアバトンタッチ'
        verbose_name_plural = 'エンジニアバトンタッチ'
        ordering = ['-handoff_date']
    
    def __str__(self):
        return f'{self.project.title} → {self.engineer_name}'
