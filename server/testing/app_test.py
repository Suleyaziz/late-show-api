import json

def test_get_episodes(client):
    response = client.get('/episodes')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'id' in data[0]
    assert 'date' in data[0]
    assert 'number' in data[0]

def test_get_episode_by_id_success(client):
    # Get first episode
    episodes_response = client.get('/episodes')
    episode_id = json.loads(episodes_response.data)[0]['id']
    
    response = client.get(f'/episodes/{episode_id}')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'id' in data
    assert 'date' in data
    assert 'number' in data
    assert 'appearances' in data

def test_get_episode_by_id_not_found(client):
    response = client.get('/episodes/9999')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Episode not found'

def test_delete_episode_success(client):
    # Get first episode
    episodes_response = client.get('/episodes')
    episode_id = json.loads(episodes_response.data)[0]['id']
    
    response = client.delete(f'/episodes/{episode_id}')
    assert response.status_code == 204
    
    # Verify episode is deleted
    get_response = client.get(f'/episodes/{episode_id}')
    assert get_response.status_code == 404

def test_delete_episode_not_found(client):
    response = client.delete('/episodes/9999')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Episode not found'

def test_get_guests(client):
    response = client.get('/guests')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'id' in data[0]
    assert 'name' in data[0]
    assert 'occupation' in data[0]

def test_create_appearance_success(client):
    # Get first episode and guest
    episodes_response = client.get('/episodes')
    guests_response = client.get('/guests')
    
    episode_id = json.loads(episodes_response.data)[0]['id']
    guest_id = json.loads(guests_response.data)[0]['id']
    
    new_appearance = {
        'rating': 5,
        'episode_id': episode_id,
        'guest_id': guest_id
    }
    
    response = client.post(
        '/appearances',
        data=json.dumps(new_appearance),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert 'id' in data
    assert data['rating'] == 5
    assert 'episode' in data
    assert 'guest' in data

def test_create_appearance_validation_error(client):
    invalid_appearance = {
        'rating': 6,  # Invalid rating
        'episode_id': 1,
        'guest_id': 1
    }
    
    response = client.post(
        '/appearances',
        data=json.dumps(invalid_appearance),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert 'errors' in data