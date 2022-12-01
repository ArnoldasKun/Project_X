# Generated by Django 4.1.3 on 2022-12-01 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Armor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('summary', models.TextField(verbose_name='summary')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos', verbose_name='photo')),
            ],
        ),
        migrations.CreateModel(
            name='ArmorOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('m', 'manufacturing'), ('r', 'repairing'), ('c', 'cancelled'), ('t', 'taken'), ('a', 'assembled'), ('p', 'paid'), ('n', 'not paid'), ('s', 'sent')], default='m', max_length=1, verbose_name='status')),
                ('date', models.DateField(auto_now_add=True, verbose_name='order date')),
                ('due_date', models.DateField(verbose_name='due_date')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='price')),
            ],
            options={
                'ordering': ['due_date'],
            },
        ),
        migrations.CreateModel(
            name='ArmorType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(help_text='Enter type of the armor', max_length=200, verbose_name='type')),
            ],
        ),
        migrations.CreateModel(
            name='Blacksmith',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(max_length=100, verbose_name='last name')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='unique ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='price')),
                ('buyer_wishes', models.TextField(blank=True, help_text='Please, write all your wishes here', max_length=10000, null=True, verbose_name='buyer wishes')),
                ('armor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_lines', to='forge.armor', verbose_name='armor')),
                ('armor_type', models.ManyToManyField(to='forge.armortype', verbose_name='armor type(s)')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_lines', to='forge.armororder', verbose_name='order')),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=30, verbose_name='phone')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.AddField(
            model_name='armororder',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forge.buyer', verbose_name='buyer'),
        ),
        migrations.AddField(
            model_name='armor',
            name='armor_type',
            field=models.ManyToManyField(help_text='Choose armors from this blacksmith', to='forge.armortype', verbose_name='armors'),
        ),
        migrations.AddField(
            model_name='armor',
            name='blacksmith',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='armors', to='forge.blacksmith'),
        ),
    ]
