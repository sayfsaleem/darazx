# Generated by Django 4.2.7 on 2024-01-31 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_customuser_invite_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='bonus',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='invite_link',
            field=models.CharField(default='2ef496d5e9cb4c89b1839490e2363b1d', max_length=50),
        ),
    ]
