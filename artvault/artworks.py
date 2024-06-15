from flask import (
    Blueprint, current_app, jsonify, request, abort
)

from artvault.db import get_db

bp = Blueprint('artworks', __name__, url_prefix='/artworks')

# Is there any use case for using both tags
#  and filename, title, description on the same query?

# Filter has an AND clause valid after inner join
gen_sql = ('SELECT tags.id, title, description, count(tags.id) n, '
           'filename, date, patreon_url FROM patreon '
           'INNER JOIN tags ON patreon.id = tags.id '
           '{filter} '
           'WHERE ( ? = null OR lower(tag) IN ({questions}) ) '
           'GROUP BY tags.id '
           'HAVING n = ? '
           'ORDER BY patreon.date DESC;')


@bp.route('/latest', methods=['GET'])
def latest_artworks():
    args = request.args
    limit = args.get('limit', 30)
    rows = get_latest_artworks(limit)
    resp = build_response(rows)
    return resp


def get_latest_artworks(limit):
    db = get_db()
    sql_stmt = ('SELECT id, title, description, '
                'filename, date, patreon_url FROM patreon '
                'ORDER BY date DESC LIMIT ?;')
    rows = db.execute(sql_stmt, (limit, )).fetchall()
    return rows


@bp.route('/search', methods=['GET'])
def search_artworks():
    args = request.args
    if not args:
        error_resp = {'error': 'Malformed query',
                      'message': 'Empty query'}
        return error_resp, 400

    if 'title' in args and 'filename' in args:
        error_resp = {'error': 'Malformed query',
                      'message':
                      'Simultaneous title and filename search not supported'}
        return error_resp, 400

    tags = args.get('tags', None)
    if tags:
        tags = tags.split(',')
        tags = [t.strip() for t in tags]

    title = args.get('title', '')
    filename = args.get('filename', '')
    if title:
        rows = search_title(title, tags)
    elif filename:
        rows = search_filename(filename, tags)
    elif tags:
        rows = search_by_tag(tags)

    response = build_response(rows)
    return response


def build_response(rows):
    response = []
    for r in rows:
        r_dic = make_dict(r)
        r_dic['url'] = (
                current_app.config['VAULT_ROOT']
                + r_dic['filename']
                )
        r_dic['thumbnail'] = (
                current_app.config['THUMB_ROOT']
                + r_dic['filename']
                )
        r_dic['date'] = r_dic['date'].split('T')[0]
        response.append(r_dic)

    return jsonify(response)


def make_dict(row):
    cols = ['id', 'title', 'description', 'filename', 'date', 'patreon_url']
    dic_row = {col: row[col] for col in cols}
    return dic_row


def search_by_tag(tags):
    sql_stmt, tag_query = make_tag_query(tags, '')

    db = get_db()
    rows = db.execute(sql_stmt, tag_query).fetchall()

    return rows


def make_tag_query(tags: list[str], filt: str):
    if isinstance(tags, str):
        tags = [tags]

    # Add ? to prepared statement
    n_tags = len(tags)
    questions = ','.join('?' * n_tags)
    format_map = {
        'questions': questions,
        'filter': filt
        }
    sql_stmt = gen_sql.format_map(format_map)
    
    # Make queries for prepared statement
    lower_case_tags = [x.lower() for x in tags]
    nuller = n_tags if tags else ''
    queries = [nuller] + lower_case_tags + [n_tags]
    return sql_stmt, queries


def search_title(title, tags=''):
    db = get_db()
    if tags:
        sql_stmt, tag_query = make_tag_query(tags, "AND  title like ? ")
        queries = ['%' + title + '%'] + tag_query
        rows = db.execute(sql_stmt, queries).fetchall()
    else:
        # Static query with short circuiting
        sql_stmt = ("SELECT id, title, description, "
                    "filename, date, patreon_url "
                    "FROM patreon WHERE "
                    "(? = null OR title like ?) ORDER by date DESC")
        queries = (title, '%' + title + '%')
        rows = db.execute(sql_stmt, queries).fetchall()
    return rows


def search_filename(filename, tags=''):
    db = get_db()
    if tags:
        sql_stmt, tag_query = make_tag_query(tags, "AND filename like ? ")
        queries = ['%' + filename + '%'] + tag_query
        rows = db.execute(sql_stmt, queries).fetchall()
    else:
        # Static query with short circuiting
        sql_stmt = ("SELECT id, title, description, "
                    "filename, date, patreon_url "
                    "FROM patreon WHERE "
                    "(? = null OR filename like ?) ORDER by date DESC")
        queries = (filename, '%' + filename + '%')

        rows = db.execute(sql_stmt, queries).fetchall()
    return rows


def search_by_dynamic_query():
    args = request.args
    if not args:
        abort(400)

    db = get_db()
    # Dynamically construct query
    queries = []
    sql_stmt = ('SELECT id, title, description, filename, '
                'date FROM patreon WHERE')
    filter_list = []
    if 'title' in args:
        filter_list.append(' lower(title) like ? ')
        like_query = f"%{args['title']}%"
        queries.append(like_query)

    if 'filename' in args:
        filter_list.append(' filename like ? ')
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

    return jsonify(response)
