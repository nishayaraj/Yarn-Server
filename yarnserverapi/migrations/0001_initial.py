# Generated by Django 4.1.5 on 2023-01-12 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MyStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('author_name', models.CharField(max_length=50)),
                ('is_published', models.BooleanField()),
                ('public', models.BooleanField()),
                ('story', models.TextField(max_length=900)),
                ('date', models.DateField()),
                ('image_url', models.CharField(max_length=200)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='yarnserverapi.user')),
            ],
        ),
        migrations.CreateModel(
            name='MyJournal',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('journal_type', models.CharField(max_length=50)),
                ('image_url', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='yarnserverapi.user')),
            ],
        ),
        migrations.CreateModel(
            name='JournalStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('my_journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                 to='yarnserverapi.myjournal')),
                ('my_story', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='yarnserverapi.mystory')),
            ],
        ),
    ]
