from decouple import config
import smtplib
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from notifications.models import Notification, User
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import Task
from django.utils import timezone
from datetime import timedelta

load_dotenv()

email = config('EMAIL')
password = config('EMAIL_PASSWORD')

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