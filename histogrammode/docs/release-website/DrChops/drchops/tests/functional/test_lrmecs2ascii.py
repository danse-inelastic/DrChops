from drchops.tests import *

class TestLrmecs2AsciiController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='lrmecs2ascii'))
        # Test response...
