class Stack:
    def __init__(self):
        self.stack = []
        
    def push(self, item):
        self.stack.append(item)
        
    def top(self):
        return self.stack[-1]
    
    def pop(self):
        return self.stack.pop()
    
    def is_empty(self):
        return (len(self.stack) == 0)
    
    def empty(self):
        self.stack = []
    
    def size(self):
        return len(self.stack)