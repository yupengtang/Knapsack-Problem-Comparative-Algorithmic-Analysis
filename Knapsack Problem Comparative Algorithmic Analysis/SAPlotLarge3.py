import numpy as np
import matplotlib.pyplot as plt
import os


OPT = 28857
quality = np.array([0,0.01,0.02,0.03,0.04,0.05,0.06])
timeList = np.array([1,2,3,4,5,6,7,8,9,10])
respath = "./DATA/DATASET/large_scale/large_3_SA"

if __name__=="__main__":
	fileNames = os.listdir(respath)
	fileToReads = [fileName for fileName in fileNames if fileName[-5:]=="trace"]
	resTable = np.zeros((10,7),dtype=float)
	for fileToRead in fileToReads:
		QualityTimeTable = []
		fileNameFul = os.path.join(respath,fileToRead)
		with open(fileNameFul,'r') as f:
			lines = f.readlines()
		for line in lines:
			t, val = line.split()
			t = float(t)/1000
			q = (OPT-float(val))/OPT
			QualityTimeTable.append((t,q))

		for row in range(10):
			for col in range(7):
				for item in QualityTimeTable:
					if item[0]<=timeList[row] and item[1]<=quality[col]:
						resTable[row][col]+=1
						break
	print(resTable)
	print("Total instance is:",len(fileToReads))
	q1 = resTable[:,0]/len(fileToReads)
	q2 = resTable[:,2]/len(fileToReads)
	q3 = resTable[:,4]/len(fileToReads)
	q4 = resTable[:,6]/len(fileToReads)
	plt.plot(timeList,q1,'-r',label="OPT")
	plt.plot(timeList,q2,'-b',label="2%")
	plt.plot(timeList,q3,'-m',label="4%")
	plt.plot(timeList,q4,'-y',label="6%")
	plt.legend()
	plt.xlabel("Run time(s)")
	plt.ylabel("P(solve)")
	plt.title("QRTD for large_3")
	plt.show()

	t1 = resTable[1,:]/len(fileToReads)
	t2 = resTable[3,:]/len(fileToReads)
	t3 = resTable[5,:]/len(fileToReads)
	t4 = resTable[7,:]/len(fileToReads)
	plt.plot(quality*100,t1,'-r',label="2s")
	plt.plot(quality*100,t2,'-b',label="4s")
	plt.plot(quality*100,t3,'-m',label="6s")
	plt.plot(quality*100,t4,'-y',label="8s")
	plt.legend()
	plt.xlabel("Solution Quality(%)")
	plt.ylabel("P(solve)")
	plt.title("SQD for large_3")
	plt.show()



