# Generated by Django 3.2.16 on 2022-10-22 12:32

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("public_id", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                ("jira_id", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[("В работе", "В работе"), ("Завершена", "Завершена")],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("cost_assign", models.PositiveIntegerField(blank=True, null=True)),
                ("cost_complete", models.PositiveIntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "tasks",
            },
        ),
    ]
