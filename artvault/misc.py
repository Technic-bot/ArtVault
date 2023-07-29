from flask import (
    Blueprint, current_app, send_file
)

from artvault.db import get_db 

bp = Blueprint('random',__name__)

@bp.route('/random',methods=('GET','POST'))
def return_random():
    db = get_db()
    rnd = db.execute("SELECT * FROM patreon ORDER BY RANDOM() LIMIT 1;").fetchone()
    print(rnd['title'],rnd['filename'])
    full_path = current_app.config['VAULT_ROOT'] + rnd['filename']
    return send_file(full_path)
