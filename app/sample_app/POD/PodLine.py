import subprocess
import os
from PIL import Image
import pytesseract
import time


outlineFilename = None 
framesPath = None
#User Inputs
def setUp(podcastVideoInput, frameFreq):
	global outlineFilename
	global framesPath
	#File/Folder Destination Generation based on User Inputs
	podcastName = podcastVideoInput.split('.')[0]
	framesDestFolder = podcastName + 'Frames'
	outlineFilename = podcastName + "Outline.txt"
	outputFrame = framesDestFolder + '/frame%03d.png'
	framesPath = "./" + framesDestFolder + "/"
	subprocess.call(['mkdir', framesDestFolder])
	#Call FFMPEG to save frames every frameFreq seconds in framesDestFolder
	subprocess.call(['ffmpeg', '-i', podcastVideoInput, '-vf', 'fps=1/'+frameFreq, outputFrame])
def process():
	#Sort frames in alphabetical order so they will be read chronologically
	frames = os.listdir(framesPath)
	frames.sort(key=str.lower)
  	#Open output file for reading and writing.  Create file if doesn't exist.
	Ofile = open(outlineFilename, 'w+')
	#Loop through 
	print("OCRing") #debug
	for frameName in frames:
		if frameName.endswith('.png'):
			frame = Image.open(framesPath + frameName)
			text = pytesseract.image_to_string(frame, lang = 'eng')
			title = text.partition("\n")[0]
			title.replace("\n", " ") 
			filteredTitle = "".join(i for i in title if ord(i) <128)
                	#Do not write duplicate titles
                	#firstString = Ofile.readline()
                	duplicateFlag = 0
			Ofile.seek(0)
			for st in Ofile: #how to loop thru file line by line
				if st == (filteredTitle + "\n"):
					duplicateFlag = 1
					break
			if (duplicateFlag == 0):
				Ofile.write(filteredTitle + "\n")
	Ofile.close()

def main():
	start = time.time()
	podcastVideoInput = 'VarLengthPods/test05min.mp4'
	frameFreq = '10' #save frame every _ seconds
	setUp(podcastVideoInput,frameFreq)
	process()
	end = time.time()
	print(end - start)
main()
