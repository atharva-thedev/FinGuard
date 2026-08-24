import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config.env import settings


class NotificationService:
    @staticmethod
    def send_email(to_email: str, subject: str, body_html: str, body_text: str = "") -> bool:
        if not settings.smtp_host or not settings.smtp_user:
            # In development or when SMTP is not configured, log to console
            print(f"[EMAIL DEV MOCK] To: {to_email} | Subject: {subject}\n{body_text or body_html}")
            return True

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = settings.email_from
            msg["To"] = to_email

            if body_text:
                msg.attach(MIMEText(body_text, "plain"))
            msg.attach(MIMEText(body_html, "html"))

            with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
                server.login(settings.smtp_user, settings.smtp_pass)
                server.sendmail(settings.email_from, [to_email], msg.as_string())
            return True
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send email to {to_email}: {e}")
            return False

    @classmethod
    def send_approval_request(
        cls,
        to_email: str,
        approver_name: str,
        invoice_number: str,
        vendor_name: str,
        amount: float,
        approve_url: str,
        reject_url: str,
    ) -> bool:
        subject = f"[FinGuard] Approval Required: Invoice #{invoice_number} from {vendor_name}"
        body_text = (
            f"Hello {approver_name},\n\n"
            f"An invoice #{invoice_number} from {vendor_name} for ${amount:,.2f} is awaiting your approval.\n\n"
            f"Approve 1-Click: {approve_url}\n"
            f"Reject 1-Click: {reject_url}\n\n"
            f"FinGuard Finance Controls"
        )
        body_html = f"""
        <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #1e293b;">FinGuard Invoice Approval</h2>
            <p>Hello <strong>{approver_name}</strong>,</p>
            <p>Invoice <strong>#{invoice_number}</strong> from <strong>{vendor_name}</strong> for <strong>${amount:,.2f}</strong> requires your review.</p>
            <div style="margin: 30px 0;">
                <a href="{approve_url}" style="background-color: #059669; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; margin-right: 12px;">Approve Invoice</a>
                <a href="{reject_url}" style="background-color: #dc2626; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">Reject Invoice</a>
            </div>
            <p style="color: #64748b; font-size: 13px;">This action link expires in 48 hours. FinGuard SaaS.</p>
        </div>
        """
        return cls.send_email(to_email, subject, body_html, body_text)
