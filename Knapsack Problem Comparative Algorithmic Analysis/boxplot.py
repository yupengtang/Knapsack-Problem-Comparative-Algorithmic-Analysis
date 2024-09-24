

import os
import pandas as pd
respath = './DATA/DATASET/trace_file/sol/large_scale/large_1_LS1'
fileNames = os.listdir(respath)
fileToReads = [fileName for fileName in fileNames]
print(fileToReads)
arr = []
for fileToRead in fileToReads:
    fileNameFul = os.path.join(respath, fileToRead)
    with open(fileNameFul, 'r') as f:
        lines = f.readlines()
        arr.append(int(lines[0][:-3]))

print(arr)
df = pd.DataFrame(arr,columns=['large_3'])
df.to_csv('boxplot3.csv',index= False)