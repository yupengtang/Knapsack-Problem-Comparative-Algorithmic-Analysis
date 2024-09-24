import os
import time
from queue import PriorityQueue
import argparse


def readFileBnB(filename):
    valueList = []
    weightList = []
    N=0
    W=0
    with open(filename,'r') as f:
        line = f.readline()
        firstword, secondword = line.split()
        N = int(firstword)
        W = int(secondword)
        i = 0
        while(i<N):
            line = f.readline()
            #if not line:
                #break
            firstword,secondword = line.split()
            valueList.append(float(firstword))
            weightList.append(float(secondword))
            i+=1
    return N,W,valueList,weightList 

class Item:
    def __init__(self, val, weight,id):
        self.val = val
        self.weight = weight
        self.id = id

class TreeNode:
    def __init__(self, level, weight, val, itemSelected):
        self.level = level
        self.val = val
        self.weight = weight
        self.itemSelected = itemSelected

    def __lt__(self, another):
        return self.weight>another.weight


# Function to calculate the upper bound of the maximum profit (bound) for a node.
def upperBound(treeNode, N, W, itemArr):
    valBound = treeNode.val
    curWeight = treeNode.weight
    idx = treeNode.level + 1
    # Continue adding items while there's capacity
    while (idx < N and curWeight + itemArr[idx].weight <= W):
        curWeight += itemArr[idx].weight
        valBound += itemArr[idx].val
        idx += 1
    # If items remain, use fractional knapsack for the next item to estimate upper bound
    if (idx < N):
        valBound += (W - curWeight) * (itemArr[idx].val / itemArr[idx].weight)
    return valBound

def writeOutput(fileName,cutOff,minVal,bestPath,timeList,bestValList):
    instanceName = os.path.basename(fileName)
    instanceDir = os.path.dirname(fileName)
    filename = instanceName +"_BnB_"+str(cutOff)
    resDir = os.path.join(instanceDir,instanceName+"_BnB")
    if not os.path.exists(resDir):
        os.makedirs(resDir)
    solFile = os.path.join(resDir,filename+".sol")
    traceFile = os.path.join(resDir,filename+".trace")

    with open(solFile, 'w') as file:
        file.write(str(minVal)+"\n")
        firstFlag = True
        for i in range(len(bestPath)):
            if firstFlag:
                file.write(str(bestPath[i]))
                firstFlag = False
            else:
                file.write(","+str(bestPath[i]))

    with open(traceFile,'w') as f:
        for i in range(len(bestValList)):
            f.write(str(timeList[i])+","+str(bestValList[i])+"\n")


# Main function for the branch and bound knapsack algorithm.
def knapsack_branch_bound(itemArr, W, N,cutOff):
    #if not os.path.exists(output_dir):
        #os.makedirs(output_dir)
    pq = PriorityQueue()
    initSelected = []
    treeNode = TreeNode(-1, 0, 0, initSelected)
    pq.put(treeNode)
    minVal = 0
    bestPath = None
    startTime = time.time()  
    timeList = []
    bestValList = []
    while not pq.empty():
        if time.time()-startTime>cutOff:
            break
        vNode = pq.get()
        vBound = upperBound(vNode, N, W, itemArr)  
        if vBound <= minVal:
            continue
        uLevel = vNode.level + 1
        if uLevel < N:
            if vNode.weight+itemArr[uLevel].weight<=W:
                uitemSelected = vNode.itemSelected.copy()
                uitemSelected.append(itemArr[uLevel].id)
                uNode = TreeNode(uLevel, vNode.weight+itemArr[uLevel].weight,vNode.val+itemArr[uLevel].val,uitemSelected)
                pq.put(uNode)
                if uNode.val > minVal:
                    minVal = uNode.val
                    bestPath = uNode.itemSelected
                    timeList.append((time.time()-startTime)*1000)
                    bestValList.append(minVal)

            uNodePeer = TreeNode(uLevel, vNode.weight,vNode.val,vNode.itemSelected.copy())
            pq.put(uNodePeer)
    return minVal,bestPath,timeList,bestValList


def BnB(fileName,cutOff):
    N,W,valueList,weightList = readFileBnB(fileName)
    itemArr = []
    for i in range(N):
        itemArr.append(Item(valueList[i],weightList[i],i))
    itemArr.sort(key=lambda x: x.val / x.weight, reverse=True)  
    minVal,bestPath,timeList,bestValList = knapsack_branch_bound(itemArr, W,N,cutOff)
    bestPath.sort()
    writeOutput(fileName,cutOff,minVal,bestPath,timeList,bestValList)


if __name__=='__main__':
    parser = argparse.ArgumentParser(prog='CSE6140',
                    description='This program experiment different algorithms to solve Knapsack Problem',
                    epilog='Follow the rule to input parameters')
    parser.add_argument('-inst','--inst')
    parser.add_argument('-alg','--alg',choices=['BnB','Approx','HC','SA'])
    parser.add_argument('-time','--time',type=int)
    parser.add_argument('-seed','--seed',type=int)
    args = parser.parse_args()
    BnB(args.inst,args.time)