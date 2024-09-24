import numpy as np
import matplotlib.pyplot as plt
import os


OPT = 9147
# quality = np.array([0.2,0.3,0.4,0.5,0.6,0.7,0.8])
# timeList = [0.0005,0.001,0.0015,0.002,0.0025,0.003,0.0035,0.004,0.0045,0.005,0.0055,0.006]
timeList = np.arange(0.0005, 0.007, 0.0005)  # Adjust upper bound and increment as needed
print(len(timeList))
quality = np.arange(0.1, 0.8, 0.1)  # Adjust upper bound and increment as needed
print(len(quality))
# for i in range(100):
# 	timeList.append(0.0001*i)
# timeList = np.array([0.0005,0.001,0.0015,0.002,0.0025,0.003,0.0035,0.004,0.0045,0.005,0.0055])
print(len(timeList))
respath = "./DATA/DATASET/trace_file/large_scale/large_1_LS1"

if __name__=="__main__":
	fileNames = os.listdir(respath)
	# print(fileNames)
	fileToReads = [fileName for fileName in fileNames]
	print(fileToReads)
	resTable = np.zeros((13,7),dtype=float)
	for fileToRead in fileToReads:
		QualityTimeTable = []
		fileNameFul = os.path.join(respath,fileToRead)
		with open(fileNameFul,'r') as f:
			lines = f.readlines()
		for line in lines:
			t, val = line.split(',')
			t = float(t)#/100
			q = (OPT-float(val))/OPT
			QualityTimeTable.append((t,q))

		for row in range(13):
			for col in range(7):
				for item in QualityTimeTable:
					if item[0]<=timeList[row] and item[1]<=quality[col]:
						resTable[row][col]+=1
						break
	print(resTable)
	q1 = resTable[:,0]/100
	q2 = resTable[:,2]/100
	q3 = resTable[:,4]/100
	q4 = resTable[:,6]/100
	plt.plot(timeList,q1,'-r',label="OPT")
	plt.plot(timeList,q2,'-b',label="30%")
	plt.plot(timeList,q3,'-m',label="50%")
	plt.plot(timeList,q4,'-y',label="70%")
	plt.legend()
	plt.xlabel("Run time(s)")
	plt.ylabel("P(solve)")
	plt.title("QRTD for large_1")
	plt.show()

	t1 = resTable[1,:]/100
	t2 = resTable[3,:]/100
	t3 = resTable[5,:]/100
	t4 = resTable[7,:]/100
	plt.plot(quality*100,t1,'-r',label="0.001s")
	plt.plot(quality*100,t2,'-b',label="0.002s")
	plt.plot(quality*100,t3,'-m',label="0.003s")
	plt.plot(quality*100,t4,'-y',label="0.004s")
	plt.legend()
	plt.xlabel("Solution Quality(%)")
	plt.ylabel("P(solve)")
	plt.title("SQD for large_1")
	plt.show()