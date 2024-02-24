# IMPLEMENTATION OF QUEUE
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("Queue is empty")

    def is_empty(self):
        return len(self.items) == 0
    

# Create an instance of the queue
# queue = CustomQueue()
