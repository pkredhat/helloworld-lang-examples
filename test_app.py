import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_root_returns_translation(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() != ""  # assumes a translation exists for default "en"

def test_root_invalid_country_code(monkeypatch, client):
    monkeypatch.setenv("COUNTRY_CODE", "zz")  # assuming "zz" doesn't exist
    from app import get_translation
    with pytest.raises(Exception, match="Translation not found"):
        get_translation("zz")

def test_missing_translation_file(monkeypatch):
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError("File not found")))
    from app import get_translation
    with pytest.raises(FileNotFoundError):
        get_translation("en")