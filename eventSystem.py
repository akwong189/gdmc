from queue import Queue
import villager
import time

class eventManager:
    """Manage the events that occur in the settlement.
    """
    def __init__(self, villagers):
        self.events = Queue()
        self.villagers = villagers

    def send_to_event_system(self, eventName, additionalInfo):
        """Send an event and info to the event system.

        Args:
            eventName (str): name of the event to be executed
            additionalInfo: additional info about the event to be executed
        """
        self.events.put([eventName, additionalInfo])

    def process_event(self, eventInfo):
        """Parses event interaction with other classes e.g. villagers

        Args:
            eventInfo (list): first item is the name of the event
        """
        if eventInfo[0] == "summon_husks":
            pass
        if eventInfo[0] == "summon_lightning":
            villagersHouse = None
            for item in self.villagers:
                print(eventInfo[1])
                if item.house == eventInfo[1]:
                    villagersHouse = item.name
            for item in self.villagers:
                time.sleep(1)
                item.lightning_dialogue(villagersHouse)
        if eventInfo[0] == "summon_villagers":
            pass

    def run_event(self):
        """Takes an event off the queue and sends it to process
        """
        eventInfo = self.events.get()
        self.process_event(eventInfo)