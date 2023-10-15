def test_empty(client):
    """Test and empty query """
    resp = client.get('/artworks/search')
    assert resp.status_code == 400

def test_Simultanoeus(client):
    """ Test searching for title and filename, simultanoeusly """
    resp = client.get('/artworks/search?title=a&filename=b')
    assert resp.status_code == 400

def test_title_search(client):
    resp = client.get('/artworks/search?title=Pinup Raine')
    post_id = resp.json[1]['id']
    assert post_id == 81944980

def test_filename_search(client):
    resp = client.get('/artworks/search?filename=mechanicpinupraine')
    post_id = resp.json[1]['id']
    assert post_id == 81944980

def test_tags(client):
    resp = client.get('/artworks/search?tags=Saria, Rose,Transformation')
    post_id = resp.json[0]['id']
    assert post_id == 86294042

def test_title_tags(client):
    resp = client.get('/artworks/search?tags=Color Art&title=Long sweater')
    post_id = resp.json[0]['id']
    assert post_id == 85267380

def test_title_tags(client):
    resp = client.get('/artworks/search?tags=Color Art&filename=mechanicpinupraine')
    post_id = resp.json[0]['id']
    assert post_id == 82524223

def test_empty_tags_with_filename(client):
    resp = client.get('/artworks/search?tags=&filename=mechanicpinupraine')
    post_id = resp.json[1]['id']
    assert post_id == 81944980

def test_empty_filename_with_tags(client):
    resp = client.get('/artworks/search?title=&tags=Saria,Rose,Transformation')
    post_id = resp.json[0]['id']
    assert post_id == 86294042

def test_redundant_file_with_tags(client):
    resp = client.get('/artworks/search?title=Portrait&tags=Saria,Rose,Transformation')
    post_id = resp.json[0]['id']
    assert post_id == 86294042

def test_latest_arts(client):
    default_limit = 30
    resp = client.get('/artworks/latest')
    n_resps = len(resp.json)
    assert n_resps == default_limit

def test_latest_arts_custom_limit(client):
    resp = client.get('/artworks/latest?limit=12')
    n_resps = len(resp.json)
    assert n_resps == 12
