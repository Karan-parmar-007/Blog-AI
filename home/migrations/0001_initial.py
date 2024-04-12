# Generated by Django 5.0.3 on 2024-03-10 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("cat_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("post_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField(max_length=4000)),
                ("post_image", models.ImageField(upload_to="media/")),
                (
                    "cat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.category"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("comment_id", models.AutoField(primary_key=True, serialize=False)),
                ("content", models.TextField(max_length=1000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="home.post",
                    ),
                ),
            ],
        ),
    ]