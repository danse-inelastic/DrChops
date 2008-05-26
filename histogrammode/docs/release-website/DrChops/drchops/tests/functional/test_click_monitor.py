from drchops.tests import *

class TestClickMonitorController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='click_monitor'))
        # Test response...
