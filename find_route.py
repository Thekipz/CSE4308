# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 12:47:10 2019

@author: tyler
"""
import sys


def ReadFile(path):
    mapping = {}
    file_open = open(path,'r')
    for line in file_open:
        word = line.split(' ')
        if(word[0]=="END"):
            break
        distance = int(word[2].replace('\n',''))
        mapping[word[0],word[1]] = distance
        #mapping[word[1],word[0]] = distance
    return mapping

output = ReadFile("input1.txt")

def ReadHeuristic(path):
    heuristic = {}
    file_open = open(path,'r')
    for line in file_open:
        word = line.split(' ')
        if(word[0]=="END"):
            break
        distance = int(word[1].replace('\n',''))
        heuristic[word[0]] = distance
    return heuristic

def SearchDict(dictionary, previous, query, numCreated):
    adjacent = []
    for k in output.keys():
        for j in k:
            if j == query:
                city = "".join(k).replace(query,'')
                node = Node(previous, city, previous.totalDistance, output[k])
                numCreated += 1
                adjacent.append(node)
                #print(output[k]) #distance to adjacent city
                #print(query) #start city
                #print("".join(k).replace(query,'')) #adjacent city name
    return adjacent, numCreated

        


class Node:
    previousNode = None
    totalDistance = 0
    currCity = None
    def __init__(self, previous, curr, total, distance):
        self.previousNode = previous
        self.totalDistance = total + distance
        self.currCity = curr
    
#SearchDict((ReadFile("input1.txt")),Node(None,"London",0,0), "London") 


def reconstructRoute(node):
    route = []
    temp = node
    while(temp.previousNode != None):
        route.append(temp)
        temp = temp.previousNode
    route.append(temp)
    temp = route.pop()
    previous = temp.currCity
    previousDistance = 0
    while(len(route)!= 0):
        temp = route.pop()
        print(previous, "to", temp.currCity, (temp.totalDistance-previousDistance), "km")
        previous = temp.currCity
        previousDistance = temp.totalDistance
        
    
def UniSearch(mapping, start, end):
    closed = []
    fringe = []
    
    fringe.append(Node(None, start, 0, 0))
    numCreated = 0
    maxNodes = len(fringe)
    def loop(numExpanded, numCreated, maxNodes):
        numExpanded += 1
        if(len(fringe)== 0):
            numExpanded-=1
            print("nodes expanded:", numExpanded)
            print("nodes generated:", numCreated)
            print("max nodes:",maxNodes)
            print("distance: infinity")
            print("route:\nnone")
            return
        node = fringe.pop(0)
        
        if(node.currCity == end):
            
            print("nodes expanded:", numExpanded)
            print("nodes generated:", numCreated)
            print("max nodes:",maxNodes)
            print("route:\n")
            reconstructRoute(node)
            return node
        
        if(node.currCity in closed):
            return loop(numExpanded, numCreated, maxNodes)
        else:
            closed.append(node.currCity)
            adjacent, numCreated = SearchDict(mapping, node, node.currCity, numCreated)
           
            while(len(adjacent)!= 0):
                fringe.append(adjacent.pop())
            if (len(fringe)>maxNodes):
                maxNodes = len(fringe)
            fringe.sort(key = lambda x: x.totalDistance)
            
            loop(numExpanded, numCreated, maxNodes)
            #test = fringe.pop()
            #print(test.currCity)
            #print(test.previousNode.currCity)
            
    numExpanded = 0
    loop(numExpanded, numCreated, maxNodes)
    
       
def InfSearch(mapping, start, end, heuristic):
    closed = []
    fringe = []
    
    fringe.append(Node(None, start, 0, 0))
    numCreated = 0
    maxNodes = len(fringe)
    def loop(numExpanded, numCreated, maxNodes, heuristic):
        numExpanded += 1
        if(len(fringe)== 0):
            numExpanded -= 1
            print("nodes expanded:", numExpanded)
            print("nodes generated:", numCreated)
            print("max nodes:",maxNodes)
            print("distance: infinity")
            print("route:\nnone")
            return
        node = fringe.pop(0)
        
        if(node.currCity == end):
            
            print("nodes expanded:", numExpanded)
            print("nodes generated:", numCreated)
            print("max nodes:",maxNodes)
            print("route:\n")
            reconstructRoute(node)
            return node
        
        if(node.currCity in closed):
            return loop(numExpanded, numCreated, maxNodes, heuristic)
        else:
            closed.append(node.currCity)
            adjacent, numCreated = SearchDict(mapping, node, node.currCity, numCreated)
           
            while(len(adjacent)!= 0):
                fringe.append(adjacent.pop())
            if (len(fringe)>maxNodes):
                maxNodes = len(fringe)
            fringe.sort(key = ( lambda x: x.totalDistance + heuristic[x.currCity]))
            loop(numExpanded, numCreated, maxNodes, heuristic)
            #test = fringe.pop()
            #print(test.currCity)
            #print(test.previousNode.currCity)
            
    numExpanded = 0
    loop(numExpanded, numCreated, maxNodes, heuristic)


path = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]
if(len(sys.argv)==4):
    UniSearch((ReadFile(path)),start, end)
if(len(sys.argv)==5):
    heuristic = sys.argv[4]
    InfSearch((ReadFile(path)),start, end, ReadHeuristic(heuristic))


#UniSearch((ReadFile("input1.txt")), "Bremen","Kassel")
#InfSearch((ReadFile("input1.txt")), "Bremen","Kassel",ReadHeuristic("heuristic.txt"))
