import numpy as np
import csv
import pandas as pd
from sklearn.cluster import KMeans
import scipy.stats as stats
import statsmodels.formula.api as sm
from scipy.stats import chisquare
from scipy.stats import chi2_contingency

def ChiTest(contingencyTable):
    stat, p, dof, expected = chi2_contingency(contingencyTable)
    alpha = 0.05
    # print(stat)
    # print('significance=%.3f, p=%.3f' % (alpha, p))
    if p <= alpha:
        return True
        # print('Variables are associated (reject H0)')
    else:
        return False
        # print('Variables are not associated(fail to reject H0)')

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
kmeans_df = KMeans(n_clusters=noOfClusters, random_state=0).fit(dataFrame_KMeans)
dataFrame['Cluster'] = kmeans_df.labels_
kmeans_dfPos = KMeans(n_clusters=noOfClusters, random_state=0).fit(dataFramePos_KMeans)
dataFramePos['Cluster'] = kmeans_dfPos.labels_
kmeans_dfNeg = KMeans(n_clusters=noOfClusters, random_state=0).fit(dataFrameNeg_KMeans)
dataFrameNeg['Cluster'] = kmeans_dfNeg.labels_

# print(dataFrame.head(10))

# print(dataFrameOrg.iloc[:,[0,4,5,6]])

# ----------------------------------------------------------------------------
# Correlation Statistics
# ----------------------------------------------------------------------------

dataFrame = pd.merge(dataFrame, dataFrameOrg.iloc[:,[0,4,5,6]], on='Org')
dataFramePos = pd.merge(dataFramePos, dataFrameOrg.iloc[:,[0,4,5,6]], on='Org')
dataFrameNeg = pd.merge(dataFrameNeg, dataFrameOrg.iloc[:,[0,4,5,6]], on='Org')

# print(dataFramePos.tail(10))

dataFrame_CorStat = dataFrame.filter(items=['Org','OrgSector','OrgKununuScore','OrgTotalKununuReviews','OrgRecomPercent','RverMonthYear','RverPosition','RverLocation','RverRecom','RvScore2','Cluster'])
dataFrame_CorStat_cont = pd.crosstab(dataFrame_CorStat.OrgSector, dataFrame_CorStat.Cluster)
