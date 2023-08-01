from flask import Flask, request, Response, jsonify

import os

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')
    app.config['DATABASE'] = app.root_path + "/db/" + app.config['DB_NAME']
    
    instance_config = app.instance_path + "/instance_config.py"
    app.config.from_pyfile(instance_config)

    from . import db
    db.init_app(app)

    from . import artworks
    app.register_blueprint(artworks.bp)

    from . import misc
    app.register_blueprint(misc.bp)
    return app
