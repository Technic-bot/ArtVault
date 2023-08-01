from flask import (
    Blueprint, current_app, jsonify, request, abort
)

from artvault.db import get_db

bp = Blueprint('artworks', __name__, url_prefix='/artworks')

def make_dict(row):
    cols = ['id','title','description','filename','date']
    dic_row = { col:row[col] for col in cols}
    return dic_row

@bp.route('/tags', methods=['POST'])
def seach_by_tag():
    return   

@bp.route('/search', methods=['GET'])
def search_by_title():
    args = request.args
    if not args:
        abort(400)

    db = get_db()    
    # Dynamically construct query
    queries = []
    sql_stmt = 'SELECT id, title, description, filename, date FROM patreon WHERE'
    filter_list = []
    if 'title' in args:
        filter_list.append( ' lower(title) like ? ')
        like_query = f"%{args['title']}%"
        queries.append(like_query)

    if 'filename' in args:
        filter_list.append( ' filename like ? ')
        like_query = f"%{args['filename']}%"
        queries.append(like_query)
    
    filter_stmt = 'AND'.join(filter_list)
    sql_stmt += filter_stmt + ' ORDER BY id;'    
    #rows = db.execute(sql_stmt, queries).fetchall()
    
    alternate_stmt = ("SELECT id, title, description, filename, date FROM patreon WHERE " 
                      "(? = null OR title like ?) "
                      "AND (? = null OR filename like ?) ")
    title_query = args.get('title',default='')
    fname_query = args.get('filename',default='')
    queries = ( title_query , '%' + title_query + '%',
                fname_query,'%' + fname_query + '%' )
 
    rows = db.execute(alternate_stmt, queries).fetchall()
    
    response = []
    for r in rows:
        r_dic = make_dict(r)    
        r_dic['url'] = current_app.config['VAULT_ROOT'] + r_dic['filename']
        response.append(r_dic)

    return  jsonify(response) 

