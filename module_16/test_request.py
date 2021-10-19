import pytest
import responses
import requests
from requests import HTTPError


def get_luke():
    try:
        response = requests.get('https://swapi.dev/api/people/1')
        if response.status_code != 404:
            response.raise_for_status()
        return response.json()
    except TimeoutError:
        return None
    except HTTPError:
        return None


@responses.activate
def test_get_luke():
    url = 'https://swapi.dev/api/people/1'
    responses.add(
        responses.GET,
        url,
        json={'error': 'not found'},
        status=404
    )
    person = get_luke()
    assert person is not None
    assert 'error' in person
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == url
