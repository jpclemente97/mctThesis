import numpy as np
#import madmom
import librosa
#import matplotlib.pyplot as plt
#from sklearn.cluster import KMeans
#import librosa.display
import pandas as pd
import os

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


# o_env = librosa.onset.onset_strength(y=percussive, sr=sr)
# times = librosa.times_like(o_env, sr=sr)
# onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)
# D = np.abs(librosa.stft(percussive))
# fig, ax = plt.subplots(nrows=2, sharex=True)
# librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
#                          x_axis='time', y_axis='log', ax=ax[0])
# ax[0].set(title='Power spectrogram')
# ax[0].label_outer()
# ax[1].plot(times, o_env, label='Onset strength')
# ax[1].vlines(times[onset_frames], 0, o_env.max(), color='r', alpha=0.9,
#            linestyle='--', label='Onsets')
# ax[1].legend()
# plt.show()
