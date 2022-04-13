# Generated by Django 3.2.12 on 2022-04-01 07:38
import qrcode
import qrcode.image.svg
from django.core.files.base import ContentFile
from django.db import migrations


def forwards(apps, schema_editor):
    Account = apps.get_model('accounts', 'Account')
    for acc in Account.objects.all():
        img = qrcode.make(
            f"algorand://{acc.address}", 
            version=1, 
            image_factory=qrcode.image.svg.SvgPathImage
        )
        cp = ContentFile(b'')
        img.save(cp)
        acc.qr_code.save('qr_code.svg', cp, save=False)
        acc.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20220328_1356'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop)
    ]