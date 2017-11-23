#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from tornado.ioloop import IOLoop
from tornado.httpclient import HTTPClient
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPError
from tornado.concurrent import Future
from tornado import gen
from functools import wraps
from time import time


def show_run_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        before_run_time = time()
        ret = func(*args, **kwargs)
        print 'Run %s cost %f s' % (func.__name__, time()-before_run_time)
        return ret
    return wrapper


@show_run_time
def sync_fetch(url):
    http_client = HTTPClient()
    body = None
    try:
        response = http_client.fetch(url)
        body = response.body
    except HTTPError as e:
        logging.warning(sync_fetch.__name__+' HTTPError: '+str(e))
    except Exception as e:
        logging.error(sync_fetch.__name__+' Exception: '+str(e))
    return body


@show_run_time
def async_fetch(url):
    http_client = AsyncHTTPClient()

    def handle_response(res):
        output_content = async_fetch.__name__+' callback', res.body
        # print output_content
    http_client.fetch(url, callback=handle_response)


@show_run_time
def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    fetch_future = http_client.fetch(url)
    my_future = Future()

    def parse_future(f):
        my_future.set_result(f.result())
        # print 'Future result:', my_future.result()
    fetch_future.add_done_callback(
        parse_future
    )


@show_run_time
@gen.coroutine
def coroutine_fetch(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)


@show_run_time
@gen.coroutine
def print_coroutine_fetch(url):
    body = yield coroutine_fetch(url)
    print 'After time:', time()
    print 'body=', body


if __name__ == '__main__':
    url_fetch = 'https://www.baidu.com'
    ret_sync = sync_fetch(url_fetch)
    async_fetch(url_fetch)
    async_fetch_future(url_fetch)
    print 'Before time:', time()
    print_coroutine_fetch(url_fetch)
    IOLoop.instance().start()
