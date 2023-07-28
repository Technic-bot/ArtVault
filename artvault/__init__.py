from flask import Flask, request, Response, jsonify

def create_app():
    app = Flask(__name__)
    print(app.root_path)

    app.config.from_pyfile('config.py')
    app.config['DATABASE'] = app.root_path + "/db/" + app.config['DB_NAME']

    @app.route('/hello')
    def hello():
        return 'World';
    
    from . import db
    db.init_app(app)

    from . import misc
    app.register_blueprint(misc.bp)
    return app
