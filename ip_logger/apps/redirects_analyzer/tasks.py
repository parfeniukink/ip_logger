from urllib.parse import urlparse

from celery import shared_task

from .services import repo


@shared_task
def save_data(*args, **kwargs):
    referrer_url = kwargs.get('HTTP_REFERER')
    host = kwargs.get('host')
    GET = kwargs.get('GET')
    redirect_url = GET['to']

    redirect_domain = urlparse(url=redirect_url).netloc
    redirect = repo.save_redirect(redirect_url=redirect_url, redirect_domain=redirect_domain)

    if referrer_url:
        referrer_domain = urlparse(url=referrer_url).netloc
        referrer = repo.save_referrer(referrer_url=referrer_url, referrer_domain=referrer_domain, redirect=redirect)
    host = repo.save_host(**host)

    return redirect, referrer, host
