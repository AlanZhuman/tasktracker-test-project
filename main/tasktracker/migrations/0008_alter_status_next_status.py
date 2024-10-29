# Generated by Django 5.1.2 on 2024-10-29 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0007_alter_task_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='next_status',
            field=models.CharField(blank=True, choices=[('PLANNED', 'PLANNED'), ('ACTIVE', 'ACTIVE'), ('ON_CHECK', 'ON_CHECK'), ('DONE', 'DONE'), ('FAILED', 'FAILED'), ('EXPIRED', 'EXPIRED')], default='PLANNED', max_length=15, null=True),
        ),
    ]
