# Generated by Django 2.0 on 2019-01-01 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthAppShopUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('myshopify_domain', models.CharField(editable=False, max_length=255, unique=True)),
                ('token', models.CharField(default='00000000000000000000000000000000', editable=False, max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductsDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.IntegerField(default=0)),
                ('productName', models.CharField(max_length=300)),
                ('quantity', models.IntegerField(default=0)),
                ('createdAt', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserDatabase',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('domainName', models.CharField(max_length=100, unique=True)),
                ('lastModified', models.DateTimeField()),
                ('flag', models.IntegerField(default=-1)),
            ],
        ),
        migrations.AddField(
            model_name='productsdatabase',
            name='sno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.UserDatabase'),
        ),
    ]