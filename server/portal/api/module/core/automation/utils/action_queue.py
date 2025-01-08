import queue
import threading
import time
from ..action import Action, ActionNode
from typing import Generic, TypeVar

T = TypeVar("T")

class ActionQueue(Generic[T]):
    def __init__(self, content: T):
        self.__queue = queue.Queue()
        self.__running = False
        
    def add_queue(self, item : T):
        self.__queue.put(item)
        print(f"Added action : {str(item)}")
        
    def process_actions(self):
        self.__running = True
        while self.__running:
            try:
                event = self.__queue.get()
                event.execute()
                self.__queue.task_done()
            except queue.Empty:
                self.__running = False
    
    def stop(self):
        self.__running = False
    