def test_empty(client):
    """ """
    resp = client.get('/artworks/search')
    assert resp.status_code == 400

def test_title(client):
    resp = client.get('/artworks/search?title=Pinup Raine')
    post_id = resp.json[0]['id']
    assert post_id == 81944980
