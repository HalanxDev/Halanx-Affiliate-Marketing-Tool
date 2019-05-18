from django.contrib import admin

from faqs.models import Topic, Question


@admin.register(Topic)
class TopicModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'pos')


@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'topic', 'created_at')
    prepopulated_fields = {'slug': ('text',)}
    list_filter = ('topic',)
