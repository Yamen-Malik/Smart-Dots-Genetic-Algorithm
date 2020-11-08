import dot, random
class Population():
    total_fitness = 0
    gen = 1
    best_dot_index = 0
    minsteps = None
    def __init__(self, size, initial_position, screen, target_position):
        """
            Makes a new dots population
                size(int): the size of the population
                initial_position(x,y): the x and y values to create the dots at
                screen : pygame screen to draw the dots at
                target_position(x,y): the x and y value of the dots target
        """
        self.size = size
        self.dots = []
        self.initial_position = initial_position
        for _ in range(size):
            self.dots.append(dot.Dot(initial_position, screen, target_position))
    
    def Draw(self):
        """
            Draws all the dots of the population at the screen
        """
        for dot in self.dots:
            dot.Draw()

    def Move(self):
        """
            Updates and moves all the dots in the population
        """
        for dot in self.dots:
            if not self.minsteps == None and dot.brain.steps >= self.minsteps:
                dot.Kill()
                continue
            dot.Move()
    
    def AllDotsDead(self):
        """
            Returns True if all population dots are dead and False if not
        """
        for dot in self.dots:
            if not dot.is_dead:
                return False
        return True
    
    def CalculateFitness(self):
        """
            Calculates the fitness of all the dots and store it
        """
        self.total_fitness = 0
        for dot in self.dots:
            self.total_fitness += dot.CalculateFitness()
    
    def NaturalSelection(self):
        """
            Starts the natural selection by choosing the best dots and getting thier babies and mutate them to create new dots
        """
        self.gen +=1
        new_dots = []
        #* get best dot and add its baby to the new gen without mutation
        self.SelectBestDot()
        new_dots.append(self.dots[self.best_dot_index].GetBaby(self.initial_position))
        new_dots[0].is_best = True
        for _ in range(1, len(self.dots)):
            #*skiped 1 because we aleadry added one (the best dot)
            #*Get parent then get its baby and add it to the new gen
            new_dots.append(self.GetParent().GetBaby(self.initial_position))
        
        #*replace the old gen with the new one and mutate the new gen
        self.dots = new_dots.copy()
        self.Mutate()
        #*Reverse the list to draw the best dot last (on top)
        #? did this break it?
        self.dots = self.dots[::-1]

    def GetParent(self):
        """
            Returns a dot from the dots list to be a parent in the new ge
        """
        #*get a random point from 0 to total_fitness to use it as a pointer to get the parent
        random_fitness = random.random() * self.total_fitness
        running_fitness = 0
        #*find the dot that has the "pointer" pointing at its "field"
        for dot in self.dots:
            running_fitness += dot.fitness
            if running_fitness >= random_fitness:
                return dot

    def Mutate(self):
        """
            Mutates all the dots in the current gen
        """
        for i in range(1, len(self.dots)):
            self.dots[i].brain.Mutate(self.minsteps)

    def SelectBestDot(self):
        """
            Sets the value of the best_dot_index by searching for the dot with the greatest fitness
            and sets the minsteps value if the best dot reached the target            
        """
        #*search for the best dot
        max_ = 0
        best_index = 0
        for i in range(len(self.dots)):
            if self.dots[i].fitness > max_:
                best_index = i
                max_ = self.dots[i].fitness
        self.best_dot_index = best_index
        #* set the minsteps if the best dot reached the target
        if self.dots[best_index].reached_target:
            self.minsteps = self.dots[best_index].brain.steps
            print("steps: ", self.minsteps)
