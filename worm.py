'''
worm.py

Author: Elijah Theander
Project: Wormvolution Python Edition

Created November 2, 2023
'''

#python standard library
from random import(
    randint,
    random
)


#Third Party Packages
from PyQt5.QtGui import(
    QColor
)

class Worm(object):
    '''
    Worm Class
    
    holds genes, color, and positional data
    allows reproduction and mutation
    '''
    genes = ['M','M','Z','Z','<','<','>','>','U','U','R','R','D','D','L','L','H','H','A','v','r',
             'e','E','C','0','-0','1','-1','2','-2','3','-3','4','-4','5','-5','6','-6'] #the genes
    facings = list('URDL') #directions head can face
    mutationRate = .2 #Likeliness of mutation on reproduction modifier

    def __init__(self, newDNA, xPos, yPos, facing = None, color = QColor(255,0,0) ):

        self.length = len(newDNA)
        self.body = self.create_list_nest(self.length)
        self.dna = newDNA

        #Create Body
        for i in range(0,self.length):
            self.body[i] = [xPos,yPos] 

        #set baseEnergy based on length of dna
        self.baseEnergy = int(400 +(self.length * 200))
        self.energy = self.baseEnergy
        
        #Generate initial facing
        if(facing == None):
            random_index = randint(0,3) - 1
            self.facing = self.facings[random_index]
        else:
            self.facing = facing

        #Set instance variables
        self.dnaStep = 0
        self.age = 0
        self.maxAge = int(200 + (self.length * 200))
        self.timeStep = 0
        self.blocked = False
        self.color = color
        self.curled = self.length - 1
        self.reproduced = False
        self.lastCondition = 0
        self.hasElse = False

    
    def create_list_nest(self,size):
        '''
        creates a nested list of size size.
        '''
        list_nest = []

        for i in range(0,size):
            list_nest.append([])
        
        return list_nest
    
    #-----------------------------------------------
    # MUTATORS
    #-----------------------------------------------

    def set_mutation_rate(self, value):
        self.mutationRate = value
    
    def set_last_condition(self,value):
        self.lastConditoin = value

    def set_blocked(self, blocked):
        self.blocked = blocked
    
    def set_color(self,color):
        self.color = color

    def time_step(self):
        self.timeStep += 1

    def set_time_step(self,value):
        self.timeStep = value
    
    def reset_time_step(self):
        self.timeStep = 0

    def change_facing(self, newFacing):
        self.facing = newFacing
        self.reset_time_step()

    def spend_energy(self, spend):
        self.energy = self.energy - spend
    
    def set_energy(self,value):
        self.energy = value

    def ageup(self):
        self.age += 1

    def go_to_last_condition(self):
        self.dnaStep = self.lastCondition

    def go_to_step(self,step):
        self.dnaStep = step % self.length

    def next_step(self):
        self.dnaStep = (self.dnaStep + 1) % self.length


    #-----------------------------------------------
    # ACCESSORS
    #-----------------------------------------------

    def get_max_age(self):
        return self.maxAge
    
    def get_base_energy(self):

        return self.baseEnergy
    
    def is_blocked(self):
        return self.blocked
    
    def get_color(self):
        return self.color
    
    def get_time_step(self):
        return self.timeStep
    
    def get_facing(self):
        return self.facing
    
    def get_energy(self):
        return self.energy
    
    def get_dna(self):
        return self.dna
    
    def get_step(self):
        return self.dnaStep
    
    def get_body(self):
        return self.body
    
    #-----------------------------------------------
    # Class Methods
    #-----------------------------------------------

    def move(self,nextPoint):
        '''
        Moves the worm to the next point along its path
        '''

        lastPoint = self.body[0]
        lastX = lastPoint[0]
        lastY = lastPoint[1]

        nextX = nextPoint[0]
        nextY = nextPoint[1]

        self.body[0] = [nextX,nextY]

        for i in range(1, len(self.body)):
            nextX = self.body[i][0]
            nextY = self.body[i][1]

            self.body[i] = [lastX,lastY]

            lastX = nextX
            lastY = nextY
        self.reset_time_step()

    def sleep(self):
        self.reset_time_step()

    def turn(self, dir):
        'Updates facing based on current facing and direction input'

        match self.facing:

            case 'U':

                if dir == 'L':
                    self.facing = 'L'
                else:
                    self.facing = 'R'
            
            case 'R':

                if dir == 'L':
                    self.facing = 'U'
                else:
                    self.facing = 'D'

            case 'D':
                
                if dir == 'L':
                    self.facing = 'R'
                else:
                    self.facing = 'L'
            
            case 'L':

                if dir == 'L':
                    self.facing = 'D'
                else:
                    self.facing = 'U'
            
        self.reset_time_step()

    def reproduce(self, point, colorVariance):
        '''
        Create and return a new worm'''
        self.reproduced = True
        newDna = []
        newElse = False

        newR = self.color.red()/255.0
        newG = self.color.green()/255.0
        newB = self.color.blue()/255.0

        for j in range(0,self.length):

            if((random()) < (self.mutationRate/self.length)): #Mutates if true
                
                rand3 = int(random() * 3)
                rand = random()

                if rand < 0.5:
                    rand -= 1
                rand = rand*colorVariance

                match rand3:

                    case 0:

                        newR += rand

                        if newR < 0.2:
                            newR = 0.2
                        elif newR > 1:
                            newR = 1

                    case 1:

                        newG += rand

                        if newG < 0.2:
                            newG = 0.2
                        elif newG > 1:
                            newG = 1

                    case 2:

                        newB += rand

                        if newB < 0.2:
                            newB = 0.2
                        elif newB > 1:
                            newB = 1

                    case _:
                        newR = 0.5
                        newG = 0.5
                        newB = 0.5

                random_index = randint(0,len(self.genes)) - 1
                randGene = self.genes[random_index]

                rand3 = int(random() *3)

                if rand3 == 1: # Add a gene, randomly assign to left or right of original

                    rand2 = int(random() * 2)

                    if ((randGene == 'e') or (self.dna[j] == 'e')):
                        newElse = True

                    if rand2 == 0:
                        newDna.append(randGene)
                        newDna.append(self.dna[j])
                    else:
                        newDna.append(self.dna[j])
                        newDna.append(randGene)
                
                elif( (rand3 == 2) or ((rand3 == 0) and (len(newDna) == 0) and j == self.length - 1)):

                    if randGene == 'e':
                        newElse = True

                    newDna.append(randGene) #Replace a gene
            else:

                if self.dna[j] == 'e':
                    newElse = True
                newDna.append(self.dna[j]) #No mutation happens, copy directly
        
        newFacing = ''

        match self.facing:

            case 'U':
                newFacing = 'R'
            case 'R':
                newFacing = 'L'
            case 'L':
                newFacing = 'U'
            case _:
                newFacing = 'D'

        
        newR = int(newR * 255)
        newG = int(newG * 255)
        newB = int(newB * 255)
        
        newWorm = Worm(newDna, point[0],point[1], newFacing, QColor(newR,newG,newB))

        self.spend_energy(self.baseEnergy)

        newWorm.hasElse = newElse

        return newWorm



'''
-------------------------------------------------------------------------------------------------
                                             TESTING
-------------------------------------------------------------------------------------------------
'''

def main():

    dna = ['M','<','C','3','Z']

    x = 8
    y = 10
    
    w1 = Worm(dna,x,y)

    cvar = 0.75

    print(f'Worm 1 body: {w1.get_body()}')

    w1.move([9,10])
    w1.move([10,10])
    w1.move([11,10])
    w1.move([12,10])
    w1.set_mutation_rate(0.9)

    print(f'Worm 1 has moved: {w1.get_body()}')

    w2 = w1.reproduce([13,11], cvar)

    print(f'Worm 2 is born!')

    print(f'Worm 1 Genes: {w1.get_dna()}')
    print(f'Worm 2 Genes: {w2.get_dna()}')


if __name__ == '__main__':
    main()

