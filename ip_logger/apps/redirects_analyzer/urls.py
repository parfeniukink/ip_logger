from django.urls import include, path

from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'redirects', views.AnalyzerViewSet, basename='redirects')

app_name = 'redirects_analyzer'

urlpatterns = [
    path('analyzer/redirect/', views.RedirectAPI.as_view(), name='analyzer'),
    path('analyzer/get_redirects_csv/', views.RedirectsCsvAPI.as_view(), name='get_redirects_csv'),

    # Analyzer views
    path('analyzer/get_referrers/', views.get_referrers, name='get_referrers'),
    path('analyzer/get_grouped_redirects/', views.get_grouped_redirects, name='get_grouped_redirects'),
    path('analyzer/get_top_referrers/', views.get_top_referrers, name='get_top_referrers'),
]
