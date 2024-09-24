import argparse
import time
import numpy as np
import copy
import os

def readFileHC(filename):
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



def HC_once(N,W,valueArr,weightArr,cutTime,seed,filename):
	np.random.seed(seed)
	initProb = W/weightArr.sum()+0.0001
	print(initProb)
	initArr = np.random.binomial(1, initProb, size=N)
	
	instanceName = os.path.basename(filename)
	instanceDir = os.path.dirname(filename)
	instanceDir = os.path.join(instanceDir,instanceName+"_HC")
	instanceName = instanceName +"_"+"HC_"+str(cutTime) + "_"+str(seed) 
	if not os.path.exists(instanceDir):
		os.makedirs(instanceDir)

	instanceFileName = os.path.join(instanceDir , instanceName +".sol")
	instanceTraceName = os.path.join(instanceDir , instanceName + ".trace")
	initTime = time.time()
	while initArr@weightArr>W:
		initArr = np.random.binomial(1, initProb, size=N)
	curWeight = initArr@weightArr
	curValue = initArr@valueArr
	curItems = initArr.copy()
	bestVal = curValue
	bestItems = curItems.copy()
	trace = []
	while(True):
		now = time.time()
		timePast = now-initTime
		if(timePast>=cutTime):
			print("timeout,HC done",)
			break
		curWeight = curItems@weightArr
		curValue = curItems@valueArr
		bestImprove=0
		tmpBestItems = None
		for i in range(N):
			tmpItems = curItems[:]
			if tmpItems[i]==0 and tmpItems@weightArr+weightArr[i]<=W:
				tmpItems[i] = 1
				if tmpItems@valueArr>curValue:
					if tmpItems@valueArr > bestImprove:
						bestImprove = tmpItems@valueArr
						tmpBestItems = tmpItems[:]
		if bestImprove > 1e-8:
			curItems = tmpBestItems[:]
			if curItems@valueArr>bestVal:
				bestVal = curItems@valueArr
				bestItems = curItems[:]
				trace.append([(time.time()-initTime)*1000,bestVal])
		else:
			while True:
				if(time.time()-initTime>=cutTime):
					print("timeout,hc done",)
					break
				curItems = np.random.binomial(1, initProb, size=N)
				if curItems@weightArr<W:
					break

	#write solution file
	print(instanceFileName)
	with open(instanceFileName,'w+') as f:
		f.writelines(str(bestVal)+'\n')
		firstFlag = True
		for i in range(N):
			if bestItems[i]:
				if firstFlag:
					f.write(str(i))
					firstFlag = False
				else:
					f.write(","+str(str(i)))

	#Write trace file
	with open(instanceTraceName,"w+") as tf:
		for traceItem in trace:
			tf.write(str(traceItem[0])+" "+str(traceItem[1])+"\n")
	return bestVal,bestItems


def HC(fileName,cutOff,seed):
	N,W,valueList,weightList = readFileHC(args.inst)
	bestVal,bestItems = HC_once(N,W,np.array(valueList,dtype=float),np.array(weightList,dtype=float),cutOff,seed,fileName)
	print("Best val:",bestVal)



if __name__=='__main__':
	parser = argparse.ArgumentParser(prog='CSE6140',
                    description='This program experiment different algorithms to solve Knapsack Problem',
                    epilog='Follow the rule to input parameters')
	parser.add_argument('-inst','--inst')
	parser.add_argument('-alg','--alg',choices=['BnB','Aprox','HC','SA'])
	parser.add_argument('-time','--time',type=int)
	parser.add_argument('-seed','--seed',type=int)
	args = parser.parse_args()
	HC(args.inst,args.time,args.seed)
