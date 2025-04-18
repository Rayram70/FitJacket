from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutvideo',
            name='video_url',
            field=models.URLField(help_text='Paste a YouTube embed link or watch link'),
        ),
    ]
