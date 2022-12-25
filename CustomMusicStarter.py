import sys
import os
import shutil
from subprocess import Popen

if len(sys.argv) < 2:
    raise ValueError("You need to open the .bat script with a file")

seqFile = sys.argv[1]

if not os.path.isfile(seqFile):
    raise ValueError(".seq file doesn't exist")
    
metaFile = seqFile[:-4] + ".meta"
    
if not os.path.isfile(metaFile):
    raise ValueError(".meta file doesn't exist")
    
baseFolder = os.path.dirname(os.path.realpath(__file__))

ootrFolder = baseFolder + "\\OoT-Randomizer"

if not os.path.isdir(ootrFolder):
    raise ValueError(ootrFolder + " doesn't exist. Please download a local python installation of the randomizer.")
    
ootrRandomizer = ootrFolder + "\\OoTRandomizer.py"

zootDec = ootrFolder + "\\ZOOTDEC.z64"

if not os.path.isfile(ootrRandomizer):
    raise ValueError(ootrRandomizer + " not found.")
    
if not os.path.isfile(zootDec):
    raise ValueError("ZOOTDEC.z64 not found in the randomizer folder. If you don't have a ZOOTDEC.z64, running the randomizer and generating a seed once will create one.")
    
musicFolder = ootrFolder + "\\data\\Music"

if not os.path.isdir(musicFolder):
    raise ValueError(musicFolder + " not found.")
    
subdirs = os.listdir(baseFolder)

bizhawkFolder = ""
for subdir in subdirs:
    if "BizHawk" in subdir:
        bizhawkFolder = baseFolder + "\\" + subdir
        
if bizhawkFolder == "" or not os.path.isdir(bizhawkFolder):
    raise ValueError(bizhawkFolder + " not found.")
    
outputFolder = ootrFolder + "\\Output"
if os.path.isdir(outputFolder):
    shutil.rmtree(outputFolder)
    
with open(baseFolder + "\\settings.sav") as f:
    string = f.read()
    string = string.replace("[COSMETIC_FILE]", baseFolder.replace("\\", "\\\\") + "\\\\Cosmetic.json")
    
    with open(ootrFolder + "\\settings.sav", "w") as f2:
        f2.write(string)
        
with open(metaFile) as f:
    string = f.readlines()
    string[0] = "Testsong\n"
    
    if len(string) >= 3:
        string[2] = "bgm\n"
    else:
        string[1] = string[1].strip() + "\n"
        string.append("bgm\n")
    
    with open(musicFolder + "\\Testsong.meta", "w") as f2:
        f2.write("".join(string))
      
shutil.copyfile(seqFile, musicFolder + "\\Testsong.seq")     

command = 'python "' + os.path.abspath(ootrRandomizer) + '"'

Popen(command, shell=True).wait()

outputFiles = os.listdir(outputFolder)
n64file = ""
for file in outputFiles:
    if ".z64" in file:
        n64file = outputFolder + "\\" + file
        
if not os.path.isfile(n64file):
    raise ValueError("Couldn't find output rom.")

command = '"' + os.path.abspath(bizhawkFolder) + '\\EmuHawk.exe" "' + os.path.abspath(n64file) + '"'  

Popen(command, shell=True).wait()