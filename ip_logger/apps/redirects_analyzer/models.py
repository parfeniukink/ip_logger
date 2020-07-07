from django.db import models


class Redirect(models.Model):
    redirect_url = models.URLField(max_length=200)
    redirect_domain = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Referrer(models.Model):
    referrer_url = models.URLField(max_length=200)
    referrer_domain = models.CharField(max_length=200)

    redirect = models.ForeignKey(Redirect,
                                 on_delete=models.CASCADE,
                                 related_name='referrers')

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Browser(models.Model):
    family = models.CharField(max_length=200)

    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)


class OperatingSystem(models.Model):
    family = models.CharField(max_length=200)

    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)


class Platform(models.Model):
    family = models.CharField(max_length=200)

    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)


class Host(models.Model):
    ip = models.CharField(max_length=15)
    browser = models.ForeignKey(Browser,
                                on_delete=models.CASCADE,
                                related_name='hosts',
                                verbose_name='browser')
    os = models.ForeignKey(OperatingSystem,
                           on_delete=models.CASCADE,
                           related_name='hosts',
                           verbose_name='os')
    platform = models.ForeignKey(Platform,
                                 on_delete=models.CASCADE,
                                 related_name='hosts',
                                 verbose_name='platform')

    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
