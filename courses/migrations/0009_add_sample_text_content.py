from django.db import migrations
from django.contrib.contenttypes.models import ContentType

def add_sample_text_content(apps, schema_editor):
    Module = apps.get_model('courses', 'Module')
    Text = apps.get_model('courses', 'Text')
    Content = apps.get_model('courses', 'Content')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Get content type for Text model
    text_ct = ContentType.objects.get_for_model(Text)

    # For each "What You'll Learn" module
    for module in Module.objects.filter(title="What You'll Learn"):
        course_title = module.course.title
        text_body = f"By the end of this course, you'll understand the core concepts of {course_title}."
        User = apps.get_model('auth', 'User')
        owner = User.objects.last()  #) or .last() depending on preference

        text = Text.objects.create(content=text_body, owner=owner)
      

        Content.objects.create(
            module=module,
            content_type=text_ct,
            object_id=text.id
        )

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_add_what_youll_learn_modules'),  # or latest
    ]

    operations = [
        migrations.RunPython(add_sample_text_content, reverse_code=migrations.RunPython.noop),
    ]
