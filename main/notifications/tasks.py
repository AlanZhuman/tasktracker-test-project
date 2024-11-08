from decouple import config
import smtplib
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from notifications.models import Notification, User
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import Task
from django.utils import timezone
from datetime import timedelta
import requests

email = config('EMAIL')
password = config('EMAIL_PASSWORD')

TELEGRAM_BOT_TOKEN = config('TELEGRAM_TOKEN')

@shared_task
def celery_send_mail(change_type, data):
    recipient_emails = []

    task_id = data.get('task_id')

    try:
        task = Task.objects.get(id=task_id) 
        subject = f"Уведомление по задаче {task.name}" 
    except Task.DoesNotExist:
        print(f"Задача с ID {task_id} не найдена.")
        return 
    
    change_messages = {
        None: data.get('msg'),
        "CREATED": 'Была создана новая задача для вас или вас поместили в наблюдатели',
        "UPDATED": 'Задача была обновлена',
        "DELETED": 'Задача была удалена',
        "STATUS_CHANGED": 'Статус задачи изменён, прошу проверьте'
    }
 
    msg = change_messages.get(change_type, 'Сообщение по задаче')

    if change_type is None:
        for user_data in data.get('recipient_list', []):
            user_name = user_data.get('name')
            try:
                user = User.objects.get(name=user_name)
                recipient_emails.append(user.email)
            except ObjectDoesNotExist:
                print(f"Пользователь с именем {user_name} не найден.")
    elif change_type == "DELETED":
        for observer_recipient in task.observers.all():
            recipient_emails.append(observer_recipient.email)
        for executor_recipient in task.executor.all():
            recipient_emails.append(executor_recipient.email)
        try:
            task.delete()
        except Exception as e:
            print("Some Error occured: "+e)
            return
    else:
        for observer_recipient in task.observers.all():
            recipient_emails.append(observer_recipient.email)
        for executor_recipient in task.executor.all():
            recipient_emails.append(executor_recipient.email)


    if recipient_emails:
        try:
            with smtplib.SMTP_SSL('smtp.yandex.com') as server:
                    server.login(email, password)
                    message = MIMEMultipart()
                    message['From'] = email
                    message['To'] = ', '.join(recipient_emails)
                    message['Subject'] = subject

                    message.attach(MIMEText(msg, 'plain', 'utf-8'))

                    server.sendmail(email, recipient_emails, message.as_string())
        except Exception as e:
            print(f"Ошибка при отправке email: {e}")
    else:
        print("Нет доступных email-адресов для отправки сообщения.")

@shared_task
def celery_expirity_check():
    expired_tasks = Task.objects.filter(time_deadline__lt=timezone.now())

    for task in expired_tasks:
        task.time_deadline += timedelta(days=1)
        task.status = Task.Statuses.EXPIRED
        task.save()

        recipient_emails = []
    
        subject = f"Уведомление по задаче {task.name}" 
        msg = "Срок задачи истёк, дедлайн продлён на 1 день, пожалуйста обратитесь к PM за деталями"

        for observer_recipient in task.observers.all():
            recipient_emails.append(observer_recipient.email)
        for executor_recipient in task.executor.all():
            recipient_emails.append(executor_recipient.email)


        if recipient_emails:
            try:
                with smtplib.SMTP_SSL('smtp.yandex.com') as server:
                    server.login(email, password)
                    message = MIMEMultipart()
                    message['From'] = email
                    message['To'] = ', '.join(recipient_emails)
                    message['Subject'] = subject

                    message.attach(MIMEText(msg, 'plain', 'utf-8'))

                    server.sendmail(email, recipient_emails, message.as_string())
            except Exception as e:
                print(f"Ошибка при отправке email: {e}")
        else:
            print("Нет доступных email-адресов для отправки сообщения.")

@shared_task
def celery_send_tg(change_type, data):
    task_id = data.get('task_id')

    try:
        task = Task.objects.get(id=task_id) 
        subject = f"Уведомление по задаче {task.name}" 
    except Task.DoesNotExist:
        print(f"Задача с ID {task_id} не найдена.")
        return 
    
    change_messages = {
        None: data.get('msg'),
        "CREATED": 'Была создана новая задача для вас или вас поместили в наблюдатели',
        "UPDATED": 'Задача была обновлена',
        "DELETED": 'Задача была удалена',
        "STATUS_CHANGED": 'Статус задачи изменён, прошу проверьте'
    }
    
    msg = change_messages.get(change_type, 'Сообщение по задаче')

    # Получаем chat_id для отправки уведомлений
    recipient_chat_id = []

    if change_type is None:
        for user_data in data.get('recipient_list', []):
            user_name = user_data.get('name')
            try:
                user = User.objects.get(name=user_name)
                recipient_chat_id.append(user.telegram_chat_id)  # предполагается, что у вас есть `telegram_chat_id`
            except ObjectDoesNotExist:
                print(f"Пользователь с именем {user_name} не найден.")
    elif change_type == "DELETED":
        for observer_recipient in task.observers.all():
            recipient_chat_id.append(observer_recipient.telegram_chat_id)
        for executor_recipient in task.executor.all():
            recipient_chat_id.append(executor_recipient.telegram_chat_id)
        try:
            task.delete()
        except Exception as e:
            print(f"Ошибка при удалении задачи: {e}")
            return
    else:
        for observer_recipient in task.observers.all():
            recipient_chat_id.append(observer_recipient.telegram_chat_id)
        for executor_recipient in task.executor.all():
            recipient_chat_id.append(executor_recipient.telegram_chat_id)

    # Отправка уведомлений через Telegram
    for chat_id in recipient_chat_id:
        if chat_id:  # Убедитесь, что chat_id не пустой
            send_telegram_message(chat_id, f"{subject}\n\n{msg}")

def send_telegram_message(chat_id, message_text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Проверка на успешный статус
        print(f"Уведомление успешно отправлено пользователю {chat_id}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке уведомления: {e}")
