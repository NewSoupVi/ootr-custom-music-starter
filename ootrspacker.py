import os
import sys
import shutil

if len(sys.argv) < 2:
    raise ValueError("You need to open the .bat script with a file")

seqFile = sys.argv[1]
assert seqFile.endswith(".seq"), "This only works with .seq files."

if not os.path.isfile(seqFile):
    raise ValueError(".seq file doesn't exist")
    
metaFile = seqFile[:-4] + ".meta"
zbankFile = seqFile[:-4] + ".zbank"
bankMetaFile = seqFile[:-4] + ".bankmeta"
sequenceName = seqFile[:-4]
sequenceFolder = os.path.dirname(seqFile)

assert os.path.isfile(metaFile), "Needs an associated .meta file."

assert not (os.path.isfile(zbankFile) ^ os.path.isfile(bankMetaFile)), "If there is a .zbank file, there needs to be a .bankMeta file."
    
zsounds = []
with open(metaFile, "r") as f:
    lines = [line.strip() for line in f.readlines()]
    
    if len(lines) > 4:
        lines = lines[4:]
    else:
        lines = []
        
    for line in lines:
        if not "zsound:" in line.lower():
            continue
        
        zsounds.append(os.path.join(sequenceFolder, line.split(":")[1]))
        
if os.path.isdir(sequenceName):
    shutil.rmtree(sequenceName)
    
if os.path.isfile(sequenceName + ".zip"):
        os.remove(sequenceName + ".zip")
        
if os.path.isfile(sequenceName + ".ootrs"):
        os.remove(sequenceName + ".ootrs")

os.mkdir(sequenceName)

files = [metaFile, seqFile]
if os.path.isfile(zbankFile):
    files = [metaFile, zbankFile, bankMetaFile, seqFile] + zsounds
        
for file in files:
    assert os.path.isfile(file), f"{file} could not be found, but is referenced in {metaFile}."
    shutil.copy(file, os.path.join(sequenceName, os.path.split(file)[1]))
    
    
shutil.make_archive(sequenceName, 'zip', sequenceName)
        
os.rename(sequenceName + ".zip", sequenceName + ".ootrs")
    
    
    
if os.path.isdir(sequenceName):
    shutil.rmtree(sequenceName)
    
if os.path.isfile(sequenceName + ".zip"):
    os.remove(sequenceName + ".zip")