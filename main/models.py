from django.db import models
from django.contrib.auth import get_user_model


class Faq(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return self.question[:10]

    class Meta:
        verbose_name_plural = 'FAQ'


class Testimony(models.Model):
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField()
    image=models.ImageField(upload_to="testimonies/", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Testimonies'


class Terms(models.Model):
    heading = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name_plural = 'Terms'


# class Contact(models.Model):
#     name=models.CharField(max_length=30)
#     email=models.EmailField(max_length=30)
#     title=models.CharField(max_length=20, null=True, blank=True)
#     subject=models.TextField()

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name_plural = 'Contact us'


class HowTo(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'How to invest'


class Privacy(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description[:10]

    class Meta:
        verbose_name_plural = 'Privacy'


class Service(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(upload_to="services/", null=True, blank=True)

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=30, verbose_name="Site name")
    website = models.CharField(max_length=30, verbose_name="Website URL", null=True, blank=True)
    address = models.CharField(max_length=50, verbose_name="Company address")
    phone = models.CharField(max_length=20, verbose_name="Company number")
    email = models.EmailField(max_length=30, verbose_name="Company email")
    founder = models.CharField(max_length=30, verbose_name="Company founder", null=True, blank=True)
    logo = models.ImageField(upload_to="main/", null=True, blank=True)
    year = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Site features'


class About(models.Model):
    heading = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    vision = models.TextField()
    mission = models.TextField()

    def __str__(self):
        return self.heading[:10]

    class Meta:
        verbose_name_plural = 'About us'