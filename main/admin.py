from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import About, Faq, Testimony, \
            Service, HowTo, Terms, Privacy, Site

admin.site.register(About)
admin.site.register(Faq)
admin.site.register(Testimony)
admin.site.register(Service)
admin.site.register(HowTo)
admin.site.register(Terms)
admin.site.register(Privacy)
admin.site.register(Site)
# admin.site.register(Contact)