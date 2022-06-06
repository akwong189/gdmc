from gdpc import interface as INTF
import random

class Villager:
    """Information about a Villager
    """
    def __init__(self, house):
        self.name = self.generate_name() #e.g. Ryan
        self.color = self.generate_color() #e.g. blue
        self.house = house #e.g. James's house
        self.relationships = [] #e.g. [James, 0], [Dana, +4], [Susan, -7]

    def generate_name(self):
        """Randomly generate a villager's first and last names.

        Returns:
            str: Villager's name
        """
        firstNameList = ["Ryan", "James", "Daniel", "Peter", 
                         "Justin", "Robert", "Deon", "Benjamin", 
                         "Jamal", "Vlad", "Sahil", "Tiger", "Adley", "Martin",
                         "Susan", "April", "Emily", "Marie", "Yvonne",
                         "Sarah", "Veronica", "Paris", "Emily", "Ava",
                         "Hannah", "Mackenna", "Katie", "Catherine", "Michael",
                         "Nathan", "Cale", "Kyle", "Luke", "Jacob", "Noah", "Peter"]
        lastNameList = ["Cornell", "Letterman", "Smith", "Barrelmaker",
                        "Woods", "Lee", "Goodman", "Jorgenson", "Washington",
                        "Hilton", "Sill", "Anderson", "Yang", "Eldemir", "Dotson"
                        "Vaughn", "Bell", "Duncan", "Smidt", "O'Flaherty",
                        "Foreman", "Moody", "Finn", "Dayment", "Godfrey", 
                        "Rees", "Sato", "Leahy"]
        return random.choice(firstNameList) + " " + random.choice(lastNameList)

    def generate_color(self):
        """Randomly generate a villager's text color.

        Returns:
            str: Villager's text color
        """
        colorList = ["light_blue", "light_green", "light_aqua", "light_red", 
                    "purple", "gold", "gray", "blue", "green", 
                    "aqua", "red", "light_purple", "yellow", "white"]
        return random.choice(colorList)

    def generate_relationships(self, villagers):
        """Initialize the relationship array of a Villager.

        Args:
            villagers (list): list of villagers in the settlement 
        """
        for item in villagers:
            if item.name != self.name:
                self.relationships.append([item.name, 0])
    
    def update_relationship(self, villagerName, relationshipNum):
        """Update the relationship array of a Villager.

        Args:
            villagerName (str): name of Villager whose relationship is to be updated
            relationshipNum (int): amount to update relationship value by 
        """
        for index, item in enumerate(self.relationships):
            if item[0] == villagerName:
                self.relationships[index][1] += relationshipNum

    def generate_vocab(self, query):
        """Constructs phrases to fill in sentence frames.

        Args:
            query (str): query for building a sentence

        Returns:
            str: random term from the query list
        """
        #vocab bank
        actionStart1 = "Run"
        actionStart2 = "Oh no"
        actionStart3 = "I\'m getting out of here"
        reason1 = "didn\'t go to church"
        reason2 = "is wearing metal armor"
        reason3 = "is ugly"
        actionEnd1 = "run"
        actionEnd2 = "oh no"
        #vocab organized
        actionStarts = [actionStart1, actionStart2, actionStart3]
        actionEnds = [actionEnd1, actionEnd2, actionStart3]
        reasons = [reason1, reason2, reason3]
        #return random reason
        if query == "reasons":
            return random.choice(reasons)
        #return random starts
        elif query == "starts":
            return random.choice(actionStarts)

    def lightning_dialogue(self, houseOwnerAffected):
        """Dialogue for the lightning stike event.

        Args:
            houseOwnerAffected (str): name of Villager whose house was struck by lightning or lightning struck near
        """
        dialogueSelect = random.randint(0, 10)
        relationshipToPerson = 0
        dialogue = None
        #check for relationship to person
        for index, item in enumerate(self.relationships):
            if houseOwnerAffected == item[0]:
                relationshipToPerson = self.relationships[index][1]
        #if bad relationship
        if relationshipToPerson < 0:
            text1 = "This is all " + houseOwnerAffected + "\'s fault!"
            text2 = "This is all because " + houseOwnerAffected + self.generate_vocab("reasons") + "."
            badResponses = [text1, text2]
            dialogue = random.choice(badResponses)
        #normal dialogue
        elif dialogueSelect < 7:
            text1 = "Is that lightning!?"
            text2 = "Lightning hit " + houseOwnerAffected + "\'s house!"
            text3 = self.generate_vocab("starts") + ", it's lightning!"
            text4 = "AHHHH!!!"
            normResponses = [text1, text2, text3, text4]
            dialogue = random.choice(normResponses)
        #print dialogue
        if dialogue:
            INTF.runCommand("tellraw @a {\"text\":\"\",\"extra\":[{\"text\":\"" + self.name + ": " + dialogue + "\",\"color\":\"" + self.color + "\",\"bold\":\"true\"}]}")


