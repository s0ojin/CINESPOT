# Generated by Django 4.2.8 on 2024-05-21 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0002_rename_genre_ids_movie_genres"),
    ]

    operations = [
        migrations.RenameField(
            model_name="movie", old_name="genres", new_name="genre_ids",
        ),
    ]
