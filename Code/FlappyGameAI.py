import numpy as np
import math,random

constant = 5.5

def randomNumber(t):
    return int(random.random()*100)%t

def relu(arr):
    #print(arr)
    for i in range(len(arr)):
        arr[i] = math.log(1+math.exp(arr[i]))
    return arr

def crossBreed(parent1,parent2):
    parentLayers = [parent1.getLayers(),parent2.getLayers()]
    child1 = neural_network()
    arr=[]
    for i in range(len(parentLayers[0])):
        arr.append(parentLayers[randomNumber(2)][i])
    child1.modifyLayers(arr)
    #child1.modifyLayers([parentLayers[randomNumber(2)][0],parentLayers[randomNumber(2)][1],parentLayers[randomNumber(2)][2]])
    #child2 = neural_network([parentLayers[randomNumber(2)][0],parentLayers[randomNumber(2)][1],parentLayers[randomNumber(2)][2]])
    return child1

def mutate(child):
    layers = child.getLayers()
    i = randomNumber(len(layers))
    j = randomNumber(len(layers[i]["weights"]))
    k = randomNumber(len(layers[i]["weights"][j]))
    layers[i]["weights"][j][k] = 2*random.random()-1
    layers[i]["biases"][k] = 2*random.random()-1
    child.modifyLayers(layers)



    

class neural_network:

    def __init__(self):
        
        self.layers = [{"weights":2*np.random.random((2,6))-1,"biases":2*np.random.random(6)-1},
                       {"weights":2*np.random.random((6,1))-1,"biases":2*np.random.random(1)-1}]
        #print(self.layers)

    def modifyLayers(self,layers):
        self.layers = layers
        #print(self.layers)
    
    def getLayers(self):
        return self.layers

    def prediction(self,inputt):
        output=None
        previousLayer = np.array(inputt)
        for layer in self.layers:
            previousLayer = relu(previousLayer.dot(layer["weights"]) + layer["biases"])
        #print(previousLayer)
        if previousLayer>constant:
            return "UP"
        else:
            return "No Command"


"""  
nn=neural_network()

while True:
    mutate(nn)
    print("Input numbers")
    print(nn.prediction(list(map(float,input().split()))))
"""   
    
    



        
        
