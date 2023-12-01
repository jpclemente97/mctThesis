import numpy as np
import librosa
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import librosa.display

def getBeatBins(signal):
	onsetTimes = librosa.onset.onset_detect(y=signal, sr=sr, hop_length=220, units='time')
	tempo, beatTimes = librosa.beat.beat_track(signal, sr=sr, hop_length=220,units='time')
	beatBins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	secondsPerBeat = 60 / tempo
	bins = 12
	binDivder = secondsPerBeat / 12

	y_beats = librosa.clicks(times=onsetTimes, length=len(signal), sr=sr)
	sf.write("testOnsets4.wav", signal + y_beats, sr)

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

	totalHits = 0
	offHits = 0
	for i in range(0, len(target)):
		totalHits += target[i]
		offHits += abs(target[i] - beatBins[i])

	accuracy = 100 * (1 - (offHits / totalHits))
	beatBins.append(accuracy)
	return beatBins

import pandas as pd
import soundfile as sf

target = [20, 4, 4, 4, 8, 4, 12, 4, 8, 4, 4, 4]
df = pd.DataFrame({'target': [20, 4, 4, 4, 8, 4, 12, 4, 8, 4, 4, 4, 'accuracy (%)']})

files120 = ['data/justDrumsTest120.wav', 'data/justDrumsTest120Spleeter.mp3', 'data/songTest120.wav', 'data/songTest120Spleeter.mp3', ]
sr = 44100

for track in files120:
	audio, sr = librosa.load(track, mono=True, sr=44100)
	harmonic, percussive = librosa.effects.hpss(audio)
	df[track + " raw audio"] = getBeatBins(audio)
	df[track + " HPSS percussive seperation"] = getBeatBins(percussive)

df.to_csv('out.csv', encoding='utf-8', index=False)