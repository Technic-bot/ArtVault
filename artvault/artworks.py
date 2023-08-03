from flask import (
    Blueprint, current_app, jsonify, request, abort
)

from artvault.db import get_db

bp = Blueprint('artworks', __name__, url_prefix='/artworks')

def make_dict(row):
    cols = ['id','title','description','filename','date']
    dic_row = { col:row[col] for col in cols}
    return dic_row

gen_sql = ( 'SELECT tags.id, title, description, count(tags.id) n, '
            'filename, date FROM patreon '
            'INNER JOIN tags ON patreon.id = tags.id '
            'WHERE ( ? = null OR lower(tag) IN ({questions}) ) '
            'GROUP BY tags.id '
            'HAVING n = ? '
            'ORDER BY tags.id;')


@bp.route('/search', methods=['GET'])
def search_artworks():
    args = request.args
    if not args:
        error_resp = { 'error': 'Malformed query',
                       'message': 'Empty query'}
        return error_resp, 400


    if 'title' in args and 'filename' in args:
        error_resp = { 'error': 'Malformed query',
                       'message': 'Simultaneous title and filename search not supported'}
        return error_resp, 400

    if 'title' in args:
        rows = search_title(args.get('title',''))
    
    if 'filename' in args:
        rows = search_filename(args.get('filename',''))

    if 'tags' in args:
        tags = args.get('tags','')
        rows = search_by_tag(tags.split())

    response = []
    for r in rows:
        r_dic = make_dict(r)    
        r_dic['url'] = current_app.config['VAULT_ROOT'] + r_dic['filename']
        response.append(r_dic)

    return  jsonify(response) 

def search_by_tag(tags):
    n = len(tags)
    questions = ','.join('?' * n )
    format_map = {'questions': questions}
    nuller = n if tags else ''

    db = get_db()    
    sql_stmt = gen_sql.format_map(format_map)
    lower_case_tags = list(map(str.lower, tags))
    queries = [nuller] + lower_case_tags + [n]
 
    rows = db.execute(sql_stmt, queries).fetchall()

    return rows

def search_title(title):
    db = get_db()    
    # Static query with short circuiting 
    sql_stmt = ("SELECT id, title, description, filename, date FROM patreon WHERE " 
                      "(? = null OR title like ?) " )
    queries = ( title , '%' + title + '%')
 
    rows = db.execute(sql_stmt, queries).fetchall()
    return rows

def search_filename(filename):
    db = get_db()    
    # Static query with short circuiting 
    sql_stmt = ("SELECT id, title, description, filename, date FROM patreon WHERE " 
                      "(? = null OR filename like ?) ")
    queries = ( filename,'%' + filename + '%' )
 
    rows = db.execute(sql_stmt, queries).fetchall()
    return rows

def search_by_dynamic_query():
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
    rows = db.execute(sql_stmt, queries).fetchall()
    response = []
    for r in rows:
        r_dic = make_dict(r)    
        r_dic['url'] = current_app.config['VAULT_ROOT'] + r_dic['filename']
        response.append(r_dic)

    return  jsonify(response) 
