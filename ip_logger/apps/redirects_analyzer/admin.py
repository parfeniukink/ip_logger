from django.contrib import admin

from . import models


@admin.register(models.Redirect)
class RedirectAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Referrer)
class ReferrerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Host)
class HostAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Browser)
class BrowserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OperatingSystem)
class OperatingSystemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Platform)
class PlatformAdmin(admin.ModelAdmin):
    pass
