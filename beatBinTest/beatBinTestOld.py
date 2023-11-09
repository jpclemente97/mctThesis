import numpy as np
#import madmom
import librosa
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import librosa.display

def getBeatBins(signal):
	onsets = librosa.onset.onset_detect(y=signal, sr=sr, hop_length=512, units='time')
	tempo, beatTimes = librosa.beat.beat_track(signal, sr=sr, hop_length=512,units='time')
	beatBins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	secondsPerBeat = 60 / tempo
	binDivder = secondsPerBeat / 12

	y_beats = librosa.clicks(times=onsets, length=len(signal), sr=sr)
	sf.write("testOnsets4.wav", signal + y_beats, sr)

	startTime = beatTimes[0]
	if (beatTimes[0] > onsets[0]):
		startTime = onsets[0]
		
	startBin = startTime - (binDivder/2)
	endBin = startTime + (binDivder / 2)
	binIndex = 0

	while sum(beatBins) < len(onsets):
		for onset in onsets:
			if onset >= startBin and onset <= endBin:
				beatBins[binIndex % 12] += 1

		binIndex += 1
		startBin += binDivder
		endBin += binDivder

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



def getBeatBinsSuperflux(signal):
	n_fft = 1024
	hop_length = int(librosa.time_to_samples(1./200, sr=sr))
	lag = 2
	n_mels = 138
	fmin = 27.5
	fmax = 16000.
	max_size = 3
	S = librosa.feature.melspectrogram(y=signal, sr=sr, n_fft=n_fft,
                                   hop_length=hop_length,
                                   fmin=fmin,
                                   fmax=fmax,
                                   n_mels=n_mels)
	odf_sf = librosa.onset.onset_strength(S=librosa.power_to_db(S, ref=np.max),
                                      sr=sr,
                                      hop_length=hop_length,
                                      lag=lag, max_size=max_size)

	tempo, beatTimes = librosa.beat.beat_track(signal, onset_envelope=odf_sf, sr=sr, hop_length=hop_length, units='time')

	secondsPerBeat = 60 / tempo
	binDivder = secondsPerBeat / 12

	onsets = librosa.onset.onset_detect(onset_envelope=odf_sf,
                                      sr=sr,
                                      hop_length=hop_length,
                                      units='time')

	print(beatTimes)
	print(onsets)
	y_beats = librosa.clicks(times=onsets, length=len(signal), sr=sr)
	sf.write("testOnsets.wav", signal + y_beats, sr)

	beatBins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	

	#print('beat time start: ' + str(beatTimes[0]))
	#print('onset time start: ' + str(onsets[0]))
	print(hop_length)
	print('tempo: ' + str(tempo))
	print(beatTimes)
	startTime = beatTimes[0]
	if (beatTimes[0] > onsets[0]):
		startTime = onsets[0]
		
	startBin = startTime - (binDivder/4)
	endBin = startTime + (3 * binDivder / 4)
	binIndex = 0

	while sum(beatBins) < len(onsets):
		for onset in onsets:
			if onset >= startBin and onset <= endBin:
				beatBins[binIndex % 12] += 1

		binIndex += 1
		startBin += binDivder
		endBin += binDivder

	totalHits = 0
	offHits = 0
	for i in range(0, len(target)):
		totalHits += target[i]
		offHits += abs(target[i] - beatBins[i])

	accuracy = 100 * (1 - (offHits / totalHits))
	beatBins.append(accuracy)
	return beatBins

target = [20, 4, 4, 4, 8, 4, 12, 4, 8, 4, 4, 4]
df = pd.DataFrame({'target': [20, 4, 4, 4, 8, 4, 12, 4, 8, 4, 4, 4, 'accuracy (%)']})

#files120 = ['data/songTest120NoSyncopation.wav', 'data/justDrumsTestNoSyncopation120.wav', 'data/songTest120NoSyncopationSpleeter.mp3', 'data/justDrumsTestNoSyncopation120Spleeter.mp3']
files120 = ['data/justDrumsTest120.wav', 'data/justDrumsTest120Spleeter.mp3', 'data/songTest120.wav', 'data/songTest120Spleeter.mp3', ]
files180 = ['data/drums150062.mp3']

sr = 44100

for track in files120:
	audio, sr = librosa.load(track, mono=True, sr=44100)
	harmonic, percussive = librosa.effects.hpss(audio)
	df[track + " raw audio"] = getBeatBins(audio)
	df[track + " HPSS percussive seperation"] = getBeatBins(percussive)
	#df[track + " raw audio + superflux"] = getBeatBinsSuperflux(audio)
	#df[track + " HPSS percussive seperation + superflux"] = getBeatBinsSuperflux(percussive)

df.to_csv('out.csv', encoding='utf-8', index=False)