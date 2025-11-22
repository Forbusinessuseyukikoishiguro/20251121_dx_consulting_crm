from django.core.management.base import BaseCommand
from projects.models import Client, Project, Handover, ProgressLog, EngineerHandoff
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'サンプルデータを投入します'

    def handle(self, *args, **kwargs):
        # 既存データをクリア
        EngineerHandoff.objects.all().delete()
        ProgressLog.objects.all().delete()
        Handover.objects.all().delete()
        Project.objects.all().delete()
        Client.objects.all().delete()

        # 顧客データ
        client1 = Client.objects.create(
            company_name='株式会社テックソリューションズ',
            contact_person='山田太郎',
            email='yamada@tech-solutions.jp',
            phone='03-1234-5678',
            industry='IT・情報サービス',
            company_size='中堅企業（100-500名）'
        )

        client2 = Client.objects.create(
            company_name='グローバル製造株式会社',
            contact_person='佐藤花子',
            email='sato@global-mfg.co.jp',
            phone='06-9876-5432',
            industry='製造業',
            company_size='大企業（1000名以上）'
        )

        client3 = Client.objects.create(
            company_name='スタートアップ株式会社',
            contact_person='鈴木一郎',
            email='suzuki@startup.jp',
            phone='03-5555-6666',
            industry='スタートアップ',
            company_size='小規模企業（～50名）'
        )

        # 案件データ
        project1 = Project.objects.create(
            client=client1,
            title='業務システムのクラウド移行支援',
            status='proposal',
            consultation_content='''現在オンプレミスで運用している基幹システムをクラウドに移行したいとのご相談。
コスト削減とスケーラビリティの向上が主な目的。
現行システムの分析から移行計画の策定、実装支援までを希望されています。''',
            proposal_content='''3フェーズでの移行を提案：
1. 現状分析・移行計画策定（2ヶ月）
2. パイロット移行・検証（3ヶ月）
3. 本番移行・運用移管（4ヶ月）

総予算: 3,500万円''',
            estimated_amount=35000000,
            start_date=timezone.now().date() + timedelta(days=30),
            end_date=timezone.now().date() + timedelta(days=300)
        )

        project2 = Project.objects.create(
            client=client2,
            title='データ活用基盤の構築',
            status='negotiation',
            consultation_content='''製造現場のデータを活用した品質改善と予知保全の実現を目指している。
IoTセンサーからのデータ収集基盤とBIツールの導入を検討中。''',
            proposal_content='''データ基盤構築の提案：
- データレイク構築（AWS）
- ETL処理基盤の実装
- BI ダッシュボード開発
- 現場担当者向け研修プログラム''',
            estimated_amount=28000000,
            start_date=timezone.now().date() + timedelta(days=45)
        )

        project3 = Project.objects.create(
            client=client3,
            title='DX戦略策定支援',
            status='hearing',
            consultation_content='''スタートアップとして急成長中だが、業務プロセスが属人化している。
デジタル化による業務効率化とスケーラビリティの確保が課題。''',
            proposal_content='',
            estimated_amount=None
        )

        project4 = Project.objects.create(
            client=client1,
            title='セキュリティ強化プロジェクト',
            status='in_progress',
            consultation_content='''セキュリティ監査で指摘された課題への対応。
ゼロトラストアーキテクチャの導入を検討。''',
            proposal_content='''セキュリティ強化施策：
1. 多要素認証の導入
2. アクセス権限の見直し
3. セキュリティ監視体制の構築
4. 従業員向けセキュリティ研修''',
            estimated_amount=15000000,
            start_date=timezone.now().date() - timedelta(days=30),
            end_date=timezone.now().date() + timedelta(days=150)
        )

        # 引継ぎ記録
        handover1 = Handover.objects.create(
            project=project1,
            handover_type='staff_notsu',
            handover_to='Staff Notsu',
            handover_content='''クラウド移行の技術的な実装部分について相談。
特にデータベースマイグレーションとネットワーク設計について助言をお願いします。''',
            technical_requirements='''- AWS環境の構築経験
- PostgreSQLのマイグレーション経験
- VPNとセキュリティグループの設計''',
            is_completed=True
        )

        handover2 = Handover.objects.create(
            project=project2,
            handover_type='uragami',
            handover_to='浦上泰弘',
            handover_content='''データ基盤のアーキテクチャ設計について相談。
特にリアルタイム処理基盤の構築方法についてアドバイスが必要です。''',
            technical_requirements='''- ストリーミング処理の経験
- Kafka or Kinesis の知識
- データパイプライン設計経験''',
            is_completed=False
        )

        # エンジニアバトンタッチ
        engineer_handoff1 = EngineerHandoff.objects.create(
            project=project4,
            engineer_name='田中エンジニア',
            technical_scope='''セキュリティ監視システムの実装
- SIEM導入と設定
- ログ収集基盤の構築
- アラート設定''',
            current_status='要件定義完了。実装フェーズに移行予定。',
            client_requirements='''24時間365日の監視体制
リアルタイムアラート
月次レポート作成''',
            timeline='3ヶ月（設計1ヶ月、実装1.5ヶ月、テスト0.5ヶ月）',
            budget=8000000,
            special_notes='顧客側のセキュリティ部門との密な連携が必要',
            is_accepted=True
        )

        engineer_handoff2 = EngineerHandoff.objects.create(
            project=project1,
            engineer_name='佐々木エンジニア',
            technical_scope='''基幹システムのクラウド移行実装
- インフラ構築（AWS）
- アプリケーション移行
- データマイグレーション''',
            current_status='提案が承認され、キックオフ準備中',
            client_requirements='''ダウンタイム最小化（深夜・休日の作業）
段階的な移行
ロールバック計画の策定''',
            timeline='9ヶ月',
            budget=25000000,
            is_accepted=False
        )

        # 進捗記録
        ProgressLog.objects.create(
            project=project1,
            activity_type='meeting',
            content='初回キックオフミーティング実施。プロジェクトのスコープと期待値について合意。',
            next_action='現行システムの詳細ヒアリング（来週予定）',
            created_by='石黒 YUKIKO'
        )

        ProgressLog.objects.create(
            project=project1,
            activity_type='proposal',
            content='クラウド移行提案書を作成。3フェーズでの段階的移行を提案。',
            next_action='提案書のプレゼンテーション（明日 14:00）',
            created_by='石黒 YUKIKO'
        )

        ProgressLog.objects.create(
            project=project2,
            activity_type='phone',
            content='データ活用の目的と現状の課題についてヒアリング。製造現場の見学も希望されている。',
            next_action='工場見学の日程調整',
            created_by='石黒 YUKIKO'
        )

        ProgressLog.objects.create(
            project=project3,
            activity_type='meeting',
            content='経営陣とのミーティング。3年後のビジョンと現状のギャップを整理。',
            next_action='DX戦略書のドラフト作成',
            created_by='石黒 YUKIKO'
        )

        ProgressLog.objects.create(
            project=project4,
            activity_type='email',
            content='セキュリティ監視システムの進捗確認。田中エンジニアから実装が順調との報告あり。',
            next_action='中間報告会の開催（来月）',
            created_by='石黒 YUKIKO'
        )

        self.stdout.write(self.style.SUCCESS('サンプルデータの投入が完了しました！'))
        self.stdout.write(f'顧客: {Client.objects.count()}件')
        self.stdout.write(f'案件: {Project.objects.count()}件')
        self.stdout.write(f'引継ぎ: {Handover.objects.count()}件')
        self.stdout.write(f'エンジニアバトンタッチ: {EngineerHandoff.objects.count()}件')
        self.stdout.write(f'進捗記録: {ProgressLog.objects.count()}件')
