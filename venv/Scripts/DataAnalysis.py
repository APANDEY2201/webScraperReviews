import numpy as np
import csv
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import scipy.stats as stats
import statsmodels.formula.api as sm
from scipy.stats import chisquare
from scipy.stats import chi2_contingency
import math
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import urllib3
from sklearn.externals import joblib
import random
import matplotlib
from sompy.sompy import SOMFactory
from sompy.visualization.plot_tools import plot_hex_map
import logging

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

print(dataFrame.head(10))

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

# ----------------------------------------------------------------------------
# PCA
# ----------------------------------------------------------------------------

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(dataFrame_KMeans)
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
# print(pca.components_)

dataFrame['PC1'] = principalDf['principal component 1']
dataFrame['PC2'] = principalDf['principal component 2']

# print(dataFrame)
dataFrame.to_csv('toTableau1.csv', encoding = 'utf-8')

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = ['Pos', 'Neg']
colors = ['r', 'g', 'b']
for target, color in zip(targets,colors):
    indicesToKeep = dataFrame['RvScore2'] == target
    ax.scatter(dataFrame.loc[indicesToKeep, 'PC1']
               , dataFrame.loc[indicesToKeep, 'PC2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()

xVals = pca.components_[0]
yVals = pca.components_[1]

print(xVals)
print(yVals)

for o in range(len(xVals)):
    x_values = [0, xVals[o]]
    y_values = [0, yVals[o]]
    plt.plot(x_values, y_values)

plt.show()

# ----------------------------------------------------------------------------
# SOM
# ----------------------------------------------------------------------------

# for i in range(2):
#     sm = SOMFactory.build(dataFrame_KMeans, mapsize=[random.choice(list(range(15, 25))), random.choice(list(range(10, 15)))], normalization = 'var', initialization='random', component_names=list(dataFrame_KMeans.columns.values), lattice="hexa")
#     sm.train(n_job=4, verbose=False, train_rough_len=30, train_finetune_len=100)
#     joblib.dump(sm, "model_{}.joblib".format(i))
#
#
# # Study the models trained and plot the errors obtained in order to select the best one
# models_pool = glob.glob("./model*")
# errors=[]
# for model_filepath in models_pool:
#     sm = joblib.load(model_filepath)
#     topographic_error = 0
#     quantization_error = 0
#     topographic_error = sm.calculate_topographic_error()
#     quantization_error = sm.calculate_quantization_error()
#     errors.append((topographic_error, quantization_error))
#     # print(errors)
# e_top, e_q = zip(*errors)
#
# # plt.scatter(e_top, e_q)
# # plt.xlabel("Topographic error")
# # plt.ylabel("Quantization error")
# # plt.show()
#
# # Manually select the model with better features. In this case, the #3 model has been selected because
# # quantization error is distributed across 34-40u and the topographic error varies much more,
# # so the model with lower topographic error has been selected. It is very important to keep the topographic
# # error as low as possible to assure a correct prototyping.
# selected_model = 1
# sm = joblib.load(models_pool[selected_model])
#
# # topographic_error = sm.calculate_topographic_error()
# # quantization_error = sm.calculate_quantization_error()
# # print ("Topographic error = %s\n Quantization error = %s" % (topographic_error, quantization_error))
#
# from sompy.visualization.mapview import View2D
# view2D  = View2D(10,10,"", text_size=7)
# # view2D.show(sm, col_sz=5, which_dim="all", denormalize=True)
# view2D.show(sm)
# plt.show()
