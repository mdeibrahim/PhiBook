# Generated manually to fix NOT NULL constraint on name field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
