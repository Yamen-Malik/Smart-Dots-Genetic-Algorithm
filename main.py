import pygame, os, sys, dot, population, time

#*load pygame screen
width, height = (800,600)
#* Center the display
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((width,height))

#* Create the target point
target_position = (400, 20)
target = dot.Dot(target_position, screen, target_position, pygame.Color("red"))
target.Kill()
#* Create the dots population
dots = population.Population(1000, (400, 550), screen, target_position)
#* update the app (called every frame)
font = pygame.font.SysFont("arial", 20)
def Update():
    screen.fill(pygame.Color("white"))
    target.Draw()
    #* obstacle test
    pygame.draw.rect(screen, pygame.Color("blue"), (width/2 - 150, height/2-5, 300, 10))
    if dots.AllDotsDead():
        dots.CalculateFitness()
        dots.NaturalSelection()
    else:
        dots.Move()
        dots.Draw()
    #*Write "gen" text
    text = font.render(f"gen: {dots.gen}", True, pygame.Color("black"))
    screen.blit(text, (width - 70, 10))

while True:
    for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		    sys.exit()
    Update()
    pygame.display.flip()
    #// time.sleep(0.001)
