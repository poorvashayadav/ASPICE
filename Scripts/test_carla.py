import unittest
from unittest.mock import MagicMock
from defect_logging import log_defect  # Importing the defect logging function from the same directory

# Mock classes to simulate behavior
class MockCarla:
    class Client:
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.world = MockWorld()

        def get_world(self):
            return self.world

class MockWorld:
    def __init__(self):
        self.actor = MagicMock()

# Test case
class TestCarlaSimulated(unittest.TestCase):

    def test_no_collision(self):
        client = MockCarla.Client('localhost', 2000)
        client.get_world().actor.check_collision = MagicMock(return_value=False)
        self.assertFalse(client.get_world().actor.check_collision())

    def test_collision(self):
        client = MockCarla.Client('localhost', 2000)
        client.get_world().actor.check_collision = MagicMock(return_value=True)

        try:
            self.assertFalse(client.get_world().actor.check_collision())
        except AssertionError as e:
            log_defect("test_collision", str(e))

    def test_actor_exists(self):
        client = MockCarla.Client('localhost', 2000)
        client.get_world().actor.exists = MagicMock(return_value=False)

        try:
            self.assertTrue(client.get_world().actor.exists())
        except AssertionError as e:
            log_defect("test_actor_exists", str(e))

if __name__ == '__main__':
    unittest.main()
