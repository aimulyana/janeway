# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-26 12:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models, connection
import django.db.models.deletion


def copy_guest_editors(apps, schema_editor):
    Account = apps.get_model('core', 'Account')
    Issue = apps.get_model('journal', 'Issue')
    IssueEditor = apps.get_model('journal', 'IssueEditor')

    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM journal_issue_guest_editors;''')
    for row in cursor.fetchall():
        issue_pk = row[1]
        account_pk = row[2]

        issue_obj = Issue.objects.get(pk=issue_pk)
        account_obj = Account.objects.get(pk=account_pk)

        IssueEditor.objects.create(
            account=account_obj,
            issue=issue_obj,
            role='Guest Editor',
        )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journal', '0024_auto_20190304_0916'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueEditor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('role',
                 models.CharField(default='Guest Editor', max_length=255)),
                ('account',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='issueeditor',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.Issue'),
        ),
        migrations.RunPython(copy_guest_editors,
                             reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='issue',
            name='guest_editors',
        ),
        migrations.AddField(
            model_name='issue',
            name='editors',
            field=models.ManyToManyField(blank=True, null=True, related_name='guest_editors', through='journal.IssueEditor', to=settings.AUTH_USER_MODEL),
        ),
    ]