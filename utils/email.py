import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import BackgroundTasks
from utils.config import SMTP_EMAIL, SMTP_PASSWORD, SMTP_PORT, SMTP_SERVER

def generate_otp(length: int = 6) -> str:
    digits = "0123456789"
    return "".join(secrets.choice(digits) for _ in range(length))


def send_otp_email(email: str, otp: str):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = f"Filmo Authentication <{SMTP_EMAIL}>"
        msg["To"] = email
        msg["Subject"] = "Your OTP"

        # Plain-text fallback
        text = f"""
Your OTP is: {otp}

This code is valid for 5 minutes.
If you didn't request this, ignore this email.
"""

        html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your OTP</title>
</head>
<body style="margin:0; padding:0; background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="min-height:100vh;">
    <tr>
      <td align="center" style="padding:60px 20px;">
        <table width="500" cellpadding="0" cellspacing="0"
          style="background:#ffffff; border-radius:16px; box-shadow:0 20px 60px rgba(0,0,0,0.3); overflow:hidden; max-width:100%;">
          
          <!-- Header with gradient -->
          <tr>
            <td style="padding:40px 30px; text-align:center; background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <div style="width:64px; height:64px; margin:0 auto 16px; background:#ffffff; border-radius:50%; display:flex; align-items:center; justify-content:center;">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2L2 7V17C2 20.866 6.477 24 12 24C17.523 24 22 20.866 22 17V7L12 2Z" fill="#667eea"/>
                  <path d="M12 8V16M8 12H16" stroke="white" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
              <h1 style="margin:0; color:#ffffff; font-size:28px; font-weight:600; letter-spacing:-0.5px;">
                Verify Your Identity
              </h1>
            </td>
          </tr>

          <!-- Content -->
          <tr>
            <td style="padding:48px 40px;">
              <p style="margin:0 0 24px; color:#374151; font-size:16px; line-height:1.6; text-align:center;">
                Enter this verification code to continue with your authentication:
              </p>

              <!-- OTP Box -->
              <div style="
                text-align:center;
                margin:32px 0;
                padding:24px;
                background:linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
                border-radius:12px;
                border:2px solid #e5e7eb;
              ">
                <div style="
                  display:inline-block;
                  padding:20px 32px;
                  font-size:36px;
                  letter-spacing:8px;
                  font-weight:700;
                  color:#1f2937;
                  background:#ffffff;
                  border-radius:8px;
                  box-shadow:0 4px 6px rgba(0,0,0,0.05);
                ">
                  {otp}
                </div>
              </div>

              <!-- Timer info -->
              <div style="text-align:center; margin:24px 0;">
                <table cellpadding="0" cellspacing="0" style="margin:0 auto;">
                  <tr>
                    <td style="padding:12px 20px; background:#fef3c7; border-radius:8px; border-left:4px solid #f59e0b;">
                      <p style="margin:0; color:#92400e; font-size:14px; font-weight:500;">
                        ⏱️ Expires in <strong>5 minutes</strong>
                      </p>
                    </td>
                  </tr>
                </table>
              </div>

              <!-- Security note -->
              <div style="
                margin:32px 0 0;
                padding:20px;
                background:#f9fafb;
                border-radius:8px;
                border-left:4px solid #667eea;
              ">
                <p style="margin:0; color:#6b7280; font-size:14px; line-height:1.6;">
                  <strong style="color:#374151;">🔒 Security tip:</strong> Never share this code with anyone. 
                  Filmo will never ask for your OTP via phone or email.
                </p>
              </div>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:32px 40px; text-align:center; background:#f9fafb; border-top:1px solid #e5e7eb;">
              <p style="margin:0 0 8px; font-size:13px; color:#9ca3af;">
                Didn't request this code?
              </p>
              <p style="margin:0; font-size:13px; color:#6b7280; font-weight:500;">
                You can safely ignore this email.
              </p>
              <div style="margin:20px 0 0; padding:20px 0 0; border-top:1px solid #e5e7eb;">
                <p style="margin:0; font-size:12px; color:#9ca3af;">
                  © 2024 Filmo. All rights reserved.
                </p>
              </div>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)

    except Exception as e:
        print("Email error:", e)


def send_otp(bg: BackgroundTasks, email: str):
    otp = generate_otp()
    bg.add_task(send_otp_email, email, otp)
    return otp
