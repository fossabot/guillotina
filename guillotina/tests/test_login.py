import json
import jwt
from guillotina.auth.users import ROOT_USER_ID
from guillotina.testing import TESTING_SETTINGS


async def test_login(container_requester):
    async with container_requester as requester:
        response, status = await requester(
            'POST',
            '/db/guillotina/@login',
            data=json.dumps({
                'username': ROOT_USER_ID,
                'password': TESTING_SETTINGS['root_user']['password']
            }))
        assert status is 200
        assert 'token' in response
        payload = jwt.decode(
            response['token'],
            TESTING_SETTINGS['jwt']['secret'],
            algorithms=['HS256'])
        assert payload['id'] == ROOT_USER_ID


async def test_refresh(container_requester):
    async with container_requester as requester:
        response, status = await requester(
            'POST',
            '/db/guillotina/@login',
            data=json.dumps({
                'username': ROOT_USER_ID,
                'password': TESTING_SETTINGS['root_user']['password']
            }))
        assert status is 200

        response, status = await requester(
            'POST',
            '/db/guillotina/@login-renew')
        assert status is 200
        assert 'token' in response
        payload = jwt.decode(
            response['token'],
            TESTING_SETTINGS['jwt']['secret'],
            algorithms=['HS256'])
        assert payload['id'] == ROOT_USER_ID
