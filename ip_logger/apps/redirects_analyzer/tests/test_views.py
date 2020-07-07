import pytest

from django.utils.http import urlencode
from django.urls import reverse

from redirects_analyzer.models import (Browser,
                                       OperatingSystem,
                                       Platform,
                                       Host,
                                       Redirect,
                                       Referrer)
from redirects_analyzer.tasks import save_data
from redirects_analyzer.services import repo

pytestmark = pytest.mark.django_db


@pytest.fixture
def redirect():
    return Redirect.objects.create(redirect_url='www.mysite.com/path/',
                                   redirect_domain='mysite.com')


@pytest.fixture
def referrer_1(redirect):
    return Referrer.objects.create(referrer_url='www.referrer_1.com/path/',
                                   referrer_domain='referrer_1.com',
                                   redirect=redirect)


@pytest.fixture
def referrer_2(redirect):
    return Referrer.objects.create(referrer_url='www.referrer_2.com/path/',
                                   referrer_domain='referrer_2.com',
                                   redirect=redirect)


################################################
####    Tests   ####
################################################
def get_reverse(view: str, query_kwargs=None):
    url = reverse(view)
    if query_kwargs:
        for key, value in query_kwargs.items():
            url += f"?{key}={value}&"
    return url


@pytestmark
def test_redirect_api(client):
    url = get_reverse(view='api:analyzer')
    response = client.get(url)

    query_kwargs = {'to': 'https://steelkiwi.com/jobs/'}
    reverse_url = get_reverse(view='api:analyzer', query_kwargs=query_kwargs)
    reverse_response = client.get(reverse_url)

    wrong_payload = {'bad': 'https://steelkiwi.com/jobs/'}
    wrong_reverse_url = get_reverse(view='api:analyzer', query_kwargs=wrong_payload)
    wrong_reverse_response = client.get(wrong_reverse_url)

    assert reverse_response.status_code == 302
    assert response.status_code == 200
    assert wrong_reverse_response.status_code == 200


@pytestmark
def test_save_data_task():
    host = {'ip': '127.0.0.1',
            'browser': 'Chrome',
            'os': 'Linux',
            'platform': 'laptop'}
    result = save_data.delay(GET={"to": "https://steelkiwi.com/jobs/"},
                             HTTP_REFERER="https://google3.com",
                             host=host)
    assert result is not None


@pytestmark
def test_repo():
    host = {'ip': '127.0.0.1',
            'browser': 'Chrome',
            'os': 'Linux',
            'platform': 'laptop'}
    result = save_data.delay(GET={"to": "https://steelkiwi.com/jobs/"},
                             HTTP_REFERER="https://google3.com",
                             host=host)
    host = repo.save_host(**host)
    redirect = repo.save_redirect(redirect_url="https://steelkiwi.com/jobs/",
                                  redirect_domain="steelkiwi.com")
    referrer = repo.save_referrer(referrer_url="https://google.com/",
                                  referrer_domain="google.com",
                                  redirect=redirect)

    assert Host.objects.count() == 1
    assert Redirect.objects.count() == 1
    assert Referrer.objects.count() == 1


@pytestmark
def test_get_referrers_api(client):
    url = get_reverse(view='api:get_referrers')
    response = client.get(url)

    query_kwargs = {'redirect_domain': 'mysite.com',
                    'referrer_domain': 'referrer_1.com'}
    reverse_url = get_reverse(view='api:get_referrers', query_kwargs=query_kwargs)
    reverse_response = client.get(reverse_url)

    wrong_query_kwargs = {'bad_payload': 'mysite.com',
                          'payload': 'referrer_1.com'}
    wrong_reverse_url = get_reverse(view='api:get_referrers', query_kwargs=query_kwargs)
    wrong_reverse_response = client.get(wrong_reverse_url)

    assert response.status_code == 200
    assert reverse_response.status_code == 200
    assert wrong_reverse_response.status_code == 200

# And other
