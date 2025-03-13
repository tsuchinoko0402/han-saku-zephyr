def test_index_page(client):
    """インデックスページが正しく表示されるかテスト"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, World!' in response.data
