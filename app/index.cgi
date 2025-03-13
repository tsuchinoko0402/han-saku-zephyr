#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import cgitb
import os
cgitb.enable()
from wsgiref.handlers import CGIHandler
from app import create_app

class ProxyFix(object):
    def __init__(self, app):
        self.app = app
        
    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

if __name__ == '__main__':
    # 本番環境用の設定を読み込む
    app = create_app('prod')
    app.wsgi_app = ProxyFix(app.wsgi_app)
    CGIHandler().run(app)
