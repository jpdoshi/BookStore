# Generated by Django 4.1.7 on 2023-04-18 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('imgurl', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField()),
            ],
        ),
    ]
