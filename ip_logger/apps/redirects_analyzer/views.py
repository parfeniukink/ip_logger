import csv

from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer

from .services import client_info
from . import serializers, models, tasks


class RedirectAPI(APIView):
    def get(self, request):
        """ Get redirect & write to DB
        :param request
        :return: HttpRedirect
        """
        redirect_url = request.GET.get('to')
        host = {'ip': client_info.get_ip(request=request),
                'browser': request.user_agent.browser.family,
                'os': request.user_agent.os.family,
                'platform': request.user_agent.device.family}

        if redirect_url:
            tasks.save_data.delay(GET=request.GET,
                                  HTTP_REFERER=request.META.get('HTTP_REFERER'),
                                  host=host)
            return redirect(redirect_url)
        return JsonResponse({"Error": 'Set redirect URL: api/analyzer/redirect?to=https://steelkiwi.com/jobs/'})


class RedirectsCsvAPI(APIView):
    renderer_classes = [CSVRenderer]

    def get(self, request):
        referrers_qs = models.Redirect.objects.all()
        referrers = serializers.CSVRedirectSerializer(referrers_qs,
                                                      many=True)
        response = Response(referrers.data)
        response['Content-Disposition'] = 'attachment; filename="referrers.csv"'
        return response


class AnalyzerViewSet(viewsets.ViewSet):
    @staticmethod
    def get_referrers(request) -> Response:
        """ Return all references of referrer/referrers from DB
        :param request
        :return: Response
        """
        redirect_domain = request.GET.get('redirect_domain')
        referrer_domain = request.GET.get('referrer_domain')

        if redirect_domain and referrer_domain:
            redirect = models.Redirect.objects.get(redirect_domain=redirect_domain)
            queryset = redirect.referrers.select_related().filter(referrer_domain=referrer_domain).order_by(
                '-created_at')
        else:
            queryset = models.Referrer.objects.all().order_by('-created_at')

        serializer = serializers.ReferrerSerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def get_grouped_redirects(request) -> Response:
        """ Return redirect/redirects with all referrers
        :param request
        :return: Response
        """
        redirect_domain = request.GET.get('redirect_domain')
        if redirect_domain:
            queryset = models.Redirect.objects.filter(redirect_domain=redirect_domain).order_by('-updated_at')
        else:
            queryset = models.Redirect.objects.all().order_by('-updated_at')
        serializer = serializers.RedirectSerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def get_top_referrers(request) -> Response:
        """ Return top 10 Referrers for current month
        :param request
        :return: Response
        """
        queryset = models.Referrer.objects.all().order_by('-updated_at')[:10]

        serializer = serializers.ReferrerSerializer(queryset, many=True)
        return Response(serializer.data)


################################################
####    Url patterns   ####
################################################
get_referrers = AnalyzerViewSet.as_view({
    'get': 'get_referrers'
})
get_grouped_redirects = AnalyzerViewSet.as_view({
    'get': 'get_grouped_redirects'
})
get_top_referrers = AnalyzerViewSet.as_view({
    'get': 'get_top_referrers'
})
