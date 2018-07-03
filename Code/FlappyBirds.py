import pygame, random, sys
from pygame.locals import *
import FlappyGameAI as fp

pygame.init()

window_height=600 
window_width=1200

blue = (0,0,255)
black = (0,0,0)
green = (0,255,0)
white = (255, 255, 255)

fps = 10000
level = 0
addnewflamerate = 20

constant1=0

mainClock = pygame.time.Clock()
Canvas = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Flappy Birds')

font = pygame.font.SysFont(None, 48)
scorefont = pygame.font.SysFont(None, 30)

class FlappyBird:
    speed = 10
    
    def __init__(self):

        self.image = load_image('FlappyBird.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.left = window_width/2-200
        self.imagerect.top = window_height/2  

    def update(self):

        if moveup:
            if self.imagerect.top>0:
                self.imagerect.top -= self.speed

        if gravity:
            if self.imagerect.bottom<window_height:
                self.imagerect.bottom += self.speed
 

class Pipe:
    speed = 10
    
    def __init__(self,y):
        self.x = window_width
        self.y = y

    def changePosition(self):
        self.x-=self.speed

    def getPosition(self):
        return self.x
    
    def getPosition1(self):
        return self.y

    def drawPipe(self):
        pygame.draw.rect(Canvas, green, (self.x,0,100,self.y))
        pygame.draw.rect(Canvas, green, (self.x,self.y+200,100,window_height))
        pygame.draw.rect(Canvas, black, (self.x,0,100,self.y),1)
        pygame.draw.rect(Canvas, black, (self.x,self.y+200,100,window_height),1)
        
        
def load_image(imagename):
    return pygame.image.load(imagename)

def drawtext(text, font, surface, x, y):        #to display text on the screen
    textobj = font.render(text, 1, white)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

def terminate():        
    pygame.quit()
    sys.exit()

def updatePipes():
    for pipe in pipes:
        pipe.changePosition()
    if pipes!=[] and pipes[0].getPosition()<=-300:
        del pipes[0]


def drawPipes():
    for pipe in pipes:
        pipe.drawPipe()
    
def collision():
    #if player.imagerect.top<=0:
        #return True
    #if player.imagerect.bottom>=window_height:
        #return True
    for pipe in pipes:
        if player.imagerect.right>=pipe.getPosition() and player.imagerect.left<pipe.getPosition()+100 and (player.imagerect.top<pipe.getPosition1() or player.imagerect.bottom>pipe.getPosition1()+200):
            return True
    return False

def nearestPipe():
    if pipes == []:
        return [0,-10]
    else:
        for pipe in pipes:
            if player.imagerect.left<pipe.getPosition():
                if player.imagerect.right>pipe.getPosition():
                    return [10*((player.imagerect.top+player.imagerect.bottom)/2-(pipe.getPosition1()+100))/window_height,-10*(player.imagerect.right+(pipe.getPosition()-player.imagerect.right))/window_width]
                else:
                    return [10*((player.imagerect.top+player.imagerect.bottom)/2-(pipe.getPosition1()+100))/window_height,-10*(pipe.getPosition())/window_width]
        return [0,-10]

def perform_cross_breed(neurons):
    cross_breed_neurons = []
    for i in range(len(neurons)-1):
        j=i+1
        while j<len(neurons):
            cross_breed_neurons.append([0,fp.crossBreed(neurons[i][1],neurons[j][1])])
            j+=1
    return cross_breed_neurons

def perform_mutation(neurons):
    for neuron in neurons:
        for i in range(5):
            fp.mutate(neuron[1])

topscore = 0
gameWon = False
neurons = []
generation = 0
bestFlappyBird=[]
population = 10
for i in range(population):
    neurons.append([0,fp.neural_network()])
    
while True:
    
    for species in range(population):
        player = FlappyBird()
        loops = 0
        pipes = []
        moveup = gravity = True
        gameExit = False
        gameStart = True
        score = 0
        population = 10
        #Level1 = [200,300,400,200,100,300,400,0,300,200]
        Level1 = [200,300,400,100]
        fps = 10000
        while not collision() or gameStart:
            score+=1+1.5*(1-nearestPipe()[0]/10)
            if score>300:
                fps = 50
            gameStart=False
            command = neurons[species][1].prediction(nearestPipe())        
            if command is "UP":
                moveup = True
                gravity = False
            else:
                moveup = False
                gravity = True
                
            #print(nearestPipe())
            """    
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()

                if event.type == KEYDOWN:
                    
                    if event.key == K_UP:
                        moveup = True
                        gravity = False



                if event.type == KEYUP:

                    if event.key == K_UP:
                        moveup = False
                        gravity = True
                        
                    if event.key == K_ESCAPE:
                        terminate()
            """
                    
            player.update()
            updatePipes()

            

            if loops%60 == 0:
                if Level1!=[]:
                    pipes.append(Pipe(Level1[0]))
                    del Level1[0]
                    Level1.append(int((random.random()*10000))%400)
                if pipes==[]:
                    gameWon=True
                    break
            
            loops+=1
            Canvas.fill(black)
            Canvas.blit(player.image, player.imagerect)
            drawPipes()
            drawtext('Generation : %s | Species : %s | Score : %s | Top score : %s' %(generation+1,species+1,int(score), int(topscore)), scorefont, Canvas, 350,  100)
            pygame.display.update()
            mainClock.tick(fps)
        neurons[species][0] = score    
        if score>topscore:
            topscore = score
            bestFlappyBird = [generation,species,score,neurons[species][1].getLayers()]
            constant1=fp.constant
        if command is "UP" and player.imagerect.bottom>window_height-50:
            fp.constant+=0.075
        elif command is "No Command" and player.imagerect.top<50:
            fp.constant-=0.075
    for i in range(population):
        j = i
        maxx,index = neurons[j],j
        while j<population:
            if neurons[j][0]>maxx[0]:
                maxx = neurons[j]
                index = j
            j+=1
        neurons[index] = neurons[i]
        neurons[i] = maxx
    if neurons[3][0]<250:
        neurons[3][1] = fp.neural_network()
    if neurons[2][0]<250:
        neurons[2][1] = fp.neural_network()
    t=neurons[0:4].copy()
    neurons=perform_cross_breed(neurons[0:2])+perform_cross_breed([neurons[int(random.random()*10)%10],neurons[int(random.random()*10)%10]])+perform_cross_breed([neurons[int(random.random()*10)%10],neurons[int(random.random()*10)%10]])+perform_cross_breed([neurons[int(random.random()*10)%10],neurons[int(random.random()*10)%10]])+[neurons[int(random.random()*10)%10]]+[neurons[int(random.random()*10)%10]]
    neurons = perform_cross_breed(neurons[0:5])+perform_cross_breed(neurons[5:10])+perform_cross_breed(neurons[0:5])+neurons[0:5]
    perform_mutation(neurons)
    neurons+=t
    generation+=1
    print(bestFlappyBird)
    print(constant1)
                

            
