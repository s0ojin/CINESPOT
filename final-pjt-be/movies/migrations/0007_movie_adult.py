# Generated by Django 4.2.8 on 2024-05-20 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0006_review_likes_users_review_review_likes_users_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie", name="adult", field=models.BooleanField(null=True),
        ),
    ]
