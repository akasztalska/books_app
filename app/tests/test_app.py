from http import HTTPStatus
import json
from app import main


def test_health(test_client):
    # when
    response = test_client.get(main.app.url_path_for("health"))
    # then
    assert response.status_code == HTTPStatus.OK.value
    assert response.json() == {"health": "It's working ✨"}


def test_should_create_a_book(test_client, monkeypatch):
    # given
    test_request_payload = {
        "title": "something",
        "author": "something else",
        "price": 10.0,
    }
    test_response_payload = {
        "id": 1,
        "title": "something",
        "author": "something else",
        "price": 10.0,
    }

    # when
    async def mock_post(payload):
        return 1

    monkeypatch.setattr(main, "add_book", mock_post)

    response = test_client.post(
        main.app.url_path_for("add_book"),
        data=json.dumps(test_request_payload),
    )
    # then
    assert response.status_code == HTTPStatus.OK.value
    assert response.json() == test_response_payload


def test_should_get_a_book(test_client, monkeypatch):
    # given
    test_data = {
        "id": 1,
        "title": "something",
        "author": "something else",
        "price": 10.0,
    }

    # when
    async def mock_get(id):
        return test_data

    monkeypatch.setattr(main, "get_book", mock_get)

    response = test_client.get(main.app.url_path_for("get_book", book_id=1))
    # then
    assert response.status_code == HTTPStatus.OK.value
    assert response.json() == test_data


def test_should_get_404_error_no_such_book(test_client, monkeypatch):
    # when
    async def mock_get(id):
        return None

    monkeypatch.setattr(main, "get_book", mock_get)

    response = test_client.get(main.app.url_path_for("get_book", book_id=999))
    # then
    assert response.status_code == HTTPStatus.NOT_FOUND.value
    assert response.json()["detail"] == "Book with such ID not found"


def test_should_get_all_books(test_client, monkeypatch):
    # when
    async def mock_get(payload):
        return 1

    monkeypatch.setattr(main, "get_all_books", mock_get)
    response = test_client.get(main.app.url_path_for("get_all_books"))
    # then
    data = response.json()
    assert response.status_code == HTTPStatus.OK.value
    assert len(data) == 1


def test_should_update_a_book_entry(test_client, monkeypatch):
    # given
    test_update_data = {
        "title": "test_title1_updated",
        "author": "test_author1",
        "price": 9.99,
    }
    expected_data = {
        "id": 1,
        "title": "test_title1_updated",
        "author": "test_author1",
        "price": 9.99,
    }

    # when
    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(main, "update_book", mock_put)

    response = test_client.put(
        main.app.url_path_for("update_book", book_id=1),
        data=json.dumps(test_update_data),
    )
    # then
    assert response.status_code == HTTPStatus.OK.value
    assert response.json() == expected_data


def test_should_successfully_delete_a_book(test_client, monkeypatch):
    # when
    async def mock_delete(id):
        return id

    monkeypatch.setattr(main, "delete_book", mock_delete)

    response = test_client.delete(main.app.url_path_for("delete_book", book_id=1))
    # then
    assert response.status_code == HTTPStatus.OK.value


def test_should_get_404_error_attempt_to_delete_nonexisting_book(
    test_client, monkeypatch
):
    # when
    async def mock_delete(id):
        return id

    monkeypatch.setattr(main, "delete_book", mock_delete)

    response = test_client.delete(main.app.url_path_for("update_book", book_id=999))
    # then
    assert response.status_code == HTTPStatus.NOT_FOUND.value
    assert response.json()["detail"] == "Book with such ID not found"
