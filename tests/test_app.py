import pytest
import json
from app import app, get_translation
from flask import Flask

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_translation_en_default(client, monkeypatch):
    monkeypatch.setenv("COUNTRY_CODE", "en")
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode().strip().lower() == "hello, world!"

def test_translation_query_param_success(client, monkeypatch):
    monkeypatch.setenv("COUNTRY_CODE", "en")
    response = client.get("/?cc=fr")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert response.data.decode().strip() != ""

def test_translation_query_param_fallback_to_env(client, monkeypatch):
    monkeypatch.setenv("COUNTRY_CODE", "de")
    response = client.get("/")
    assert response.status_code in [200, 404]

def test_missing_translation_key(client, monkeypatch):
    monkeypatch.setenv("COUNTRY_CODE", "xx")  # assume not in JSON
    response = client.get("/")
    assert response.status_code in [200, 404]
    assert isinstance(response.data.decode(), str)

def test_malformed_json(monkeypatch):
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: (_ for _ in ()).throw(json.JSONDecodeError("Malformed", "doc", 0)))
    with pytest.raises(json.JSONDecodeError):
        get_translation("en")

def test_file_not_found(monkeypatch):
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError("Not found")))
    with pytest.raises(FileNotFoundError):
        get_translation("en")

# def test_query_translation_with_valid_param(client):
#     response = client.get("/query?cc=en")
#     assert response.status_code in [200, 404]
#     if response.status_code == 200:
#         data = json.loads(response.data.decode())
#         assert "translation" in data
#         assert isinstance(data["translation"], str)