# Generated by Django 3.2 on 2021-04-19 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestModel',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipments.equipmentmodel')),
                ('requested_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Request Model',
            },
        ),
    ]
