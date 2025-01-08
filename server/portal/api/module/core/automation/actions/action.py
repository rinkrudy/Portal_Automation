from abc import ABC, abstractmethod


class Action(ABC):
    def __init__(self) -> None:
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__} instance"
    
    @classmethod
    @abstractmethod  
    def set_argument(self, **kwargs):
        pass
        
    @classmethod
    @abstractmethod  
    def perform(self):
        """ 추상 메서드 : 반드시 구현해야함"""    
        pass
    
    
class ActionNode:
    def __init__(self, action) -> None:
        if action == None:
            raise ValueError("Action is invalid")
        self.__action = action
        self.__activate = True    
        pass
    
    @property
    def activate(self):
        return self.__activate

    @activate.setter
    def activate(self, value):
        self.__activate = True
    
    
    @property
    def action_inst(self):
        if self.__action == None:
            raise ValueError("Actino instance is none")
        return self.__action
        


