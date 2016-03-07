#!/usr/bin/env python
# _*_ coding: utf-8 _*_

from app import create_app

application = create_app('production')

if __name__ == '__main__':
    application.run()