import mock
from urllib.parse import urlencode
from snaprate.server import Application
from snaprate.handlers import MainHandler, BaseHandler
from tornado.testing import AsyncHTTPTestCase


class UserAPITest(AsyncHTTPTestCase):
    def get_app(self):
        self.app = Application([('/', MainHandler)])
        return self.app


class TestSnaprateApp(AsyncHTTPTestCase):
    def get_app(self):
        import sys
        sys.path.append('./bin')
        from run_server import create_parser, main
        parser = create_parser()
        args = parser.parse_args(['-d', 'web/tests', '--port', '8899'])
        server, t = main(args)
        return server

    def test_homepage(self):

        with mock.patch.object(BaseHandler, 'get_secure_cookie') as m:
            m.return_value = bytes('"tornado"', 'utf-8')
            response = self.fetch('/auth/login/')
            response = self.fetch('/spam')
            response = self.fetch('/', method='GET')
            data = {'username': 'guest',
                    'password': 'guest',
                    'resource': 'PIPELINE1'}
            response = self.fetch('/auth/login/', method='POST',
                body=urlencode(data))
            response = self.fetch('/')
            response = self.fetch('/?s=spam')
            response = self.fetch('/download/?s=PIPELINE1', method='GET')

            for each in ['next', 'prev', 'nextbad']:
                data = {"score": 0,
                        "comments": 'comment',
                        "subject": 1,
                        "pipeline": 'PIPELINE1',
                        "then": each}
                response = self.fetch('/post/', method='POST',
                                      body=urlencode(data))

            response = self.fetch('/download/?s=PIPELINE1', method='GET')
            data = {"src": 'BBRC02_E07373'}
            response = self.fetch('/xnat/', method='POST',
                                  body=urlencode(data))

            response = self.fetch('/auth/logout/')
            response = self.fetch('/stats/')
            response = self.fetch('/stats/?s=PIPELINE1')
            response = self.fetch('/?s=PIPELINE1&id=2')
            data = {'pipeline': 'PIPELINE1', "id": 1}
            response = self.fetch('/pipelines/', method='POST',
                                  body=urlencode(data))
