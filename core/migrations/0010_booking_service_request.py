from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_userjobhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='service_request',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='bookings',
                to='core.servicerequest',
            ),
        ),
    ]