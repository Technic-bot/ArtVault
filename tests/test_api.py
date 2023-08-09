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
    post_id = resp.json[0]['id']
    assert post_id == 81944980

def test_filename_search(client):
    resp = client.get('/artworks/search?filename=mechanicpinupraine')
    post_id = resp.json[0]['id']
    assert post_id == 81944980

def test_tags(client):
    resp = client.get('/artworks/search?tags=Saria Rose Transformation')
    post_id = resp.json[0]['id']
    assert post_id == 58721673

def test_title_tags(client):
    resp = client.get('/artworks/search?tags=Color Art&title=Long sweater')
    post_id = resp.json[0]['id']
    assert post_id == 85267380

def test_title_tags(client):
    resp = client.get('/artworks/search?tags=Color Art&filename=mechanicpinupraine')
    post_id = resp.json[0]['id']
    assert post_id == 82524223
