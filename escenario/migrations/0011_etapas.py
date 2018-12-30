# Generated by Django 2.1.4 on 2018-12-30 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escenario', '0010_auto_20181229_1824'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etapas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('inicio', models.DateField(null=True, verbose_name='Fecha Inicio')),
                ('fin', models.DateField(null=True, verbose_name='Fecha Termino')),
                ('trama', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='escenario.Trama')),
            ],
        ),
    ]
