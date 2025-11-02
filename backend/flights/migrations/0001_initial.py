from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination_image', models.ImageField(blank=True, null=True, upload_to='destination_photos/')),
                ('flight_number', models.CharField(max_length=20)),
                ('airline', models.CharField(max_length=100)),
                ('from_city', models.CharField(max_length=100)),
                ('to_city', models.CharField(max_length=100)),
                ('from_airport_code', models.CharField(max_length=3)),
                ('to_airport_code', models.CharField(max_length=3)),
                ('departure', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('seats_available', models.PositiveIntegerField()),
                ('flight_class', models.CharField(max_length=20)),
                ('trip_type', models.CharField(default='one_way', max_length=10)),
                ('from_coords', models.CharField(blank=True, max_length=50, null=True)),
                ('to_coords', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(default=5)),
                ('text', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='flights.flight')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flight_reviews', to='users.user')),
            ],
        ),
    ]
