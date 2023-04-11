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





class Testimonial(BaseModel):
    image_url = models.CharField(null=True, blank=True, max_length=500)
    person_name = models.CharField(null=True, blank=True, max_length=500)
    testimony = models.CharField(null=True, blank=True, max_length=500)
    active = models.BooleanField(default=False)
    def __str__(self):
        active_testimonial = "testimony of " + self.person_name + " is an ACTIVE testimonial "
        inactive_testimonial = "testimony of " + self.person_name + " is an INACTIVE testimonial "
        return inactive_testimonial if self.active == False else active_testimonial


class OurTeam(BaseModel):
    image_url = models.CharField(null=True, blank=True, max_length=500)
    person_name = models.CharField(null=True, blank=True, max_length=500)
    position = models.CharField(null=True, blank=True, max_length=500)
    active = models.BooleanField(default=False)
    def __str__(self):
        active_string = "Team member " + self.person_name + " " + self.position + " is an ACTIVE team member"
        inactive_string = "Team member " + self.person_name + " " + self.position + " is an IN-ACTIVE team member"
        return active_string  if self.active == True else inactive_string 





class Testimonial(BaseModel):
    image_url = models.CharField(null=True, blank=True, max_length=500)
    person_name = models.CharField(null=True, blank=True, max_length=500)
    testimony = models.CharField(null=True, blank=True, max_length=500)
    active = models.BooleanField(default=False)
    def __str__(self):
        active_testimonial = "testimony of " + self.person_name + " is an ACTIVE testimonial "
        inactive_testimonial = "testimony of " + self.person_name + " is an INACTIVE testimonial "
        return inactive_testimonial if self.active == False else active_testimonial



class Banner(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    image_url = models.URLField()
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Deactivate other banners
        Banner.objects.exclude(pk=self.pk).update(active=False)
        super(Banner, self).save(*args, **kwargs)
        



