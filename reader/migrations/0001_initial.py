# Generated by Django 4.0.5 on 2022-06-18 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegAcceso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('reg_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuil', models.BigIntegerField()),
                ('deduccion', models.CharField(max_length=50)),
                ('tipo', models.CharField(max_length=50)),
                ('dato1', models.CharField(max_length=50)),
                ('dato2', models.CharField(blank=True, max_length=50, null=True)),
                ('porc', models.CharField(blank=True, max_length=3, null=True)),
                ('id_reg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registers', to='reader.regacceso')),
            ],
        ),
    ]