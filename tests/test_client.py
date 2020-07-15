from werkzeug.security import generate_password_hash

from statsservice.models import Client


def test_client(session):
    client = Client(name="Corp")

    session.add(client)
    session.commit()

    assert client.is_active is False
    assert client.is_admin() is False
    assert client.token != ""
