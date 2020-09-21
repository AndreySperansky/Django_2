# Generated by Django 3.0.7 on 2020-08-04 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='sex',
            field=models.CharField(choices=[('mail', 'Мужской'), ('femail', 'Женский'), ('other', 'Не указан')], default='other', max_length=6),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
