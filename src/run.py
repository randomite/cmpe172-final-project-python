#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.factory import create_app
from api.utils.config import DevelopmentConfig, ProductionConfig
import os

if os.environ.get('WORK_ENV') == 'PROD':
    app = create_app(ProductionConfig)
else:
    if __name__ == '__main__':
        app = create_app(DevelopmentConfig)
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
        app.config['MYSQL_DATABASE_DB'] = 'employees'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        app.run(port=5000, host="0.0.0.0", use_reloader=True)

if __name__ == '__main__':
    if os.environ.get('WORK_ENV') == 'PROD':
        app = create_app(ProductionConfig)
        app.run(port=5000, host="0.0.0.0", use_reloader=False)
    else:
        app = create_app(DevelopmentConfig)
        app.run(port=5000, host="0.0.0.0", use_reloader=True)
