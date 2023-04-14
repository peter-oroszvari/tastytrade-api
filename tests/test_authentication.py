import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest
import requests_mock
from tastytrade_api.authentication import TastytradeAuth

class TestTastytradeAuth(unittest.TestCase):
    API_URL = "https://api.tastytrade.com/sessions"

    def setUp(self):
        self.username = "test_username"
        self.password = "test_password"
        self.auth = TastytradeAuth(self.username, self.password)

    @requests_mock.Mocker()
    def test_login_success(self, mock):
        mock_response = {
            'data': {
                'user': {
                    'email': 'email@me.com',
                    'username': 'test_username',
                    'external-id': 'abcd-123'
                },
                'remember-token': 'rm-abcabc123123',
                'session-token': 'st-abcabc123123'
            },
            'context': '/sessions'
        }
        mock.post(self.API_URL, json=mock_response, status_code=201)

        auth_data = self.auth.login()

        with self.subTest("Check auth_data"):
            self.assertIsNotNone(auth_data)
        with self.subTest("Check session_token"):
            self.assertEqual(self.auth.session_token, mock_response['data']['session-token'])
        with self.subTest("Check remember_token"):
            self.assertEqual(self.auth.remember_token, mock_response['data']['remember-token'])
        with self.subTest("Check user_data"):
            self.assertEqual(self.auth.user_data, mock_response['data']['user'])

    @requests_mock.Mocker()
    def test_login_failure(self, mock):
        mock.post(self.API_URL, status_code=400)

        auth_data = self.auth.login()

        with self.subTest("Check auth_data"):
            self.assertIsNone(auth_data)
        with self.subTest("Check session_token"):
            self.assertIsNone(self.auth.session_token)
        with self.subTest("Check remember_token"):
            self.assertIsNone(self.auth.remember_token)
        with self.subTest("Check user_data"):
            self.assertIsNone(self.auth.user_data)

    @requests_mock.Mocker()
    def test_login_success_with_two_factor(self, mock):
        two_factor_code = "123456"
        mock_response = {
            'data': {
                'user': {
                    'email': 'email@me.com',
                    'username': 'test_username',
                    'external-id': 'abcd-123'
                },
                'remember-token': 'rm-abcabc123123',
                'session-token': 'st-abcabc123123'
            },
            'context': '/sessions'
        }
        mock.post(self.API_URL, json=mock_response, status_code=201)

        auth_data = self.auth.login(two_factor_code=two_factor_code)

        with self.subTest("Check auth_data"):
            self.assertIsNotNone(auth_data)
        with self.subTest("Check session_token"):
            self.assertEqual(self.auth.session_token, mock_response['data']['session-token'])
        with self.subTest("Check remember_token"):
            self.assertEqual(self.auth.remember_token, mock_response['data']['remember-token'])
        with self.subTest("Check user_data"):
            self.assertEqual(self.auth.user_data, mock_response['data']['user'])

    @requests_mock.Mocker()
    def test_destroy_session(self, mock):
        mock.delete(self.API_URL, status_code=204)

        self.auth.session_token = "st-abcabc123123"
        destroy_result = self.auth.destroy_session()

        with self.subTest("Check destroy_result"):
            self.assertTrue(destroy_result)
        with self.subTest("Check session_token"):
            self.assertIsNone(self.auth.session_token)
        with self.subTest("Check remember_token"):
            self.assertIsNone(self.auth.remember_token)
        with self.subTest("Check user_data"):
            self.assertIsNone(self.auth.user_data)

    @requests_mock.Mocker()
    def test_destroy_session_failure(self, mock):
        mock.delete(self.API_URL, status_code=400)

        self.auth.session_token = "st-abcabc123123"
        destroy_result = self.auth.destroy_session()

        with self.subTest("Check destroy_result"):
            self.assertFalse(destroy_result)
        with self.subTest("Check session_token"):
            self.assertIsNotNone(self.auth.session_token)

if __name__ == '__main__':
    unittest.main()
