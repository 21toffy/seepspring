import uuid
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True



class Faq(BaseModel):
    question = models.CharField(null=True, blank=True, max_length=500)
    answer = models.CharField(null=True, blank=True, max_length=500)
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.question

class ReportChallenge(BaseModel):
    challenge = models.CharField(null=True, blank=True, max_length=500)
    solution = models.CharField(null=True, blank=True, max_length=500)
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.challenge


class ContactUs(BaseModel):
    channel = models.CharField(null=True, blank=True, max_length=500)
    value = models.CharField(null=True, blank=True, max_length=500)
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.channel


