import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        # 환경변수에서 이메일 설정 가져오기
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "apg0001daum@gmail.com")
        self.sender_password = os.getenv("SENDER_PASSWORD", "ixkc hseb xven qbcf")
        
        if not self.sender_email or not self.sender_password:
            logger.warning("이메일 설정이 없습니다. 환경변수 SENDER_EMAIL과 SENDER_PASSWORD를 설정해주세요.")
    
    def send_article_email(self, email_data: Dict[str, Any]) -> bool:
        """
        기사 정보를 이메일로 전송
        
        Args:
            email_data: {
                'email': str,
                'title': str,
                'url': str,
                'original': str,
                'summary': str
            }
        
        Returns:
            bool: 전송 성공 여부
        """
        if not self.sender_email or not self.sender_password:
            raise ValueError("이메일 설정이 없습니다.")
        
        try:
            # 이메일 메시지 생성
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = email_data['email']
            msg['Subject'] = f"TransNews - {email_data['title']}"
            
            # 이메일 본문 생성
            body = f"""
안녕하세요!

TransNews에서 요청하신 기사 정보를 전송해드립니다.

📰 기사 제목: {email_data['title']}
🔗 기사 URL: {email_data['url']}

📄 원문:
{email_data['original']}

📝 요약:
{email_data['summary']}

감사합니다.
TransNews 팀
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # SMTP 서버 연결 및 이메일 전송
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"이메일 전송 성공: {email_data['email']}")
            return True
            
        except Exception as e:
            logger.error(f"이메일 전송 실패: {e}")
            return False
    
    def is_configured(self) -> bool:
        """이메일 서비스가 올바르게 설정되었는지 확인"""
        return bool(self.sender_email and self.sender_password)
