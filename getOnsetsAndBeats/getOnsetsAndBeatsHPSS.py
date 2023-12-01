import numpy as np
import librosa
import pandas as pd
import os
import soundfile as sf

def getBeatInfo(fileName, signal):
	onsets = librosa.onset.onset_detect(y=signal, sr=sr, hop_length=220, units='time')
	tempo, beatTimes = librosa.beat.beat_track(signal, sr=sr, hop_length=220,units='time')
	filesArray.append(fileName)
	tempoArray.append(tempo)
	beatTimesArray.append(beatTimes)
	onsetsArray.append(onsets)


df = pd.DataFrame()
sr = 44100
genreList = os.listdir('fma_small')
filesArray = []
tempoArray = []
beatTimesArray = []
onsetsArray = []

for genre in genreList:
	if genre != '.DS_Store' and genre != 'checksums' and genre != 'README.txt':
		tracks = os.listdir('fma_small/' + genre)
		for track in tracks:
			if track != '.DS_Store' and track != 'checksums' and track != 'README.txt':
				audioFile = 'fma_small/' + genre + '/' + track
				audio, sr = librosa.load(audioFile, mono=True, sr=44100)
				harmonic, percussive = librosa.effects.hpss(audio)
				print(track)
				getBeatInfo(track, audio)

df['file'] = filesArray
df['tempo'] = tempoArray
df['beatTimes'] = beatTimesArray
df['onsets'] = onsetsArray
df.to_csv('hpssTrackInfo.csv', encoding='utf-8', index=False)
