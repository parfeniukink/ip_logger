from .. import models


def save_host(*args, **kwargs):
    """ Save host details to DB
    :param args:
    :param kwargs:
    :return: models.Host
    """
    ip = kwargs.get('ip')
    browser = kwargs.get('browser')
    os = kwargs.get('os')
    platform = kwargs.get('platform')

    browser_family = models.Browser.objects.get_or_create(family=browser)[0]
    os_family = models.OperatingSystem.objects.get_or_create(family=os)[0]
    platform_family = models.Platform.objects.get_or_create(family=platform)[0]

    host, created = models.Host.objects.get_or_create(ip=ip,
                                                      browser=browser_family,
                                                      os=os_family,
                                                      platform=platform_family)
    return host


def save_redirect(*args, **kwargs):
    """ Save and return RedirectAPI instance
    :param args:
    :param kwargs:
    :return: models.RedirectAPI
    """
    redirect_url = kwargs.get('redirect_url')
    redirect_domain = kwargs.get('redirect_domain')
    redirect, created = models.Redirect.objects.get_or_create(redirect_url=redirect_url,
                                                              redirect_domain=redirect_domain)
    return redirect


def save_referrer(*args, **kwargs):
    """ Save and return Referrer instance
    :param args:
    :param kwargs:
    :return: models.Referrer
    """
    referrer_url = kwargs.get('referrer_url')
    referrer_domain = kwargs.get('referrer_domain')
    redirect = kwargs.get('redirect')
    referrer = models.Referrer.objects.create(referrer_url=referrer_url,
                                              referrer_domain=referrer_domain,
                                              redirect=redirect)
    return referrer
