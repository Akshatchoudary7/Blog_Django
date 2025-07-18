# Generated by Django 5.2.4 on 2025-07-17 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_reaction_reaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislike_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='funny_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='love_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='reactions_data',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='post',
            name='sad_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='shock_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Reaction',
        ),
    ]
