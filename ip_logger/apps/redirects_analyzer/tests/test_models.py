import pytest

from redirects_analyzer.models import (Browser,
                                       OperatingSystem,
                                       Platform,
                                       Host,
                                       Redirect,
                                       Referrer)

pytestmark = pytest.mark.django_db


################################################
####    Fixtures   ####
################################################
@pytest.fixture
def browser():
    return Browser.objects.create(family='Chrome')


@pytest.fixture
def os():
    return OperatingSystem.objects.create(family='Linux')


@pytest.fixture
def platform():
    return Platform.objects.create(family='laptop')


@pytest.fixture
def host(browser, os, platform):
    return Host.objects.create(ip='127.0.0.1',
                               browser=browser,
                               os=os,
                               platform=platform)


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
@pytestmark
def test_browser(browser):
    assert Browser.objects.count() == 1
    assert browser.family == 'Chrome'


@pytestmark
def test_os(os):
    assert OperatingSystem.objects.count() == 1
    assert os.family == 'Linux'


@pytestmark
def test_platform(platform):
    assert Platform.objects.count() == 1
    assert platform.family == 'laptop'


@pytestmark
def test_host(host):
    assert Host.objects.count() == 1
    assert host.ip == '127.0.0.1'


@pytestmark
def test_redirect(redirect, referrer_1, referrer_2):
    assert Redirect.objects.count() == 1
    assert redirect.redirect_url == 'www.mysite.com/path/'
    assert redirect.redirect_domain == 'mysite.com'
    assert redirect.referrers.count() == 2


@pytestmark
def test_referrer_1(referrer_1, redirect):
    assert Referrer.objects.count() == 1
    assert referrer_1.referrer_url == 'www.referrer_1.com/path/'
    assert referrer_1.referrer_domain == 'referrer_1.com'
    assert referrer_1.redirect == redirect


@pytestmark
def test_referrer_2(referrer_2, redirect):
    assert Referrer.objects.count() == 1
    assert referrer_2.referrer_url == 'www.referrer_2.com/path/'
    assert referrer_2.referrer_domain == 'referrer_2.com'
    assert referrer_2.redirect == redirect
