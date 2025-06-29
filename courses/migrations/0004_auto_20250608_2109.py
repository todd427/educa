# Generated by Django 5.0.14 on 2025-06-08 21:09

from django.db import migrations
from django.utils.text import slugify

def create_101_courses_and_welcome_modules(apps, schema_editor):
    Subject = apps.get_model('courses', 'Subject')
    Course = apps.get_model('courses', 'Course')
    Module = apps.get_model('courses', 'Module')
    User = apps.get_model('auth', 'User')

    owner = User.objects.first()
    if not owner:
        raise Exception("No users found. Please create a user before running this migration.")

    for subject in Subject.objects.all():
        course_title = f"{subject.title} 101"
        course_slug = slugify(course_title)

        course, created = Course.objects.get_or_create(
            subject=subject,
            owner=owner,
            slug=course_slug,
            defaults={"title": course_title}
        )

        Module.objects.get_or_create(
            course=course,
            title="Welcome",
            defaults={
                "description": f"Introduction to {subject.title}",
                "order": 0,
            }
        )


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20250608_2103'),
    ]

    operations = [
        migrations.RunPython(create_101_courses_and_welcome_modules),
    ]
