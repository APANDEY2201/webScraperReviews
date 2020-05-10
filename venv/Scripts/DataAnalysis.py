import numpy as np
import csv
import pandas as pd
from sklearn.cluster import KMeans

# ----------------------------------------------------------------------------
# Data imports
# ----------------------------------------------------------------------------

csvFileName1 = 'Master_Data_Milestone1_Fitted.csv' #Master_Data_Milestone1_Small_for_training.csv'
analysisDataSource = list(csv.reader(open(csvFileName1, encoding='utf-8'), delimiter='|'))  # CSV file to 2 dimensional list of string

csvFileName2 = 'Orgs_Data_Milestone1.csv' #Master_Data_Milestone1_Small_for_training.csv'
analysisOrgData = list(csv.reader(open(csvFileName2, encoding='utf-8'), delimiter='|'))  # CSV file to 2 dimensional list of string

dataFrame = pd.DataFrame(analysisDataSource[1:],columns=analysisDataSource[0])
dataFrameOrg = pd.DataFrame(analysisOrgData[1:],columns=analysisOrgData[0])

# ----------------------------------------------------------------------------
# Data formatting
# ----------------------------------------------------------------------------

dataFrame['RvScore'] = dataFrame['RvScore'].replace(to_replace ="NA",value ="-10").replace(to_replace ="  ",value ="-10")
dataFrame['RvScore'] = dataFrame['RvScore'].astype(float)
dataFrame['topic0'] = dataFrame['topic0'].astype(float)
dataFrame['topic1'] = dataFrame['topic1'].astype(float)
dataFrame['topic2'] = dataFrame['topic2'].astype(float)
dataFrame['topic3'] = dataFrame['topic3'].astype(float)
dataFrame['topic4'] = dataFrame['topic4'].astype(float)
dataFrame['topic5'] = dataFrame['topic5'].astype(float)
dataFrame['topic6'] = dataFrame['topic6'].astype(float)
dataFrame['topic7'] = dataFrame['topic7'].astype(float)
dataFrame['topic8'] = dataFrame['topic8'].astype(float)
dataFrame['topic9'] = dataFrame['topic9'].astype(float)

dataFrame['RvScore'] = dataFrame['RvScore'] - 2.5
dataFrame['RvScore2'] = np.where(dataFrame['RvScore'] < 0, "Neg", "Pos")

# ----------------------------------------------------------------------------
# Checking averaged topics in + and - sentiments
# ----------------------------------------------------------------------------

# print(dataFrame)
#
# print(dataFrame['RvScore2'].describe())
#
# print(dataFrame.iloc[2,10:20])

posDistribution = [0 for i in range(0,10)]
negDistribution = [0 for i in range(0,10)]

cntPos = 0
cntNeg = 0
for index, row in dataFrame.iterrows():
    if row['RvScore2'] == "Pos":
        cntPos = cntPos + 1
        posDistribution = posDistribution + row[10:20]
    if row['RvScore2'] == "Neg":
        cntNeg = cntNeg + 1
        negDistribution = negDistribution + row[10:20]

posDistribution = posDistribution / cntPos
negDistribution = negDistribution / cntNeg

# print(posDistribution)
# print(negDistribution)

# ----------------------------------------------------------------------------
# Clustering
# ----------------------------------------------------------------------------

noOfClusters = 5

dataFramePos = dataFrame[dataFrame['RvScore2']=="Pos"]
dataFrameNeg = dataFrame[dataFrame['RvScore2']=="Neg"]

dataFrame_KMeans = dataFrame.iloc[:,10:20]
dataFramePos_KMeans = dataFramePos.iloc[:,10:20]
dataFrameNeg_KMeans = dataFrameNeg.iloc[:,10:20]

# print(dataFrame_KMeans.head(20))

kmeans_df = KMeans(n_clusters=noOfClusters, random_state=0).fit(dataFrame_KMeans)
dataFrame['Cluster'] = kmeans_df.labels_

print(dataFrame)