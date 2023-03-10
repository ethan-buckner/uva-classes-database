# Generated by Django 4.1.2 on 2022-11-11 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('subject', models.CharField(db_column='subject_id', max_length=200, primary_key=True, serialize=False)),
                ('js', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=8)),
                ('overall_rating', models.IntegerField()),
                ('difficulty_rating', models.IntegerField()),
                ('user_name', models.CharField(default='anonymous', max_length=50)),
                ('user_email', models.CharField(max_length=50)),
                ('review_title', models.CharField(max_length=200)),
                ('review_text', models.CharField(max_length=600)),
                ('review_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('instructor', models.CharField(max_length=200)),
                ('email', models.CharField(default='x', max_length=200)),
                ('course_number', models.IntegerField(db_column='subj_id', primary_key=True, serialize=False)),
                ('semester_code', models.IntegerField()),
                ('course_section', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('catalog_number', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('units', models.CharField(max_length=200)),
                ('component', models.CharField(max_length=200)),
                ('class_capacity', models.IntegerField()),
                ('wait_list', models.IntegerField()),
                ('wait_cap', models.IntegerField()),
                ('enrollment_total', models.IntegerField()),
                ('enrollment_available', models.IntegerField()),
                ('topic', models.CharField(max_length=200)),
                ('days', models.CharField(default='', max_length=200)),
                ('start_time', models.CharField(default='', max_length=200)),
                ('end_time', models.CharField(default='', max_length=200)),
                ('facility_description', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UniqueUser',
            fields=[
                ('userID', models.IntegerField(primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=50)),
                ('userEmail', models.CharField(max_length=50)),
                ('userFriends', models.CharField(default='', max_length=500)),
                ('userSchedule', models.CharField(default='', max_length=500)),
            ],
        ),
    ]
