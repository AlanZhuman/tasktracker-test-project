# Generated by Django 5.1.2 on 2024-10-28 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0002_alter_task_executor_remove_task_observers_and_more'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='executor',
        ),
        migrations.RemoveField(
            model_name='task',
            name='observers',
        ),
        migrations.AddField(
            model_name='task',
            name='executor',
            field=models.ManyToManyField(related_name='tasks_as_executor', to='user.user'),
        ),
        migrations.AddField(
            model_name='task',
            name='observers',
            field=models.ManyToManyField(related_name='tasks_as_observer', to='user.user'),
        ),
    ]
