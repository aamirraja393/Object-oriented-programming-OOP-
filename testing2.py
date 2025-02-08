import unittest
from chamber import Chamber
from backpack import Backpack
from games import Game

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.b1 = Backpack(6)
        self.c1 = Chamber('burning castle', "You have entered the burning castle", [])
        self.c2 = Chamber('abandoned stables', "You have entered the abandoned stables", ["water bucket"])
        self.c1.set_exit("east", self.c2)
        self.c2.set_exit("west", self.c1)
        self.g1 = Game()

    def tearDown(self):
        del self.b1
        del self.c1
        del self.c2
        del self.g1

    def test_backpack(self):
        self.b1.add_item('dog')
        self.b1.add_item('book')
        self.b1.add_item('pen')
        self.assertTrue(self.b1.check_item('book'))
        self.assertTrue(self.b1.check_item('pen'))
        self.assertFalse(self.b1.check_item('balloon'))

    def test_check_item(self):
        self.b1.add_item('dog')
        self.assertTrue(self.b1.check_item('dog'))
        self.assertFalse(self.b1.check_item('candy'))

    def test_remove_item(self):
        """Test removing items from the backpack."""
        self.b1.add_item('dog')
        self.b1.add_item('book')
        # Successfully remove an item
        self.b1.remove_item('dog')
        self.assertFalse(self.b1.check_item('dog'))

    def test_room_creation(self):
        # Testing the creation of rooms with correct descriptions
        self.assertEqual(self.c1.get_short_description(), "You have entered the burning castle")
        self.assertEqual(self.c2.get_short_description(), "You have entered the abandoned stables")

    def test_set_and_get_exits(self):
        # Testing exits set and retrieval
        self.assertEqual(self.c1.get_exit("east"), self.c2)
        self.assertEqual(self.c2.get_exit("west"), self.c1)
        self.assertIsNone(self.c1.get_exit("north"))

    def test_get_long_description(self):
        # Testing the long description of the room including exits
        description = self.c1.get_long_description()
        self.assertIn("You have entered the burning castle", description)
        self.assertIn("Exits: ['east']", description)

    def test_print_welcome(self):
        # Test if the welcome message is printed correctly
        self.g1.print_welcome()

    def test_process_go_command(self):
        self.g1.process_command(('GO', 'east'))
        expected_description = "You have entered the abandoned stables, and see that a water bucket has been left on the floor, perhaps it may be useful further ahead."
        self.assertEqual(self.g1.current_room.description, expected_description)

if __name__ == '__main__':
    unittest.main()
