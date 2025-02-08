"""
This class is the main class of the "Adventure World" application.
'Ring Lord' is a very simple, text based adventure game. Users can walk
around some scenery. That's all. It should really be extended to make it more
interesting!

To play this game, create an instance of this class and call the "play" method.

This main class creates and initialises all the others: it creates all rooms,
creates the parser and starts the game. It also evaluates and executes the
commands that the parser returns.

This game is adapted from the 'World of Zuul' by Michael Kolling and
David J. Barnes. The original was written in Java and has been simplified and
converted to Python by Kingsley Sage.
"""

# This below section imports the relevant classes, so these are classes that can be used in order to structure our game around.
import logging
from chamber import Chamber
from text_ui import TextUI
from backpack import Backpack

# This is the main section of the code that runs each time when the game starts.
logging.basicConfig(filename='game_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Game:
    logging.info("starting the game")

    def __init__(self):
        """
        Initialises the game.
        """
        self.create_rooms()
        # This line of code creates the rooms that are being imported from the class of Chamber.
        self.current_room = self.burningcastle
        # This part of the code makes you start the game at the burning castle location.
        self.textUI = TextUI()
        # This line of the code allows you to interact with the code and by importing the text into the game.
        self.backpack = Backpack(capacity=0)
        # The above line starts using the backpack class and sets the backpack capacity at 0,
        # This is so that it is 0 when our game starts
        self.object_obtained = None
        # The above line of code allows me to use object_obtained throughout the code,
        # This is so that I can see whether an item has been obtained from a room
        self.game_finished = False

        self.GreatStable_open = False

# Below I am creating the code for each room, and I am coding each room: through defining what each room contains:
    # I am setting the name of each area, with the first part of the text in quotation marks
    # This will say what the name of the area is.
    # The second part that is in quotation marks is;
    # the text that will appear before the user when they enter the location.
    # The third part that is in quotation marks is the area within square brackets for each line of code;
    # this will contain the inventory of each item.
    def create_rooms(self):
        logging.info("Creating chambers")
        """
            Sets up all room assets.
        :return: None
        """
        self.burningcastle = Chamber('burning castle', "You have entered the burning castle", [])
        self.abandonedstables = Chamber('abandoned stables', "You have entered the abandoned stables, and see that a water bucket has been left on the floor, perhaps it may be useful further ahead.",["water bucket"])
        self.Throneroom = Chamber('Throne room', "You have entered the throne room",[])
        self.greatbridge = Chamber("on the Great bridge", "You arrive on the Great Bridge, but the bridge erupts into flames. You must first extinguish the fire before moving forward.",[])
        self.armory = Chamber("in the armory", "You have entered the armory and find a skeleton holding a greatsword and a shield. If you take these items, they may be of use to you.",["Sword and shield"])
        self.dragonlair = Chamber("In the Dragon's lair", "You have entered the Dragon's lair. You hear the low roars of dragons of many dragons in the distance... ",[])
        self.queenlake = Chamber("In the Queen lake", "You have entered the Queen's lake, and a gigantic hippo bursts out of the water. He begins to talk. If you wish to cross my path create for me a sandwich of the finest ingrdients this kingdom has to offer, and I shall reward you with treasures and mystery. ",[])
        self.kitchen = Chamber("In the Kitchen", "You have enter the Kitchen, and notice a chopping board, a knife, and a tap. Perhaps, they may be of some use?",['Knife and chopping board'])
        self.pantry = Chamber("In the Pantry", "You have entered the Pantry, you can only pick up the veg if you have knives on you. ",['Cheese, Mayo and lettuce'])
        self.GreatStable = Chamber("In the Great Stables", "You have entered the Great Stables",[])
        self.Drawbridge = Chamber("On the Final Drawbridge", "You are on the Final Drawbridge",[])

        # Here below I am setting up each chamber's exits.
        # This will create the exits for each area of the game.
        # This  will be displayed when the individual is at each of the locations.

        self.burningcastle.set_exit("east", self.abandonedstables)
        self.abandonedstables.set_exit("west", self.burningcastle)
        self.abandonedstables.set_exit("south", self.Throneroom)
        self.Throneroom.set_exit("north", self.abandonedstables)
        self.Throneroom.set_exit("south", self.greatbridge)
        self.greatbridge.set_exit("north", self.Throneroom)
        self.greatbridge.set_exit("south", self.armory)
        self.armory.set_exit("north", self.greatbridge)
        self.armory.set_exit("south", self.dragonlair)
        self.dragonlair.set_exit("west", self.queenlake)
        self.queenlake.set_exit("east", self.pantry)
        self.pantry.set_exit("west", self.queenlake)
        self.queenlake.set_exit("north", self.kitchen)
        self.kitchen.set_exit("south", self.queenlake)
        # self.queenlake.set_exit("west", self.GreatStable)
        self.GreatStable.set_exit("north", self.Drawbridge)
        self.Drawbridge.set_exit("play", self.burningcastle)

    # This section of the code below will print a welcome message when the game is played.
    # When the game has finished the player will get presented with a thankyou message.

    def play(self):
        logging.info("Starting the game loop")
        """
            The main play loop.
        :return: None
        """
        self.print_welcome()
        finished = False
        while not self.game_finished:
            command = self.textUI.get_command()  # Returns a 2-tuple
            finished = self.process_command(command)
        print("Thank you for playing!")

    # Below I am creating a definition, which links to the area above.
    # This is because the below message will be printed whenever the game is started.
    # Additionally, this will contain all commands the user can input when the game has started.

    def print_welcome(self):
        logging.info("Displaying welcome message")

        """
            Displays a welcome message.
        :return: None
        """
        self.textUI.print_to_textUI("The Castle is scorching. You see the rubble of collapsed building on the horizon. Your oxygen is depleting and you need to escape the forsaken castle")
        self.textUI.print_to_textUI("the castle is engulfed in flames, yet you seek salvation from such catastrophic devestation.")
        self.textUI.print_to_textUI("Search the castle. Escape the region, but be weary for the smoke has clouded your judgement and things are not as trivial as they once seemed...")
        self.textUI.print_to_textUI(f'Your command words are: {self.show_command_words()}')

    # The code below links to the above code.
    # This is because the below code contains what commands will be returned as potential commands that can be chosen.

    def show_command_words(self):
        logging.info("Showing command words")
        """
            Show a list of available commands.
        :return: None
        """
        return ['help', 'go', 'quit', 'Pick up items']

    # Below I have created definitions for the process commands.
    # This contains what commands for go, help, quit, and pick for different locations across the game.
    # This also contains what text to display when anything that is an invalid command
    # that will display when the player command doesn't meet a criteria.
    # The code then dives deeper and contains criteria for each command that could be selected.
    # When one or more criteria is selected it mentions what text should be printed in each instance.

    def process_command(self, command):
        logging.debug(f"Processing command: {command}")

        """
            Process a command from the TextUI.
        :param command: a 2-tuple of the form (command_word, second_word)
        :return: True if the game has been quit, False otherwise
        """
        command_word, second_word = command
        if command_word != None:
            command_word = command_word.upper()

        want_to_quit = False
        print (command_word)
        if command_word == "HELP":
            self.print_help()
        elif command_word == "GO":
            self.do_go_command(second_word)
        elif command_word == "QUIT":
            want_to_quit = True
        elif command_word == 'PICK':
            self.pick_up_items()
        else:
            # Unknown command...
            self.textUI.print_to_textUI("The flames have surrounded that location. Please type go followed by south,east,north,or west to go choose a different region")

        return want_to_quit

    def print_help(self):
        """
            Display some useful help text.
        :return: None
        """
        self.textUI.print_to_textUI("The flames approach. Make a decision quickly, as to where you wish to go. Type go, followed by a direction to choose where to go")
        # self.textUI.print_to_textUI("around the deserted complex.")
        # self.textUI.print_to_textUI("")
        self.textUI.print_to_textUI(f'Your command words are: {self.show_command_words()}.')

    def do_go_command(self, second_word):
        logging.debug(f"Executing go with input {second_word}")

        """
            Performs the GO command.
        :param second_word: the direction the player wishes to travel in
        :return: None
        """
        if second_word == None:
            # Missing second word...
            logging.info("Player didn't choose a direction")
            self.textUI.print_to_textUI("Go where?")
            return

        next_room = self.current_room.get_exit(second_word)

        if next_room == None:
            logging.info("Player chose direction with no room")
            self.textUI.print_to_textUI("There is no door!")
        else:
            self.current_room = next_room

        if self.current_room == self.greatbridge and second_word == 'north' and self.greatbridge.been_before == True:
            logging.info("Player went back from the great bridge from the armory")
            self.textUI.print_to_textUI("A bridge which was once in flames resides here.")

        if self.current_room == self.dragonlair and second_word == 'west' and self.dragonlair.been_before == True:
            logging.info("Player went back to the Dragon lair after having defeated the dragon.")
            self.textUI.print_to_textUI("The Dragon's body remains. Young Dragons appear to be crowding around the body of the larger Dragon and seem filled with anger and fury, but as they're too small to take flight and breath fire unlike the older Dragon they cower in fear, but roar continuously as you walk past them. You feel no remorse, as it was either kill or be killed, but a subtle sadness resides within you. You may pass, but your actions are nothing to be proud of...")
        else:
            self.textUI.print_to_textUI(self.current_room.get_long_description())

        if self.current_room == self.greatbridge and self.object_obtained == 'water bucket' and self.greatbridge.been_before == False:
            logging.info("Player removed the fire on the bridge.")
            self.greatbridge.been_before = True
            self.textUI.print_to_textUI("Luckily as you had picked up a water bucket earlier, you pour the water from the bucket over the fire, until no drop of water remains in the bucket, and you can now move onwards to the next location.")
            # self.current_room = self.armory

        elif self.current_room == self.greatbridge and self.greatbridge.been_before == False:
            logging.info("Player got the bridge before picking up the water bucket.")
            self.textUI.print_to_textUI("You cannot leave, until the fire has been dealt with. Find the water bucket, and bring it back to cross the bridge.")

        elif self.backpack.capacity >=5:
            logging.info("Player got the bridge before picking up the water bucket.")
            self.textUI.print_to_textUI("Your backpack capacity is full")
            self.textUI.print_to_textUI("Drop items so that you are carrying no more than 5 before continuing")

        if self.current_room == self.dragonlair and self.object_obtained == 'sword and shield'and self.dragonlair.been_before == False:
            self.dragonlair.been_before = True
            self.textUI.print_to_textUI("A Dragon awakens from its slumber in the distance, and you head towards it unsheathing your greatsword and shield. It opens in gaping jaw and attempts to bite, but you jump into the air and a mystical energy flows out of the shield, allowing you to jump extremely high and you come crashing down at the dragon's neck, successfully decapitating it with your greatsword.")

        elif self.current_room == self.dragonlair and self.dragonlair.been_before == False:
            self.textUI.print_to_textUI("You fear the presence of the Dragons, and your anxiety overtakes you. Come back equipped and you may gain more courage to face this behemouth of a beast")

        if self.current_room == self.queenlake and 'sandwich' not in self.object_obtained and not self.queenlake.been_before:
            #self.textUI.print_to_textUI("You cannot pass me mortal! Give me the delicacies of this land before you have permission to pass me. GO AND RETRIEVE ME A SNACK!")
            pass

        if self.current_room == self.queenlake and self.object_obtained == 'sandwich':
            self.textUI.print_to_textUI("Oh sorry, I didn't see you there. He proceeds to eat the sandwich. Decent at best, but I'll let you pass!")
            self.GreatStable_open = True
            self.queenlake.set_exit("west", self.GreatStable)

        if self.current_room == self.queenlake and second_word =='west' and self.GreatStable_open == False:
            self.textUI.print_to_textUI("You cannot pass me mortal! Give me the delicacies of this land before you have permission to pass me. GO AND RETRIEVE ME A SNACK!")

        if self.current_room == self.GreatStable and self.GreatStable_open==True:
            self.textUI.print_to_textUI("You get on a horse and ride out of the castle.")

        if self.current_room == self.Drawbridge:
            self.textUI.print_to_textUI("You ride out of the castle with style.")
            self.textUI.print_to_textUI("You will become a part of history.")
            self.textUI.print_to_textUI("You have won the game.")
            self.game_finished = True

    # The code below creates a new definition called pick up items.
    # This tells the code what exactly to print when different pick-ups are made.
    # This is done in order to keep track of the inventory an individual has for each part of the game.
    # This is also done in order to keep track of backpack capacity.
    # The code below also contains an element which ensures that a player contain hold more than 5 items.
    # Additionally, sections further below contains code that ensures that particular conditions are met
    # before each location opens up to ensure that the player can move onwards to the next location.

    def pick_up_items (self):

        if self.current_room == self.abandonedstables:
            if self.current_room == self.abandonedstables and self.backpack.capacity == 1:
                self.textUI.print_to_textUI("You have picked up the item in this room!")
            else:
                self.textUI.print_to_textUI("You have picked up Water Bucket")
                self.textUI.print_to_textUI("Your backpack capacity has increased by 1")
                self.textUI.print_to_textUI("You could use this water to extinguish any fires you find!")
                self.backpack.capacity = 1
                self.textUI.print_to_textUI(f"your backpack capacity is currently {self.backpack.capacity}")
                self.object_obtained = 'water bucket'

        if self.current_room == self.armory:
            if self.current_room == self.abandonedstables and self.object_obtained == 'sword and shield':
                self.textUI.print_to_textUI("You have picked up the item in this room!")
            self.textUI.print_to_textUI("You have picked up a greatsword and a shield from a nearby skeleton")
            self.textUI.print_to_textUI("Your backpack capacity has increased by 1")
            self.textUI.print_to_textUI("You could use this fight any monsters that reside within this castle!")
            self.object_obtained = 'sword and shield'
            self.backpack.capacity = 2
            self.textUI.print_to_textUI(f"your backpack capacity is currently {self.backpack.capacity}")

        if self.backpack.capacity >=5:
            self.textUI.print_to_textUI("Your backpack capacity is full")
            self.textUI.print_to_textUI("Drop items so that you are carrying no more than 5 before continuing")
            self.textUI.print_to_textUI(f"your backpack capacity is currently {self.backpack.capacity}")

        if self.current_room == self.kitchen:
                self.textUI.print_to_textUI("You have picked up a knife and a chopping board")
                self.textUI.print_to_textUI("Your backpack capacity has increased by 2")
                self.textUI.print_to_textUI("You could use to create an item of food!")
                self.object_obtained = 'knife and chopping board'
                self.backpack.capacity = 4
                self.textUI.print_to_textUI(f"your backpack capacity is currently {self.backpack.capacity}")

        if self.current_room == self.pantry and self.object_obtained =='knife and chopping board':
                self.textUI.print_to_textUI("You mix up the ingredients you find in hopes of creating a sandwich.")
                self.textUI.print_to_textUI("Your drop the knife and chopping board and grab the sandwich")
                self.textUI.print_to_textUI("Within your past life you were a chef! So the urge to create a delicious mitchellin star dish overcomes you. You begin to finely chop the lettuce. You twirl the cheese around the lettuce, and finely spread the mayonaise over your greatsword and spread it across the lettuce. ")
                self.textUI.print_to_textUI("This is the narrator. I know I shouldn't be breaking the fourth wall, but I felt like I should make a quick apperance, as you've been doing well! So here's a quick metaphorical handshake! So take this handshake and go speak with your Hippo friend! ")
                self.textUI.print_to_textUI("You have picked up a sandwich")
                self.object_obtained = 'sandwich'
                self.backpack.capacity = 4
                self.textUI.print_to_textUI(f"your backpack capacity is currently {self.backpack.capacity}")


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
