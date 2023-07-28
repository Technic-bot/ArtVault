from flask import (
    Blueprint
)

from artvault.db import get_db 

bp = Blueprint('random',__name__)

@bp.route('/random',methods=('GET','POST'))
def return_random():
    db = get_db()
    rnd = db.execute("SELECT * FROM patreon ORDER BY RANDOM() LIMIT 1;").fetchone()
    print(rnd['title'])
    return 'random'
