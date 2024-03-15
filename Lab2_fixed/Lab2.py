import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Функция отправки письма
def send_email(email_login, email_password, smtp_server, recipient_email, subject, email_body):
    try:
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(email_login, email_password)
        msg = MIMEMultipart()
        msg['From'] = email_login
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(email_body, 'plain'))
        server.send_message(msg)
        server.quit()
        print("Успех: Письмо успешно отправлено!")
    except Exception as e:
        print("Ошибка:", str(e))

# Функция для чтения входящих писем
def read_emails(email_login, email_password, imap_server):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_login, email_password)
        mail.select('inbox')
        result, data = mail.search(None, 'ALL')
        email_ids = data[0].split()
        latest_email_id = email_ids[-1]  # Получаем последнее сообщение
        result, data = mail.fetch(latest_email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        print("Последнее письмо:\nОт:", msg['From'], "\nТема:", msg['Subject'], "\n", msg.get_payload(decode=True))
        mail.logout()
    except Exception as e:
        print("Ошибка:", str(e))

# Пример использования
email_login = input("Введите логин: ")
email_password = input("Введите пароль: ")
smtp_server = input("Введите SMTP сервер: ")
imap_server = input("Введите IMAP сервер: ")

# Для отправки письма
recipient_email = input("Введите email получателя: ")
subject = input("Введите тему письма: ")
email_body = input("Введите текст письма: ")
send_email(email_login, email_password, smtp_server, recipient_email, subject, email_body)

# Для чтения писем
read_emails(email_login, email_password, imap_server)
