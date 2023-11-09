import numpy as np
import math
import csv
import pandas as pd

def getWnbd(beatTimes, onsetTimes, bins):
	noteCount = 0
	wnbdTotal = 0

	numberOfBeatsSinceLastNote = 0
	tx = 0

	for i in (range(len(beatTimes) - 1)):
		currentBeat = float(beatTimes[i])
		nextBeat = float(beatTimes[i+1])

		binSeconds = (nextBeat - currentBeat) / bins
		binBegin = currentBeat - (binSeconds/2)
		binEnd = currentBeat + (binSeconds/2)

		for j in range(bins):
			# Extract a subarray of onsets for each 16th note to remove duplicate notes
			currentOnsets = onsetTimes[(onsetTimes >= binBegin) & (onsetTimes < binEnd)]
			if np.size(currentOnsets) != 0:
				# Calculate WNBD for previous note
				if tx != 0:
					if numberOfBeatsSinceLastNote == 1:
						wnbdTotal += 2 / tx
					else:
						wnbdTotal += 1 / tx

				numberOfBeatsSinceLastNote = 0
				noteCount += 1
				tx = min(j, bins - j) / bins

			binBegin += binSeconds
			binEnd += binSeconds

		numberOfBeatsSinceLastNote += 1

	if noteCount == 0:
		return 0
	else:
		return (wnbdTotal / noteCount)


def getRhythmValues(beatTimes, onsetTimes, bins):
	beatBins = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

	for i in (range(len(beatTimes) - 1)):
		currentBeat = float(beatTimes[i])
		nextBeat = float(beatTimes[i+1])

		binSeconds = (nextBeat - currentBeat) / bins
		binBegin = currentBeat - (binSeconds/2)
		binEnd = currentBeat + (binSeconds/2)

		for j in range(bins):
			# Extract a subarray of onsets for each 16th note to remove duplicate notes
			currentOnsets = onsetTimes[(onsetTimes >= binBegin) & (onsetTimes < binEnd)]
			if np.size(currentOnsets) != 0:
				beatBins[j] += 1

			binBegin += binSeconds
			binEnd += binSeconds
	
	totalHits = np.sum(beatBins)
	if totalHits != 0:
		pulse = beatBins[0] / totalHits
		eighthNote = beatBins[6] / totalHits
		sixteenthNote = (beatBins[3] + beatBins[9]) / totalHits
		triplet = (beatBins[4] + beatBins[8]) / totalHits
		sixteenthNoteTriplet = (beatBins[2] + beatBins[10]) / totalHits
		offBeat = (beatBins[1] + beatBins[5] + beatBins[7] + beatBins[11]) / totalHits
		
		return [pulse, eighthNote, sixteenthNote, triplet, sixteenthNoteTriplet, offBeat]

	else:
		return 0 

# For Librosa HPSS
#with open("hpssTrackInfo.csv", 'r') as file:
# For Spleeter
with open("spleeterTrackInfo.csv", 'r') as file:
    bins = 12
    invalidFiles = 0

    filesArray = []
    featuresArray = []
    df = pd.DataFrame()

    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        fileName = row[0].replace('.mp3', '')
        beatTimes = row[2].split()
        onsetTimes = row[3].split()

        if beatTimes[0] == '[':
        	beatTimes.pop(0)
        if onsetTimes[0] == '[':
        	onsetTimes.pop(0)
        if beatTimes[len(beatTimes) - 1] == ']':
        	beatTimes.pop(len(beatTimes) - 1)

        if onsetTimes[len(onsetTimes) - 1] == ']':
        	onsetTimes.pop(len(onsetTimes) - 1)

        beatTimes[0] = beatTimes[0].replace('[', '')
        onsetTimes[0] = onsetTimes[0].replace('[', '')
        beatTimes[len(beatTimes) - 1] = beatTimes[len(beatTimes) - 1].replace(']', '')
        onsetTimes[len(onsetTimes) - 1] = onsetTimes[len(onsetTimes) - 1].replace(']', '')

        if(onsetTimes != [''] and beatTimes != ['']):
	        dummy = np.array(beatTimes)
	        beatTimes = dummy.astype(float)
	        dummy = np.array(onsetTimes)
	        onsetTimes = dummy.astype(float)

	        wnbd = getWnbd(beatTimes, onsetTimes, bins)
	        rhythmValues = getRhythmValues(beatTimes, onsetTimes, bins)

	        if rhythmValues == 0:
	        	invalidFiles += 1
	        else:
	        	features = [wnbd] + rhythmValues
	        	featuresArray.append(features)
	        	filesArray.append(fileName)
        else:
            invalidFiles += 1

    df['file'] = filesArray
    df['features'] = featuresArray
    df.to_csv('spleeterFeatures.csv', encoding='utf-8', index=False)
    print("invalid files = " + str(invalidFiles))


