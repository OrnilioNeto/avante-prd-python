from django.db import migrations, models


def set_existing_users(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    User.objects.update(must_change_password=False)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='must_change_password',
            field=models.BooleanField(default=True, verbose_name='Deve trocar a senha'),
        ),
        migrations.RunPython(set_existing_users),
    ]
