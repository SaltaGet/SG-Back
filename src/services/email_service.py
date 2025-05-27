import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config

from src.schemas.user_schema.email_contact import EmailContact

class EmailService:
    def __init__(self):
        self.smtp_server = config('SMTP_SERVER')
        self.port = config('EMAIL_PORT')
        self.email = config('EMAIL')
        self.password = config('EMAIL_PASSWORD')

    async def send_email(self, subject: str, html_message: str):
        logging.info("Enviando email")
        
        message = MIMEMultipart()
        message['From'] = self.email
        message['To'] = self.email
        message['Subject'] = subject

        message.attach(MIMEText(html_message, 'html'))

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            try:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(message)
                logging.info("Email enviado")
            except smtplib.SMTPException as e:
                logging.error(f"Error sending email: {e}")

    async def send_contact(self, contact: EmailContact):
        try:
            html_message = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Contacto SaltaGet</title>
            </head>
            <body style="background-color:#f4f4f4; margin:0; padding:0;">
                <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f4;">
                <tr>
                    <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background:#fff; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.05); margin:40px 0;">
                        <tr>
                        <td style="background:#007bff; color:#fff; padding:24px 0; text-align:center; border-radius:8px 8px 0 0;">
                            <h1 style="margin:0; font-size:28px; font-family:sans-serif;">SaltaGet</h1>
                        </td>
                        </tr>
                        <tr>
                        <td style="padding:32px 40px; font-family:sans-serif; color:#333;">
                            <h2 style="margin-top:0;">Nuevo contacto recibido</h2>
                            <p style="font-size:16px; line-height:1.6;">
                            <b>Asunto:</b> {contact.issue}<br>
                            <b>Nombre completo:</b> {contact.full_name}<br>
                            <b>Email:</b> {contact.email}<br>
                            <b>Celular:</b> {contact.cellphone}<br>
                            <b>Motivo:</b><br>
                            {contact.reason}
                            </p>
                        </td>
                        </tr>
                        <tr>
                        <td style="background:#f4f4f4; color:#888; text-align:center; padding:16px; border-radius:0 0 8px 8px; font-size:12px;">
                            © 2025 SaltaGet. Todos los derechos reservados.
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>
                </table>
            </body>
            </html>
            """
            await self.send_email("SaltaGet - Nuevo contacto", html_message)
            return True
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            return False

   