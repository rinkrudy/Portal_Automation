from abc import ABC, abstractmethod


class ActionSequence:
    def __init__(self, *, name, description):
        self.name = "ActionSequence"
        self.description = ""
        if (name is not None):
            self.name = name
        if (description is not None):
            self.description = description
        self.__list_action = []
        pass
    
    @classmethod
    @abstractmethod        
    def intialize(self):
        pass
        
    def set_action(self, action : Action):
        if action is None:
            raise ValueError("Action is None, Failed append actionlist")
        action_node = ActionNode(action)
        self.__list_action.append(action)
        
    def execute(self):