from django.db import models

from faqs.utils import create_slug, get_topic_image_upload_path


class Topic(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, blank=True)
    image = models.ImageField(upload_to=get_topic_image_upload_path, blank=True, null=True)
    pos = models.IntegerField(default=0)

    class Meta:
        ordering = ['pos']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.name, Topic.objects.values_list('slug', flat=True).all())
        super(Topic, self).save(*args, **kwargs)


class Question(models.Model):
    topic = models.ForeignKey('Topic', related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    answer = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    pos = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = "Frequent asked question"
        verbose_name_plural = "Frequently asked questions"
        ordering = ['pos']

    def __str__(self):
        return str(self.text)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.text, Question.objects.values_list('slug', flat=True).all())
        super(Question, self).save(*args, **kwargs)
