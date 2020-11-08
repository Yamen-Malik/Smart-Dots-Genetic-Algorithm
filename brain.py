import random
class Brain():
    mutation_rate = 0.01
    def __init__(self, directions_number):
        self.steps = 0
        self.directions = []
        self.directions_number = directions_number
        self.GenerateDirections()

    def GenerateDirections(self):
        for _ in range(self.directions_number):
            #// self.directions.append((random.randint(-1,1),random.randint(-1,1)))
            self.directions.append((random.random()*2-1, random.random()*2-1))
    
    def GetNextDirection(self):
        if self.steps >= len(self.directions):
            return False
        direction = self.directions[self.steps]
        self.steps +=1
        return direction

    def Clone(self):
        """
            Returns a new brain with the same values
        """
        clone = Brain(self.directions_number)
        clone.directions = self.directions.copy()
        return clone
    
    def Mutate(self, last_step_index):
        self.directions = self.directions[:last_step_index]
        for i in range(len(self.directions)):
            if random.random() < self.mutation_rate:
                self.directions[i] = (random.random()*2-1, random.random()*2-1)
