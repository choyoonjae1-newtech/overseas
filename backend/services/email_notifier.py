"""
이메일 알림 서비스
- 중요 뉴스/공시 발생 시 관리자에게 이메일 발송
- SMTP를 통한 이메일 전송
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import logging
from datetime import datetime
from core.config import settings

logger = logging.getLogger(__name__)


class EmailNotifier:
    """이메일 알림 서비스"""

    def __init__(self):
        # SMTP 설정 (환경변수에서 가져옴)
        self.smtp_server = getattr(settings, 'SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = getattr(settings, 'SMTP_PORT', 587)
        self.smtp_username = getattr(settings, 'SMTP_USERNAME', None)
        self.smtp_password = getattr(settings, 'SMTP_PASSWORD', None)
        self.from_email = getattr(settings, 'FROM_EMAIL', self.smtp_username)
        self.admin_emails = getattr(settings, 'ADMIN_EMAILS', []).split(',') if hasattr(settings, 'ADMIN_EMAILS') else []

        # 알림 활성화 여부
        self.enabled = bool(self.smtp_username and self.smtp_password and self.admin_emails)

        if not self.enabled:
            logger.warning("이메일 알림이 비활성화되었습니다. SMTP 설정을 확인하세요.")

    def send_email(
        self,
        subject: str,
        body: str,
        to_emails: List[str],
        html: bool = False
    ) -> bool:
        """
        이메일 발송
        """
        if not self.enabled:
            logger.debug("이메일 알림이 비활성화되어 있습니다.")
            return False

        try:
            # 메시지 생성
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject

            # 본문 추가
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            # SMTP 서버 연결 및 발송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            logger.info(f"✅ 이메일 발송 완료: {subject} -> {', '.join(to_emails)}")
            return True

        except Exception as e:
            logger.error(f"❌ 이메일 발송 실패: {e}")
            return False

    def notify_new_regulation(
        self,
        country_name: str,
        news_title: str,
        news_url: Optional[str] = None,
        source: Optional[str] = None
    ) -> bool:
        """
        신규 금융규제 공시 알림
        """
        subject = f"[긴급] {country_name} 금융규제 공시 - {news_title}"

        body = f"""
JB우리캐피탈 해외사업 모니터링 시스템

새로운 금융규제 공시가 발표되었습니다.

📍 국가: {country_name}
📰 제목: {news_title}
📡 출처: {source or '알 수 없음'}
🔗 링크: {news_url or 'URL 없음'}
📅 알림 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⚠️ 이 공시는 귀사의 사업에 영향을 미칠 수 있습니다.
   상세 내용을 확인하시고 필요한 조치를 취하시기 바랍니다.

---
이 이메일은 자동으로 발송되었습니다.
JB우리캐피탈 해외사업 모니터링 시스템
        """.strip()

        # HTML 버전
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #dc2626; color: white; padding: 20px; text-align: center; }}
        .content {{ background-color: #f9fafb; padding: 20px; margin-top: 20px; border-radius: 8px; }}
        .info-item {{ margin: 10px 0; }}
        .label {{ font-weight: bold; color: #374151; }}
        .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>⚠️ 긴급 알림: 금융규제 공시</h2>
        </div>
        <div class="content">
            <p>새로운 금융규제 공시가 발표되었습니다.</p>

            <div class="info-item">
                <span class="label">📍 국가:</span> {country_name}
            </div>
            <div class="info-item">
                <span class="label">📰 제목:</span> {news_title}
            </div>
            <div class="info-item">
                <span class="label">📡 출처:</span> {source or '알 수 없음'}
            </div>
            <div class="info-item">
                <span class="label">🔗 링크:</span> <a href="{news_url or '#'}">{news_url or 'URL 없음'}</a>
            </div>
            <div class="info-item">
                <span class="label">📅 알림 시각:</span> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>

            <p style="margin-top: 20px; padding: 15px; background-color: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 4px;">
                <strong>⚠️ 중요:</strong> 이 공시는 귀사의 사업에 영향을 미칠 수 있습니다.
                상세 내용을 확인하시고 필요한 조치를 취하시기 바랍니다.
            </p>
        </div>
        <div class="footer">
            이 이메일은 자동으로 발송되었습니다.<br>
            JB우리캐피탈 해외사업 모니터링 시스템
        </div>
    </div>
</body>
</html>
        """

        return self.send_email(
            subject=subject,
            body=html_body,
            to_emails=self.admin_emails,
            html=True
        )

    def notify_geopolitical_risk(
        self,
        country_name: str,
        news_title: str,
        news_url: Optional[str] = None,
        source: Optional[str] = None
    ) -> bool:
        """
        지정학적 리스크 알림
        """
        subject = f"[주의] {country_name} 지정학적 리스크 - {news_title}"

        body = f"""
JB우리캐피탈 해외사업 모니터링 시스템

지정학적 리스크 관련 중요 뉴스가 감지되었습니다.

📍 국가: {country_name}
📰 제목: {news_title}
📡 출처: {source or '알 수 없음'}
🔗 링크: {news_url or 'URL 없음'}
📅 알림 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⚠️ 해당 국가의 정세 변화를 모니터링하시기 바랍니다.

---
이 이메일은 자동으로 발송되었습니다.
JB우리캐피탈 해외사업 모니터링 시스템
        """.strip()

        return self.send_email(
            subject=subject,
            body=body,
            to_emails=self.admin_emails,
            html=False
        )

    def send_daily_digest(
        self,
        news_count_by_country: dict,
        highlights: List[dict]
    ) -> bool:
        """
        일일 요약 리포트
        """
        subject = f"[일일 리포트] 해외사업 모니터링 요약 - {datetime.now().strftime('%Y-%m-%d')}"

        highlights_html = ""
        for item in highlights[:5]:  # 최대 5개
            highlights_html += f"""
            <div style="margin: 10px 0; padding: 10px; background-color: white; border-left: 3px solid #3b82f6; border-radius: 4px;">
                <div style="font-weight: bold; color: #1f2937;">{item['country']} - {item['title']}</div>
                <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">
                    {item['source']} • {item['category']}
                </div>
            </div>
            """

        body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #1e40af; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .stat-box {{ text-align: center; padding: 15px; background-color: #f3f4f6; border-radius: 8px; }}
        .stat-number {{ font-size: 32px; font-weight: bold; color: #1e40af; }}
        .stat-label {{ font-size: 14px; color: #6b7280; }}
        .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>📊 일일 모니터링 리포트</h2>
            <p>{datetime.now().strftime('%Y년 %m월 %d일')}</p>
        </div>
        <div class="content">
            <h3>📈 오늘의 수집 현황</h3>
            <div style="display: flex; gap: 20px; margin: 20px 0;">
                <div style="flex: 1; text-align: center; padding: 15px; background-color: #dbeafe; border-radius: 8px;">
                    <div style="font-size: 28px; font-weight: bold; color: #1e40af;">{news_count_by_country.get('MM', 0)}</div>
                    <div style="font-size: 14px; color: #1e40af;">🇲🇲 미얀마</div>
                </div>
                <div style="flex: 1; text-align: center; padding: 15px; background-color: #dcfce7; border-radius: 8px;">
                    <div style="font-size: 28px; font-weight: bold; color: #16a34a;">{news_count_by_country.get('ID', 0)}</div>
                    <div style="font-size: 14px; color: #16a34a;">🇮🇩 인도네시아</div>
                </div>
            </div>

            <h3 style="margin-top: 30px;">🔥 주요 소식</h3>
            {highlights_html if highlights_html else '<p style="color: #6b7280;">주요 소식이 없습니다.</p>'}
        </div>
        <div class="footer">
            이 이메일은 자동으로 발송되었습니다.<br>
            JB우리캐피탈 해외사업 모니터링 시스템
        </div>
    </div>
</body>
</html>
        """

        return self.send_email(
            subject=subject,
            body=body,
            to_emails=self.admin_emails,
            html=True
        )


# 싱글톤 인스턴스
email_notifier = EmailNotifier()
