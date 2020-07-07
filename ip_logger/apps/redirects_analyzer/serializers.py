from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from . import models


class ReferrerSerializer(serializers.ModelSerializer):
    redirect = serializers.SerializerMethodField()

    class Meta:
        model = models.Referrer
        fields = '__all__'

    @staticmethod
    def get_redirect(obj):
        return PureRedirectSerializer(obj.redirect).data


class PureReferrerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Referrer
        fields = ('referrer_url', 'referrer_domain')


class RedirectSerializer(serializers.ModelSerializer):
    referrers = serializers.SerializerMethodField()
    redirects = serializers.SerializerMethodField()

    class Meta:
        model = models.Redirect
        fields = '__all__'

    @staticmethod
    def get_redirects(obj):
        return obj.referrers.count()

    @staticmethod
    def get_referrers(obj):
        return PureReferrerSerializer(obj.referrers.all(),
                                      many=True).data


class CSVRedirectSerializer(serializers.ModelSerializer):
    redirects = serializers.SerializerMethodField()
    referrers = serializers.SerializerMethodField()

    class Meta:
        model = models.Redirect
        fields = '__all__'

    @staticmethod
    def get_redirects(obj):
        return obj.referrers.count()

    @staticmethod
    def get_referrers(obj):
        """ Return all redirect referrers without duplicates """
        return PureReferrerSerializer(obj.referrers.all().distinct('referrer_domain'),
                                      many=True).data


class PureRedirectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Redirect
        fields = ('redirect_domain',)


class BrowserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Browser
        fields = ('family',)


class OperatingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OperatingSystem
        fields = ('family',)


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Platform
        fields = ('family',)


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = '__all__'
