from aiosmtplib import SMTP
from email.message import EmailMessage
from pydantic import EmailStr
import ssl

class EmailService:
    def __init__(self, smtp_server: str, port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password

    async def send_verification_email(self, to_email: EmailStr, verification_link: str):
        msg = EmailMessage()
        msg["From"] = self.username
        msg["To"] = to_email
        msg["Subject"] = "Подтверждение регистрации"
        
        body = f"""
        Добро пожаловать!
        Для завершения регистрации перейдите по ссылке:
        {verification_link}
        """
        msg.set_content(body)

        ssl_context = ssl.create_default_context()
        
        try:
            async with SMTP(
                hostname=self.smtp_server,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=True,
                tls_context=ssl_context
            ) as smtp:
                await smtp.send_message(msg)
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")