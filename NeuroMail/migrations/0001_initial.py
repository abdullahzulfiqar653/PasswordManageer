# Generated by Django 4.2 on 2024-10-06 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.models.mixins.uid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.CharField(editable=False, max_length=15, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, main.models.mixins.uid.UIDMixin),
        ),
        migrations.CreateModel(
            name='EmailAiTemplate',
            fields=[
                ('id', models.CharField(editable=False, max_length=15, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, main.models.mixins.uid.UIDMixin),
        ),
        migrations.CreateModel(
            name='EmailBox',
            fields=[
                ('id', models.CharField(editable=False, max_length=15, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='email_attachments/')),
                ('to', models.TextField(blank=True, help_text="Comma-separated email addresses for 'To'")),
                ('cc', models.TextField(blank=True, help_text="Comma-separated email addresses for 'CC'")),
                ('bcc', models.TextField(blank=True, help_text="Comma-separated email addresses for 'BCC'")),
                ('email_type', models.CharField(choices=[('sent', 'Sent'), ('inbox', 'Inbox'), ('draft', 'Draft'), ('trash', 'Trash')], default='inbox', max_length=10)),
                ('is_starred', models.BooleanField(default=False)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_boxes', to='NeuroMail.email')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, main.models.mixins.uid.UIDMixin),
        ),
        migrations.CreateModel(
            name='EmailExtension',
            fields=[
                ('id', models.CharField(editable=False, max_length=15, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, main.models.mixins.uid.UIDMixin),
        ),
        migrations.CreateModel(
            name='EmailBoxRecipient',
            fields=[
                ('id', models.CharField(editable=False, max_length=15, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254)),
                ('recipient_type', models.CharField(choices=[('to', 'To'), ('cc', 'CC'), ('bcc', 'BCC')], max_length=3)),
                ('email_box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipients', to='NeuroMail.emailbox')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, main.models.mixins.uid.UIDMixin),
        ),
    ]
