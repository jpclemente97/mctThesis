import numpy as np
import csv
import matplotlib.pyplot as plt
import math

def calculateSerendipityPerUser(serendipityPerUser, avgQualityPerUser, avgExpectednessPerUser, 
	stdQualityPerUser, stdExpectednessPerUser, pssMethod, serendipityType):
	belowAverageQualityClustersWithSerendipity = 0
	aboveAverageQualityClustersWithSerendipity = 0
	belowAverageExpectednessClustersWithSerendipity = 0
	aboveAverageExpectednessClustersWithSerendipity = 0

	#Librosa start and end
	start = 0
	end = 6
	if (pssMethod == "Spleeter"):
		start = 6
		end = 11

	totalClusters = 0
	for i in range(0, len(serendipityPerUser)):
		for j in range(start, end):
			totalClusters += 1
			if (serendipityPerUser[i][j] > 0):
				userAvgQualityCluster = avgQualityPerUser[i][j]
				userAvgExpectednessCluster = avgExpectednessPerUser[i][j]
				userStdQualityCluster = stdQualityPerUser[i][j]
				userStdExpectednessCluster = stdExpectednessPerUser[i][j]

				userAvgQualityTotal = np.average(avgQualityPerUser[i][start:end])
				userAvgExpectednessTotal = np.average(avgExpectednessPerUser[i][start:end])
				userStdQualityTotal = np.average(stdQualityPerUser[i][start:end])
				userStdExpectednessTotal = np.average(stdExpectednessPerUser[i][start:end])

				if (userAvgQualityCluster <= userAvgQualityTotal):
					belowAverageQualityClustersWithSerendipity += 1
				else:
					aboveAverageQualityClustersWithSerendipity += 1

				if (userAvgExpectednessCluster <= userAvgExpectednessTotal):
					belowAverageExpectednessClustersWithSerendipity += 1
				else:
					aboveAverageExpectednessClustersWithSerendipity += 1

	print('Total clusters analyzed = ' + str(totalClusters))
	totalClustersWithSerendipity = belowAverageQualityClustersWithSerendipity + aboveAverageQualityClustersWithSerendipity
	print('Number of ' + pssMethod + ' clusters with ' + serendipityType + ' = ' + str(totalClustersWithSerendipity))
	print('Number of ' + pssMethod + ' clusters with ' + serendipityType + ' with above average quality = ' + str(aboveAverageQualityClustersWithSerendipity))
	print('Number of ' + pssMethod + ' clusters with ' + serendipityType + ' with below average quality = ' + str(belowAverageQualityClustersWithSerendipity))
	print('Number of ' + pssMethod + ' clusters with ' + serendipityType + ' with above average expectedness = ' + str(aboveAverageExpectednessClustersWithSerendipity))
	print('Number of ' + pssMethod + ' lusters with ' + serendipityType + ' with below average expectedness = ' + str(belowAverageExpectednessClustersWithSerendipity))

	print('Percentage of ' + pssMethod + ' clusters with ' + serendipityType + ' = ' + str(totalClustersWithSerendipity/totalClusters))
	print('Percentage of ' + pssMethod + ' clusters with ' + serendipityType + ' with above average quality = ' + str(aboveAverageQualityClustersWithSerendipity/totalClustersWithSerendipity))
	print('Percentage of ' + pssMethod + ' clusters with ' + serendipityType + ' with below average quality = ' + str(belowAverageQualityClustersWithSerendipity/totalClustersWithSerendipity))
	print('Percentage of ' + pssMethod + ' clusters with ' + serendipityType + ' with above average expectedness = ' + str(aboveAverageExpectednessClustersWithSerendipity/totalClustersWithSerendipity))
	print('Percentage of ' + pssMethod + ' lusters with ' + serendipityType + ' with below average expectedness = ' + str(belowAverageExpectednessClustersWithSerendipity/totalClustersWithSerendipity))
	print('')
	print('')

stdQualityCluster = []
stdExpectedCluster = []
avgQualityCluster = []
avgExpectedCluster = []

stdQualityPerUser = []
stdExpectednessPerUser = []
avgQualityPerUser = []
avgExpectednessPerUser = []
serendipityPerUser = []
antiserendipityPerUser = []

serendipityPerCluster = np.zeros(11)
antiserendipityPerCluster = np.zeros(11)

trueNegativePerUser = []
truePositivePerUser = []
trueNegativePerCluster = np.zeros(11)
truePositivePerCluster = np.zeros(11)

favoriteTrackPerUser = []
leastFavoriteTrackPerUser = []

for i in range(0, 11):
	stdQualityCluster.append(np.array([]))
	stdExpectedCluster.append(np.array([]))
	avgQualityCluster.append(np.array([]))
	avgExpectedCluster.append(np.array([]))
	trueNegativePerUser.append(np.array([]))
	truePositivePerUser.append(np.array([]))

with open('evaluationResponses.csv', 'r') as csvFile:
	next(csvFile)
	reader = csv.reader(csvFile)
	userIndex = 0
	for row in reader:
		stdQualityPerUser.append(np.array([]))
		stdExpectednessPerUser.append(np.array([]))
		avgQualityPerUser.append(np.array([]))
		avgExpectednessPerUser.append(np.array([]))
		serendipityPerUser.append(np.array([]))
		antiserendipityPerUser.append(np.array([]))

		favoriteNumber = [int(i) for i in row[133].split() if i.isdigit()]
		leastFavoriteNumber = [int(i) for i in row[134].split() if i.isdigit()]
		if (len(favoriteNumber) == 0):
			favoriteTrackPerUser.append(-1)
		else:
			favoriteTrackPerUser.append(favoriteNumber[0])
		if(len(leastFavoriteNumber) == 0):
			leastFavoriteTrackPerUser.append(-1)
		else:
			leastFavoriteTrackPerUser.append(leastFavoriteNumber[0])
		for i in range(0, 11):
			# extract array of quality and expected values
			clusterArray = row[(i*12) + 1:(i*12) + 13]
			qualityArray = np.array(clusterArray[0::2]).astype(int)
			expectedArray = np.array(clusterArray[1::2]).astype(int)
			stdQualityPerUser[userIndex] = np.append(stdQualityPerUser[userIndex], np.std(qualityArray, ddof=1))
			stdExpectednessPerUser[userIndex] = np.append(stdExpectednessPerUser[userIndex], np.std(expectedArray, ddof=1))
			avgQualityPerUser[userIndex] = np.append(avgQualityPerUser[userIndex], np.average(qualityArray))
			avgExpectednessPerUser[userIndex] = np.append(avgExpectednessPerUser[userIndex], np.average(expectedArray))
			stdQualityCluster[i] = np.append(stdQualityCluster[i], np.std(qualityArray, ddof=1))
			stdExpectedCluster[i] = np.append(stdExpectedCluster[i], np.std(expectedArray, ddof=1))
			avgQualityCluster[i] = np.append(avgQualityCluster[i], np.average(qualityArray))
			avgExpectedCluster[i] = np.append(avgExpectedCluster[i], np.average(expectedArray))

			# get serendipity and antiserendipity
			serendipity = np.zeros(6)
			antiserendipity = np.zeros(6)
			trueNegative = np.zeros(6)
			truePositive = np.zeros(6)
			for j in range(0, 6):
				if (qualityArray[j] > 4 and expectedArray[j] < 4):
					serendipity[j] += 1
					serendipityPerCluster[i] += 1
				elif (qualityArray[j] < 4 and expectedArray[j] > 4):
					antiserendipity[j] += 1
					antiserendipityPerCluster[i] += 1
				elif (qualityArray[j] < 4 and expectedArray[j] < 4):
					trueNegative[j] += 1
					trueNegativePerCluster[i] += 1
				elif (qualityArray[j] > 4 and expectedArray[j] > 4):
					truePositive[j] += 1
					truePositivePerCluster[i] += 1

			serendipityPerUser[userIndex] = np.append(serendipityPerUser[userIndex], sum(serendipity))
			antiserendipityPerUser[userIndex] = np.append(antiserendipityPerUser[userIndex], sum(antiserendipity))
			truePositivePerUser[i] = np.append(truePositivePerUser[i], truePositive)
			trueNegativePerUser[i] = np.append(trueNegativePerUser[i], trueNegative)

		userIndex += 1

# Serendipity vs. average cluster values
calculateSerendipityPerUser(serendipityPerUser, avgQualityPerUser, avgExpectednessPerUser, 
	stdQualityPerUser, stdExpectednessPerUser, 'Librosa', 'serendipity')
calculateSerendipityPerUser(serendipityPerUser, avgQualityPerUser, avgExpectednessPerUser, 
	stdQualityPerUser, stdExpectednessPerUser, 'Spleeter', 'serendipity')
calculateSerendipityPerUser(antiserendipityPerUser, avgQualityPerUser, avgExpectednessPerUser, 
	stdQualityPerUser, stdExpectednessPerUser, 'Librosa', 'anti-serendipity')
calculateSerendipityPerUser(antiserendipityPerUser, avgQualityPerUser, avgExpectednessPerUser, 
	stdQualityPerUser, stdExpectednessPerUser, 'Spleeter', 'anti-serendipity')

# Favorite track cluster vs. average
favoriteTracksInBelowAverageQualityCluster = 0
favoriteTracksInAboveAverageQualityCluster = 0
favoriteTracksInBelowAverageExpectednessCluster = 0
favoriteTracksInAboveAverageExpectednessCluster = 0
favoriteTracksInLibrosaClusters = 0
favoriteTracksInSpleeterClusters = 0
totalValidFavoriteTracks = len(favoriteTrackPerUser)

for i in range(0, len(favoriteTrackPerUser)):
	if (favoriteTrackPerUser[i] == -1):
		totalValidFavoriteTracks -= 1
	else:
		favoriteTrackCluster = math.floor((favoriteTrackPerUser[i] - 1) / 6)
		if(favoriteTrackCluster <= 5):
			favoriteTracksInLibrosaClusters += 1
		else:
			favoriteTracksInSpleeterClusters += 1

		averageUserQuality = np.average(avgQualityPerUser[i])
		averageUserExpectedness = np.average(avgExpectednessPerUser[i])

		averageQualityFavoriteTrackCluster = avgQualityPerUser[i][favoriteTrackCluster]
		averageExpectednessFavoriteTrackCluster = avgExpectednessPerUser[i][favoriteTrackCluster]

		if (averageUserQuality > averageQualityFavoriteTrackCluster):
			favoriteTracksInBelowAverageQualityCluster += 1
		else:
			favoriteTracksInAboveAverageQualityCluster += 1
		if (averageUserExpectedness > averageExpectednessFavoriteTrackCluster):
			favoriteTracksInBelowAverageExpectednessCluster += 1
		else:
			favoriteTracksInAboveAverageExpectednessCluster += 1

print('Total participants with valid favorite tracks = ' + str(totalValidFavoriteTracks))
print('Number of favorite tracks in Librosa clusters = ' + str(favoriteTracksInLibrosaClusters))
print('Number of favorite tracks in Spleeter clusters = ' + str(favoriteTracksInSpleeterClusters))
print('Number of participants with favorite tracks in above average quality clusters = ' + str(favoriteTracksInAboveAverageQualityCluster))
print('Number of participants with favorite tracks in below average quality clusters = ' + str(favoriteTracksInBelowAverageQualityCluster))
print('Number of participants with favorite tracks in above average expectedness clusters = ' + str(favoriteTracksInAboveAverageExpectednessCluster))
print('Number of participants with favorite tracks in below average expectedness clusters = ' + str(favoriteTracksInBelowAverageExpectednessCluster))

print('Percentage of favorite tracks in Librosa clusters = ' + str(favoriteTracksInLibrosaClusters / totalValidFavoriteTracks))
print('Percentage of favorite tracks in Spleeter clusters = ' + str(favoriteTracksInSpleeterClusters / totalValidFavoriteTracks))
print('Percentage of participants with favorite tracks in above average quality clusters = ' + str(favoriteTracksInAboveAverageQualityCluster / totalValidFavoriteTracks))
print('Percentage of participants with favorite tracks in below average quality clusters = ' + str(favoriteTracksInBelowAverageQualityCluster / totalValidFavoriteTracks))
print('Percentage of participants with favorite tracks in above average expectedness clusters = ' + str(favoriteTracksInAboveAverageExpectednessCluster / totalValidFavoriteTracks))
print('Percentage of participants with favorite tracks in below average expectedness clusters = ' + str(favoriteTracksInBelowAverageExpectednessCluster / totalValidFavoriteTracks))
print('')
print('')

# Least favorite track cluster vs. average
leastFavoriteTracksInBelowAverageQualityCluster = 0
leastFavoriteTracksInAboveAverageQualityCluster = 0
leastFavoriteTracksInBelowAverageExpectednessCluster = 0
leastFavoriteTracksInAboveAverageExpectednessCluster = 0
leastFavoriteTracksInLibrosaClusters = 0
leastFavoriteTracksInSpleeterClusters = 0
totalValidLeastFavoriteTracks = len(leastFavoriteTrackPerUser)

for i in range(0, len(leastFavoriteTrackPerUser)):
	if (leastFavoriteTrackPerUser[i] == -1):
		totalValidLeastFavoriteTracks -= 1
	else:
		leastFavoriteTrackCluster = math.floor((leastFavoriteTrackPerUser[i] - 1) / 6)
		if(leastFavoriteTrackCluster <= 5):
			leastFavoriteTracksInLibrosaClusters += 1
		else:
			leastFavoriteTracksInSpleeterClusters += 1

		averageUserQuality = np.average(avgQualityPerUser[i])
		averageUserExpectedness = np.average(avgExpectednessPerUser[i])

		averageQualityLeastFavoriteTrackCluster = avgQualityPerUser[i][leastFavoriteTrackCluster]
		averageExpectednessLeastFavoriteTrackCluster = avgExpectednessPerUser[i][leastFavoriteTrackCluster]

		if (averageUserQuality > averageQualityLeastFavoriteTrackCluster):
			leastFavoriteTracksInBelowAverageQualityCluster += 1
		else:
			leastFavoriteTracksInAboveAverageQualityCluster += 1
		if (averageUserExpectedness > averageExpectednessLeastFavoriteTrackCluster):
			leastFavoriteTracksInBelowAverageExpectednessCluster += 1
		else:
			leastFavoriteTracksInAboveAverageExpectednessCluster += 1

print('Total participants with valid least favorite tracks = ' + str(totalValidLeastFavoriteTracks))
print('Number of least favorite tracks in Librosa clusters = ' + str(leastFavoriteTracksInLibrosaClusters))
print('Number of least favorite tracks in Spleeter clusters = ' + str(leastFavoriteTracksInSpleeterClusters))
print('Number of participants with least favorite tracks in above average quality clusters = ' + str(leastFavoriteTracksInAboveAverageQualityCluster))
print('Number of participants with least favorite tracks in below average quality clusters = ' + str(leastFavoriteTracksInBelowAverageQualityCluster))
print('Number of participants with least favorite tracks in above average expectedness clusters = ' + str(leastFavoriteTracksInAboveAverageExpectednessCluster))
print('Number of participants with least favorite tracks in below average expectedness clusters = ' + str(leastFavoriteTracksInBelowAverageExpectednessCluster))

print('Percentage of least favorite tracks in Librosa clusters = ' + str(leastFavoriteTracksInLibrosaClusters / totalValidLeastFavoriteTracks))
print('Percentage of least favorite tracks in Spleeter clusters = ' + str(leastFavoriteTracksInSpleeterClusters / totalValidLeastFavoriteTracks))
print('Percentage of participants with least favorite tracks in above average quality clusters = ' + str(leastFavoriteTracksInAboveAverageQualityCluster / totalValidLeastFavoriteTracks))
print('Percentage of participants with least favorite tracks in below average quality clusters = ' + str(leastFavoriteTracksInBelowAverageQualityCluster / totalValidLeastFavoriteTracks))
print('Percentage of participants with least favorite tracks in above average expectedness clusters = ' + str(leastFavoriteTracksInAboveAverageExpectednessCluster / totalValidLeastFavoriteTracks))
print('Percentage of participants with least favorite tracks in below average expectedness clusters = ' + str(leastFavoriteTracksInBelowAverageExpectednessCluster / totalValidLeastFavoriteTracks))
print('')
print('')

# Graph avg and std
stdQualityClusterLibrosa = stdQualityCluster[0:6]
stdExpectedClusterLibrosa = stdExpectedCluster[0:6]
stdQualityClusterSpleeter = stdQualityCluster[6:11]
stdExpectedClusterSpleeter = stdExpectedCluster[6:11]

avgQualityClusterLibrosa = avgQualityCluster[0:6]
avgExpectedClusterLibrosa = avgExpectedCluster[0:6]
avgQualityClusterSpleeter = avgQualityCluster[6:11]
avgExpectedClusterSpleeter = avgExpectedCluster[6:11]

numParticipants = len(stdQualityClusterLibrosa[0])
x = np.arange(numParticipants)

qualityLibrosaFig, qualityLibrosaAxs = plt.subplots(nrows=len(stdQualityClusterLibrosa), ncols=2, figsize=(18, 20))
qualityLibrosaFig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.93, wspace=0.2, hspace=0.4)
qualityLibrosaFig.suptitle("Standard Deviation and Average of Quality Values Per Participant in Librosa PSS Clusters", fontsize=25)
for ax in qualityLibrosaAxs.flat:
    ax.set_xticks(x)
for ax in qualityLibrosaAxs[:,0]:
    ax.set(xlabel='Participant', ylabel='Standard Deviation')
for ax in qualityLibrosaAxs[:,1]:
    ax.set(xlabel='Participant', ylabel='Average')


expectedLibrosaFig, expectedLibrosaAxs = plt.subplots(nrows=len(stdExpectedClusterLibrosa), ncols=2, figsize=(18, 20))
expectedLibrosaFig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.93, wspace=0.2, hspace=0.4)
expectedLibrosaFig.suptitle("Standard Deviation and Average of Expectedness Values Per Participant in Librosa PSS Clusters", fontsize=25)
for ax in expectedLibrosaAxs.flat:
    ax.set_xticks(x)
for ax in expectedLibrosaAxs[:,0]:
    ax.set(xlabel='Participant', ylabel='Standard Deviation')
for ax in expectedLibrosaAxs[:,1]:
    ax.set(xlabel='Participant', ylabel='Average')

qualitySpleeterFig, qualitySpleeterAxs = plt.subplots(nrows=len(stdQualityClusterSpleeter), ncols=2, figsize=(18, 20))
qualitySpleeterFig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.93, wspace=0.2, hspace=0.4)
qualitySpleeterFig.suptitle("Standard Deviation and Average of Quality Values Per Participant in Spleeter PSS Clusters", fontsize=25)
for ax in qualitySpleeterAxs.flat:
    ax.set_xticks(x)
for ax in qualitySpleeterAxs[:,0]:
    ax.set(xlabel='Participant', ylabel='Standard Deviation')
for ax in qualitySpleeterAxs[:,1]:
    ax.set(xlabel='Participant', ylabel='Average')

expectedSpleeterFig, expectedSpleeterAxs = plt.subplots(nrows=len(stdExpectedClusterSpleeter), ncols=2, figsize=(18, 20))
expectedSpleeterFig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.93, wspace=0.2, hspace=0.4)
expectedSpleeterFig.suptitle("Standard Deviation and Average of Expectedness Values Per Participant in Spleeter PSS Clusters", fontsize=25)
for ax in expectedSpleeterAxs.flat:
    ax.set_xticks(x)
for ax in expectedSpleeterAxs[:,0]:
    ax.set(xlabel='Participant', ylabel='Standard Deviation')
for ax in expectedSpleeterAxs[:,1]:
    ax.set(xlabel='Participant', ylabel='Average')

averageQualityPerClusterLibrosa = np.zeros(6)
averageStdQualityPerClusterLibrosa = np.zeros(6)
averageExpectedPerClusterLibrosa = np.zeros(6)
averageStdExpectedPerClusterLibrosa = np.zeros(6)

for i in range(0, len(stdQualityClusterLibrosa)):
	stdQuality = stdQualityClusterLibrosa[i]
	qualityLibrosaAxs[i, 0].set_title("Standard Deviation Cluster " + str(i), fontsize=15)
	qualityLibrosaAxs[i, 0].axhline(np.average(stdQuality), color='red', linestyle='--', linewidth=0.5, label='std = ' + str(round(np.average(stdQuality), 2)))
	qualityLibrosaAxs[i, 0].legend(loc='upper right')
	qualityLibrosaAxs[i, 0].plot(x, stdQuality)
	averageStdQualityPerClusterLibrosa[i] = np.average(stdQuality)
	avgQuality = avgQualityClusterLibrosa[i]
	qualityLibrosaAxs[i, 1].set_title("Average Cluster " + str(i), fontsize=15)
	qualityLibrosaAxs[i, 1].axhline(np.average(avgQuality), color='red', linestyle='--', linewidth=0.5, label='avg = ' + str(round(np.average(avgQuality), 2)))
	qualityLibrosaAxs[i, 1].legend(loc='upper right')
	qualityLibrosaAxs[i, 1].plot(x, avgQuality)
	averageQualityPerClusterLibrosa[i] = np.average(avgQuality)

	stdExpected = stdExpectedClusterLibrosa[i]
	expectedLibrosaAxs[i, 0].set_title("Cluster " + str(i), fontsize=15)
	expectedLibrosaAxs[i, 0].axhline(np.average(stdExpected), color='red', linestyle='--', linewidth=0.5, label='std = ' + str(round(np.average(stdExpected), 2)))
	expectedLibrosaAxs[i, 0].legend(loc='upper right')
	expectedLibrosaAxs[i, 0].plot(x, stdExpected)
	averageStdExpectedPerClusterLibrosa[i] = np.average(stdExpected)
	avgExpected = avgExpectedClusterLibrosa[i]
	expectedLibrosaAxs[i, 1].set_title("Average Cluster " + str(i), fontsize=15)
	expectedLibrosaAxs[i, 1].axhline(np.average(avgExpected), color='red', linestyle='--', linewidth=0.5, label='avg = ' + str(round(np.average(avgExpected), 2)))
	expectedLibrosaAxs[i, 1].legend(loc='upper right')
	expectedLibrosaAxs[i, 1].plot(x, avgExpected)
	averageExpectedPerClusterLibrosa[i] = np.average(avgExpected)

print('Average standard deviation quality value for all Librosa clusters: ' + str(np.average(averageStdQualityPerClusterLibrosa)))
print('Average quality value for all Librosa clusters: ' + str(np.average(averageQualityPerClusterLibrosa)))
print('Average standard deviation expectedness value for all Librosa clusters: ' + str(np.average(averageStdExpectedPerClusterLibrosa)))
print('Average expectedness value for all Librosa clusters: ' + str(np.average(averageExpectedPerClusterLibrosa)))
print('')

averageQualityPerClusterSpleeter = np.zeros(5)
averageStdQualityPerClusterSpleeter = np.zeros(5)
averageExpectedPerClusterSpleeter = np.zeros(5)
averageStdExpectedPerClusterSpleeter = np.zeros(5)

for i in range(0, len(stdQualityClusterSpleeter)):
	stdQuality = stdQualityClusterSpleeter[i]
	qualitySpleeterAxs[i, 0].set_title("Standard Deviation Cluster " + str(i), fontsize=15)
	qualitySpleeterAxs[i, 0].axhline(np.average(stdQuality), color='red', linestyle='--', linewidth=0.5, label='std = ' + str(round(np.average(stdQuality), 2)))
	qualitySpleeterAxs[i, 0].legend(loc='upper right')
	qualitySpleeterAxs[i, 0].plot(x, stdQuality)
	averageStdQualityPerClusterSpleeter[i] = np.average(stdQuality)
	avgQuality = avgQualityClusterSpleeter[i]
	qualitySpleeterAxs[i, 1].set_title("Average Cluster " + str(i), fontsize=15)
	qualitySpleeterAxs[i, 1].axhline(np.average(avgQuality), color='red', linestyle='--', linewidth=0.5, label='avg = ' + str(round(np.average(avgQuality), 2)))
	qualitySpleeterAxs[i, 1].legend(loc='upper right')
	qualitySpleeterAxs[i, 1].plot(x, avgQuality)
	averageQualityPerClusterSpleeter[i] = np.average(avgQuality)

	stdExpected = stdExpectedClusterSpleeter[i]
	expectedSpleeterAxs[i, 0].set_title("Standard Deviation Cluster " + str(i), fontsize=15)
	expectedSpleeterAxs[i, 0].axhline(np.average(stdExpected), color='red', linestyle='--', linewidth=0.5, label='std = ' + str(round(np.average(stdExpected), 2)))
	expectedSpleeterAxs[i, 0].legend(loc='upper right')
	expectedSpleeterAxs[i, 0].plot(x, stdExpected)
	averageStdExpectedPerClusterSpleeter[i] = np.average(stdExpected)
	avgExpected = avgExpectedClusterSpleeter[i]
	expectedSpleeterAxs[i, 1].set_title("Average Cluster " + str(i), fontsize=15)
	expectedSpleeterAxs[i, 1].axhline(np.average(avgExpected), color='red', linestyle='--', linewidth=0.5, label='avg = ' + str(round(np.average(avgExpected), 2)))
	expectedSpleeterAxs[i, 1].legend(loc='upper right')
	expectedSpleeterAxs[i, 1].plot(x, avgExpected)
	averageExpectedPerClusterSpleeter[i] = np.average(avgExpected)

print('Average standard deviation quality value for all Spleeter clusters: ' + str(np.average(averageStdQualityPerClusterSpleeter)))
print('Average quality value for all Spleeter clusters: ' + str(np.average(averageQualityPerClusterSpleeter)))
print('Average standard deviation expectedness value for all Spleeter clusters: ' + str(np.average(averageStdExpectedPerClusterSpleeter)))
print('Average expectedness value for all Spleeter clusters: ' + str(np.average(averageExpectedPerClusterSpleeter)))

qualityLibrosaFig.savefig('qualityLibrosaFig.png')
expectedLibrosaFig.savefig('expectedLibrosaFig.png')
qualitySpleeterFig.savefig('qualitySpleeterFig.png')
expectedSpleeterFig.savefig('expectedSpleeterFig.png')

# Serendipity
serendipityPerClusterLibrosa = serendipityPerCluster[0:6]
antiserendipityPerClusterLibrosa = antiserendipityPerCluster[0:6]
serendipityPerClusterSpleeter = serendipityPerCluster[6:11]
antiserendipityPerClusterSpleeter = antiserendipityPerCluster[6:11]

trueNegativePerUserLibrosa = trueNegativePerUser[0:6]
truePositivePerUserLibrosa = truePositivePerUser[0:6]
trueNegativePerUserSpleeter = trueNegativePerUser[6:11]
truePositivePerUserSpleeter = truePositivePerUser[6:11]

trueNegativePerClusterLibrosa = trueNegativePerCluster[0:6]
truePositivePerClusterLibrosa = truePositivePerCluster[0:6]
trueNegativePerClusterSpleeter = trueNegativePerCluster[6:11]
truePositivePerClusterSpleeter = truePositivePerCluster[6:11]

serendipityPerClusterLibrosaFig, serendipityPerClusterLibrosaAxs = plt.subplots(figsize=(10, 3))
serendipityPerClusterLibrosaFig.subplots_adjust(bottom=0.2)
serendipityPerClusterLibrosaFig.suptitle("Total Serendipity Across All Participants Per Librosa PSS Cluster")
serendipityPerClusterLibrosaAxs.set(xlabel='Cluster', ylabel='Total Serendipity Found')
serendipityPerClusterLibrosaAxs.set_xticks(np.arange(6))
serendipityPerClusterLibrosaAxs.axhline(np.average(serendipityPerClusterLibrosa), color='red', linewidth=0.5, label='Serendipity per Cluster = ' + str(round(np.average(serendipityPerClusterLibrosa), 2)) + ', Total Serendipity = ' + str(np.sum(serendipityPerClusterLibrosa)))
serendipityPerClusterLibrosaAxs.legend(loc='upper right')
serendipityPerClusterLibrosaAxs.plot(np.arange(6), serendipityPerClusterLibrosa)
serendipityPerClusterLibrosaFig.savefig('serendipityPerClusterLibrosaFig.png')

serendipityPerClusterSpleeterFig, serendipityPerClusterSpleeterAxs = plt.subplots(figsize=(10, 3))
serendipityPerClusterSpleeterFig.subplots_adjust(bottom=0.2)
serendipityPerClusterSpleeterFig.suptitle("Total Serendipity Across All Participants Per Spleeter PSS Cluster")
serendipityPerClusterSpleeterAxs.set(xlabel='Cluster', ylabel='Total Serendipity Found')
serendipityPerClusterSpleeterAxs.set_xticks(np.arange(5))
serendipityPerClusterSpleeterAxs.axhline(np.average(serendipityPerClusterSpleeter), color='red', linewidth=0.5, label='Serendipity per Cluster = ' + str(round(np.average(serendipityPerClusterSpleeter), 2)) + ', Total Serendipity = ' + str(np.sum(serendipityPerClusterSpleeter)))
serendipityPerClusterSpleeterAxs.legend(loc='upper right')
serendipityPerClusterSpleeterAxs.plot(np.arange(5), serendipityPerClusterSpleeter)
serendipityPerClusterSpleeterFig.savefig('serendipityPerClusterSpleeterFig.png')

antiserendipityPerClusterLibrosaFig, antiserendipityPerClusterLibrosaAxs = plt.subplots(figsize=(10, 3))
antiserendipityPerClusterLibrosaFig.subplots_adjust(bottom=0.2)
antiserendipityPerClusterLibrosaFig.suptitle("Total Antiserendipity Across All Participants Per Librosa PSS Cluster")
antiserendipityPerClusterLibrosaAxs.set(xlabel='Cluster', ylabel='Total Serendipity Found')
antiserendipityPerClusterLibrosaAxs.set_xticks(np.arange(6))
antiserendipityPerClusterLibrosaAxs.axhline(np.average(antiserendipityPerClusterLibrosa), color='red', linewidth=0.5, label='Anti-serendipity per Cluster = ' + str(round(np.average(antiserendipityPerClusterLibrosa), 2)) + ', Total Anti-Serendipity = ' + str(np.sum(antiserendipityPerClusterLibrosa)))
antiserendipityPerClusterLibrosaAxs.legend(loc='upper right')
antiserendipityPerClusterLibrosaAxs.plot(np.arange(6), antiserendipityPerClusterLibrosa)
antiserendipityPerClusterLibrosaFig.savefig('antiserendipityPerClusterLibrosaFig.png')

antiserendipityPerClusterSpleeterFig, antiserendipityPerClusterSpleeterAxs = plt.subplots(figsize=(10, 3))
antiserendipityPerClusterSpleeterFig.subplots_adjust(bottom=0.2)
antiserendipityPerClusterSpleeterFig.suptitle("Total Antiserendipity Across All Participants Per Spleeter PSS Cluster")
antiserendipityPerClusterSpleeterAxs.axhline(np.average(antiserendipityPerClusterSpleeter), color='red', linewidth=0.5, label='Anti-serendipity per Cluster = ' + str(round(np.average(antiserendipityPerClusterSpleeter), 2)) + ', Total Anti-Serendipity = ' + str(np.sum(antiserendipityPerClusterSpleeter)))
antiserendipityPerClusterSpleeterAxs.set(xlabel='Cluster', ylabel='Total Serendipity Found')
antiserendipityPerClusterSpleeterAxs.set_xticks(np.arange(5))
antiserendipityPerClusterSpleeterAxs.legend(loc='upper right')
antiserendipityPerClusterSpleeterAxs.plot(np.arange(5), antiserendipityPerClusterSpleeter)
antiserendipityPerClusterSpleeterFig.savefig('antiserendipityPerClusterSpleeterFig.png')

trueNegativePerClusterLibrosaFig, trueNegativePerClusterLibrosaAxs = plt.subplots(figsize=(10, 3))
trueNegativePerClusterLibrosaFig.subplots_adjust(bottom=0.2)
trueNegativePerClusterLibrosaFig.suptitle("Total True Negative Across All Participants Per Librosa PSS Cluster")
trueNegativePerClusterLibrosaAxs.set(xlabel='Cluster', ylabel='Total trueNegative Found')
trueNegativePerClusterLibrosaAxs.set_xticks(np.arange(6))
trueNegativePerClusterLibrosaAxs.axhline(np.average(trueNegativePerClusterLibrosa), color='red', linewidth=0.5, label='True Negative per Cluster = ' + str(round(np.average(trueNegativePerClusterLibrosa), 2)) + ', Total True Negative = ' + str(np.sum(trueNegativePerClusterLibrosa)))
trueNegativePerClusterLibrosaAxs.legend(loc='upper right')
trueNegativePerClusterLibrosaAxs.plot(np.arange(6), trueNegativePerClusterLibrosa)
trueNegativePerClusterLibrosaFig.savefig('trueNegativePerClusterLibrosaFig.png')

trueNegativePerClusterSpleeterFig, trueNegativePerClusterSpleeterAxs = plt.subplots(figsize=(10, 3))
trueNegativePerClusterSpleeterFig.subplots_adjust(bottom=0.2)
trueNegativePerClusterSpleeterFig.suptitle("Total True Negative Across All Participants Per Spleeter PSS Cluster")
trueNegativePerClusterSpleeterAxs.set(xlabel='Cluster', ylabel='Total trueNegative Found')
trueNegativePerClusterSpleeterAxs.set_xticks(np.arange(5))
trueNegativePerClusterSpleeterAxs.axhline(np.average(trueNegativePerClusterSpleeter), color='red', linewidth=0.5, label='True Negative per Cluster = ' + str(round(np.average(trueNegativePerClusterSpleeter), 2)) + ', Total True Negative = ' + str(np.sum(trueNegativePerClusterSpleeter)))
trueNegativePerClusterSpleeterAxs.legend(loc='upper right')
trueNegativePerClusterSpleeterAxs.plot(np.arange(5), trueNegativePerClusterSpleeter)
trueNegativePerClusterSpleeterFig.savefig('trueNegativePerClusterSpleeterFig.png')

truePositivePerClusterLibrosaFig, truePositivePerClusterLibrosaAxs = plt.subplots(figsize=(10, 3))
truePositivePerClusterLibrosaFig.subplots_adjust(bottom=0.2)
truePositivePerClusterLibrosaFig.suptitle("Total True Positive Across All Participants Per Librosa PSS Cluster")
truePositivePerClusterLibrosaAxs.set(xlabel='Cluster', ylabel='Total Serendipity Found')
truePositivePerClusterLibrosaAxs.set_xticks(np.arange(6))
truePositivePerClusterLibrosaAxs.axhline(np.average(truePositivePerClusterLibrosa), color='red', linewidth=0.5, label='True Positive per Cluster = ' + str(round(np.average(truePositivePerClusterLibrosa), 2)) + ', Total True Positive = ' + str(np.sum(truePositivePerClusterLibrosa)))
truePositivePerClusterLibrosaAxs.legend(loc='upper right')
truePositivePerClusterLibrosaAxs.plot(np.arange(6), truePositivePerClusterLibrosa)
truePositivePerClusterLibrosaFig.savefig('truePositivePerClusterLibrosaFig.png')

truePositivePerClusterSpleeterFig, truePositivePerClusterSpleeterAxs = plt.subplots(figsize=(10, 3))
truePositivePerClusterSpleeterFig.subplots_adjust(bottom=0.2)
truePositivePerClusterSpleeterFig.suptitle("Total True Positive Across All Participants Per Spleeter PSS Cluster")
truePositivePerClusterSpleeterAxs.axhline(np.average(truePositivePerClusterSpleeter), color='red', linewidth=0.5, label='True Positive per Cluster = ' + str(round(np.average(truePositivePerClusterSpleeter), 2)) + ', Total True Positive = ' + str(np.sum(truePositivePerClusterSpleeter)))
truePositivePerClusterSpleeterAxs.set(xlabel='Cluster', ylabel='Total Serendipity Found')
truePositivePerClusterSpleeterAxs.set_xticks(np.arange(5))
truePositivePerClusterSpleeterAxs.legend(loc='upper right')
truePositivePerClusterSpleeterAxs.plot(np.arange(5), truePositivePerClusterSpleeter)
truePositivePerClusterSpleeterFig.savefig('truePositivePerClusterSpleeterFig.png')

