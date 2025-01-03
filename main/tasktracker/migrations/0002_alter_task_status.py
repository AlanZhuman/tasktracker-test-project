# Generated by Django 5.1.2 on 2024-10-30 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('PLANNED', 'PLANNED'), ('ACTIVE', 'ACTIVE'), ('ON_CHECK', 'ON_CHECK'), ('DONE', 'DONE'), ('FAILED', 'FAILED'), ('EXPIRED', 'EXPIRED')], default='PLANNED', max_length=15),
        ),
    ]
