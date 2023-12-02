import wave
import subprocess
import os
import sys

genreList = os.listdir('fma_small')

for genre in genreList:
	if genre != '.DS_Store' and genre != 'checksums' and genre != 'README.txt':
		path = "instrumentals/" + genre
		if os.path.exists(path) == False:
			songList = os.listdir('fma_small/' + genre)
			for song in songList:
				if song != '.DS_Store':
					print(song)
					output = "instrumentals/" + genre
					print(output)
					inputFile = "fma_small/" + genre + "/" + song
					print(inputFile)
					command = "python -m spleeter separate -c mp3 -p spleeter:4stems -o " + output + " " + inputFile 
					print(command)
					os.system(command)
				outputList = os.listdir(output)
				for newFolder in outputList:
					if newFolder != '.DS_Store':
						newFolderList = os.listdir(output + "/" + newFolder)
						for newFile in newFolderList:
							if newFile != 'drums.mp3' and newFile != '.DS_Store':
								os.remove(output + "/" + newFolder + "/" + newFile)
