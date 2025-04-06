from queue import PriorityQueue
from GradeVoo import GradeVoo

class FilaPrioridade:
  def __init__(self, initial_item:GradeVoo):
    self.queue = PriorityQueue()
    self.enqueue(initial_item)
  def enqueue(self, value:GradeVoo):
    self.queue.put((value.fitness, value))

  def dequeue(self):
    if(not self.queue.empty()):
      (_, no) = self.queue.get()
      return no
    return None 