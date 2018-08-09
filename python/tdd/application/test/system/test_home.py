import json
from application.test.system.base_test import BaseTest


class TestHome(BaseTest):
    def test_home(self):
        with self.app() as c:
            resp = c.get('/')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(
                json.loads(resp.get_data()),
                {'message': 'Hello, world!'}
            )