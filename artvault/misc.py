from flask import (
    Blueprint, current_app, send_file, jsonify, redirect
)

from artvault.db import get_db 

bp = Blueprint('random',__name__)

@bp.route('/random',methods=('GET','POST'))
def return_random():
    db = get_db()
    rnd = db.execute("SELECT * FROM patreon ORDER BY RANDOM() LIMIT 1;").fetchone()
    # print(rnd['title'],rnd['filename'])
    full_path = current_app.config['VAULT_ROOT'] + rnd['filename']
    print(full_path)
    # resp = {'url': full_path}
    # return jsonify(resp)
    return redirect(full_path, code=302)

@bp.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return r
