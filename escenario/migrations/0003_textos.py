# Generated by Django 2.1.4 on 2018-12-29 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escenario', '0002_contexto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Textos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('texto', models.TextField(verbose_name='Descripcion')),
                ('contexto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='escenario.Contexto')),
            ],
        ),
    ]
