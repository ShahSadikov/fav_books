# Generated by Django 2.2 on 2021-04-17 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fav_books_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='books_liked_by',
            field=models.ManyToManyField(related_name='user_who_liked', to='fav_books_app.User'),
        ),
    ]
