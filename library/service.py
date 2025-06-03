from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives

from .models import Code
from .utils import code_generate
import threading


#
# def send_simple_email():
#     send_mail(
#         subject="Django email sinovi",
#         message="Bu test email.",
#         from_email="bekmurodovshohruh0224@gmail.com",
#         recipient_list=["bekmurodov2006@gmail.com"],
#         fail_silently=False,
#         html_message=
#         """
#             <h1>Xush Kelibsiz</h1>
#             <p>Bu bizning asosiy sahifa</p>
#         """
#     )
#
#
# def send_file_pdf_and_txt():
#     file_path = 'file.pdf'
#     email = EmailMessage(
#         subject="Test",
#         body='test_message',
#         from_email="bekmurodovshohruh0224@gmail.com",
#         to=["bekmurodov2006@gmail.com"],
#     )
#     with open(file_path, 'rb') as f:
#         email.attach("file.pdf", f.read(), "application/pdf")
#     email.send()
#
#

def send_html_email(to, user):
    try:
        reset_link = 'http://127.0.0.1:8000/restore_password/'
        subject = "Forgot Password"
        from_email = "bekmurodovshohruh0224@gmail.com"
        recipient_list = [to]
        text_content = "test"
        code = code_generate()
        Code.objects.create(code_number=code, user=user)
        html_content = f"""
        <main>
            <h1>Hello, {user.username}!</h1>
            <h2>{code}</h2>
            <p>A request to reset the password for your account has been received.</p>
            <p>If you initiated this request, click the button below to proceed.</p>
            <a href="{reset_link}" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Reset Password</a>
            <p>If you did not make this request, no further action is required.</p>
        </main>
        """
        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_email_in_thread(to, user):
    thread = threading.Thread(
        target=send_html_email,
        args=(to, user)
    )
    thread.start()
