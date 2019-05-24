# Generated by Django 2.2.1 on 2019-05-24 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    atomic = False

    dependencies = [
        ('login', '0002_auto_20190524_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movies_added', to='login.User')),
                ('favorited_by', models.ManyToManyField(related_name='favorites', to='login.User')),
            ],
        ),
    ]