from queue import Queue
import villager
import time

class eventManager:

    def __init__(self, villagers):
        self.events = Queue()
        self.villagers = villagers

    def send_to_event_system(self, eventName, additionalInfo):
        self.events.put([eventName, additionalInfo])

    def process_event(self, eventInfo):
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
        eventInfo = self.events.get()
        self.process_event(eventInfo)