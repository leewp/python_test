#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from async_test1 import show_run_time
from async_test1 import sync_fetch
from concurrent.futures.thread import ThreadPoolExecutor
import time
import motor
import logging


@show_run_time
@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)


@show_run_time
@gen.coroutine
def print_fetch_coroutine(url):
    body = yield fetch_coroutine(url)
    print 'coroutine body:', body


@gen.coroutine
def divide(x, y):
    return x / y


def bad_call():
    divide(1, 0)


@gen.coroutine
def good_call():
    yield divide(1, 0)


@gen.coroutine
def call_task():
    t = yield gen.Task(IOLoop.current().add_timeout, time.time()+5)
    print 'Finished t', t


thread_pool = ThreadPoolExecutor(4)


@gen.coroutine
def call_blocking():
    t = yield thread_pool.submit(sync_fetch, 'https://www.zhihu.com')
    # print 'Finish t', t


@gen.coroutine
def parallel_fetch(url1, url2):
    http_client = AsyncHTTPClient()

    res1, res2 = yield [http_client.fetch(url1), http_client.fetch(url2)]
    print res1.body, res2.body


@gen.coroutine
def parallel_fetch_many(urls):
    http_client = AsyncHTTPClient()

    responses = yield [http_client.fetch(url) for url in urls]
    for r in responses:
        print r.code


@gen.coroutine
def parallel_fetch_dict(urls):
    http_client = AsyncHTTPClient()

    responses = yield {url: http_client.fetch(url) for url in urls}
    for k, v in responses.iteritems():
        print k, v.code

'''
db = motor.MotorClient.test


@gen.coroutine
def loop_example(collection):
    cursor = db.collection.find()
    while (yield cursor.fetch_next):
        doc = cursor.next_object()
'''


@gen.coroutine
def print_time():
    print time.time()


@gen.coroutine
def seconds_loop():
    while True:
        nxt = gen.sleep(10)
        yield print_time()
        yield nxt


if __name__ == '__main__':
    url_bd = 'https://www.baidu.com'
    urls = ['https://www.baidu.com', 'https://www.zhihu.com']
    # print_fetch_coroutine(url_bd)

    bad_call()
    good_call()
    call_task()
    print 'after call task'
    call_blocking()
    print 'after call block'
    parallel_fetch(*urls)
    parallel_fetch_many(urls)
    parallel_fetch_dict(urls)
    seconds_loop()
    print 'after seconds_loop'
    IOLoop.instance().start()
    # IOLoop.current().run_sync()
    # IOLoop.current().spawn_callback(divide, 1, 0)
    # IOLoop.current().spawn_callback(seconds_loop)
