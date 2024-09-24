from SA import SA_once,readFile
import numpy as np
import os


#10 seconds [1,2,3,4,5,8,9,10,11,12,15,16,17,18,19]


if __name__=="__main__":
	fileList = ["large_"+str(i) for i in [1,2,3,4,5,8,9,10,11,12,15,16,17,18,19]]
	largeDir = "./DATA/DATASET/large_scale"
	smallDir = "./DATA/DATASET/small_scale"
	
	for fileName in fileList:
		fileToRead = os.path.join(largeDir,fileName)
		N,W,valueList,weightList = readFile(fileToRead)
		result = []
		for k in range(10):
			bestVal,bestItems = SA_once(N,W,np.array(valueList,dtype=float),np.array(weightList,dtype=float),10,k,fileToRead)
			result.append(bestVal)
		print(fileToRead)
		print("10 rounds average:",np.sum(result)/len(result))
	
	
	fileListLong = ["large_"+str(i) for i in [6,7,13,14,20,21]]
	for fileName in fileListLong:
		fileToRead = os.path.join(largeDir,fileName)
		N,W,valueList,weightList = readFile(fileToRead)
		result = []
		for k in range(10):
			bestVal,bestItems = SA_once(N,W,np.array(valueList,dtype=float),np.array(weightList,dtype=float),60,k,fileToRead)
			result.append(bestVal)
		print(fileToRead)
		print("10 rounds average:",np.sum(result)/len(result))

	fileListSmall = ["small_"+str(i) for i in [1,2,3,4,5,6,7,8,9,10]]
	for fileName in fileListSmall:
		fileToRead = os.path.join(smallDir,fileName)
		N,W,valueList,weightList = readFile(fileToRead)
		result = []
		for k in range(10):
			bestVal,bestItems = SA_once(N,W,np.array(valueList,dtype=float),np.array(weightList,dtype=float),3,k,fileToRead)
			result.append(bestVal)
		print(fileToRead)
		print("10 rounds average:",np.sum(result)/len(result))
