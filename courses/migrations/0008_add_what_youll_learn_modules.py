# courses/migrations/0008_add_what_youll_learn_modules.py

from django.db import migrations

def add_what_youll_learn_modules(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Module = apps.get_model('courses', 'Module')

    for course in Course.objects.all():
        Module.objects.get_or_create(
            course=course,
            title="What You'll Learn",
            defaults={
                "description": f"This module introduces the key concepts of {course.title}.",
            }
        )

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_alter_content_options_content_order_and_more'),  # keep this
    ]

    operations = [
        migrations.RunPython(add_what_youll_learn_modules),
    ]
