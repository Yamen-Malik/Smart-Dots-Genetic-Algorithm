import pygame
from brain import Brain
dot_raduis = 4
dot_color = pygame.Color("black")
velocity_limit = 3
best_color = pygame.Color("green")
class Dot():
    position = [0,0]
    velocity = [0,0]
    acceleration = [0,0]
    is_dead = False
    is_best = False
    reached_target = False
    fitness = 0

    def __init__(self, position, screen, target_position , color = dot_color):
        self.position = position
        self.screen = screen
        self.brain = Brain(1000)
        self.target_position = target_position
        self.color = color

    def Move(self):
        """
            Moves the dot on the screen by taking a direction from the brain
                (works only if the dot is alive)
        """
        if not self.is_dead:
            direction = self.brain.GetNextDirection()
            if direction == False:
                #* if the brain has no directions left kill the dot
                self.Kill()
                return
            #*move
            #// self.acceleration = [self.acceleration[i] + direction[i] for i in range(len(self.acceleration))]
            self.acceleration = direction
            self.velocity = [max(-velocity_limit,min(velocity_limit,self.velocity[i] + self.acceleration[i])) for i in range(len(self.velocity))]
            self.position = [self.position[i]+self.velocity[i] for i in range(len(self.velocity))]
            #*Kill the dot if it hit the screen walls or the target
            if self.position[0] >= self.screen.get_width() or self.position[0] <= 0 or self.position[1] >= self.screen.get_height() or self.position[1] <= 0:
                self.Kill()
            if self.GetDistanceFromTarget() <=5:
                self.reached_target = True
                self.Kill()
            #* die when hit obstacle (test)
            if self.position[0] >= (self.screen.get_width()/2 - 150) and self.position[0] <= (self.screen.get_width()/2 + 150) and self.position[1] >= (self.screen.get_height()/2 - 5) and self.position[1] <= (self.screen.get_height()/2 + 5):
                self.Kill()

    def Draw(self):
        if self.is_best:
            pygame.draw.circle(self.screen, best_color, list(map(lambda x:int(x),self.position)), dot_raduis)
            return
        #// pygame.draw.circle(self.screen, self.color, self.position, dot_raduis)
        pygame.draw.circle(self.screen, self.color, list(map(lambda x:int(x),self.position)), dot_raduis)
    
    def Kill(self):
        self.is_dead = True
        self.velocity = [0,0]

    def CalculateFitness(self):
        self.fitness = 0
        if self.reached_target:
            self.fitness = 1/16 * 10000/(self.brain.steps^2)
        else:
            self.fitness = 1/(self.GetDistanceFromTarget() ^ 2)
        return self.fitness

    def GetDistanceFromTarget(self):
        """
            Returns the distance between the dot and the target
        """
        return abs(int(self.position[0] - self.target_position[0])) + abs(int(self.position[1] - self.target_position[1]))

    def GetBaby(self, position):
        """
            Returns a new dot (baby) with the same the brain values
        """
        baby = Dot(position, self.screen, self.target_position)
        baby.brain = self.brain.Clone()
        return baby

