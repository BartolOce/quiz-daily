from django.contrib import admin

# Register your models here.
from .models import UserProfile, ModeratorProfile, Question, YesNoQuestion, MultipleChoiceQuestion

admin.site.register(UserProfile)
admin.site.register(ModeratorProfile)
admin.site.register(Question)
admin.site.register(YesNoQuestion)
admin.site.register(MultipleChoiceQuestion)
