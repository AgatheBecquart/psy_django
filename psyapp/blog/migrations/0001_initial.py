<<<<<<< HEAD
# Generated by Django 4.2.3 on 2023-07-10 14:42

from django.db import migrations, models
import django.db.models.deletion
=======
# Generated by Django 4.1.7 on 2023-07-10 14:37

from django.db import migrations, models
>>>>>>> Agathe
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        ('authentication', '0001_initial'),
=======
>>>>>>> Agathe
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField(max_length=1000)),
                ('emotion', models.CharField(max_length=50)),
<<<<<<< HEAD
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.patient')),
=======
>>>>>>> Agathe
            ],
        ),
    ]
