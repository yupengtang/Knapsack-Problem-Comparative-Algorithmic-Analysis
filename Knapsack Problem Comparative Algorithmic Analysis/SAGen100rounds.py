from SA import readFile,SA_once
import numpy as np

if __name__=='__main__':
	
	'''
	parser = argparse.ArgumentParser(prog='CSE6140',
                    description='This program experiment different algorithms to solve Knapsack Problem',
                    epilog='Follow the rule to input parameters')
	parser.add_argument('-inst','--inst')
	parser.add_argument('-alg','--alg',choices=['BnB','Aprox','LS1','LS2'])
	parser.add_argument('-time','--time',type=int)
	parser.add_argument('-seed','--seed',type=int)
	args = parser.parse_args()
	'''
	N,W,valueList,weightList = readFile('./DATA/DATASET/large_scale/large_1')
	print(N)
	print(W)
	for i in range(100):
		bestVal,bestItems = SA_once(N,W,np.array(valueList,dtype=float),np.array(weightList,dtype=float),3,i,'./DATA/DATASET/large_scale/large_1')
		print("round:",i)

	N,W,valueList,weightList = readFile('./DATA/DATASET/large_scale/large_3')
	print(N)
	print(W)
	for i in range(100):
		bestVal,bestItems = SA_once(N,W,np.array(valueList,dtype=float),np.array(weightList,dtype=float),10,i,'./DATA/DATASET/large_scale/large_3')
		print("round:",i)
	