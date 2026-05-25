from backend.services.sessions import create_session, get_access_token_from_session, delete_session, update_session, get_refresh_token_from_session

def test_create_and_get_access_token():
    session_id = create_session("access_token_test", "refresh_token_test")
    assert session_id is not None
    
    access_token = get_access_token_from_session(session_id)
    assert access_token == "access_token_test"

def test_create_and_get_refresh_token():
    session_id = create_session("access_token_test", "refresh_token_test")
    assert session_id is not None
    refresh_token = get_refresh_token_from_session(session_id)
    assert refresh_token == "refresh_token_test"

def test_delete_session():
    session_id = create_session("access_token_test", "refresh_token_test")
    assert session_id is not None
    delete_session(session_id)
    assert get_access_token_from_session(session_id) is None
    assert get_refresh_token_from_session(session_id) is None

def test_update_session():
    session_id = create_session("access_token_test", "refresh_token_test")
    assert session_id is not None
    update_session(session_id, "new_access_token", "new_refresh_token")
    assert get_access_token_from_session(session_id) == "new_access_token"
    assert get_refresh_token_from_session(session_id) == "new_refresh_token"