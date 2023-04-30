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

removeZbankAndBankMetaLater = False

if not os.path.isfile(zbankFile):
    removeZbankAndBankMetaLater = True

    #  create from vanilla banks
    
    vanilla_banks_dir = ""

    baseFolder = os.path.dirname(os.path.realpath(__file__))
    exclude = ["OoT-Randomizer"]
    for root, dirs, files in os.walk(baseFolder, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        for filename in files:    
            if filename == "0a.bankmeta":
                vanilla_banks_dir = root
    
    assert vanilla_banks_dir, "If you don't provide a .bankmeta and .zbank file, you'll need the vanilla banks in a folder called vanilla_banks in the Custom Music Starter directory."
    
    bank = ""
    with open(metaFile, "r") as file:
        bank = hex(int(file.readlines()[1].strip(), 16))[2:]
                
    if len(bank) == 1:
        bank = "0" + bank
            
        zbank_file = os.path.join(vanilla_banks_dir, bank + ".zbank")
        bankmeta_file = os.path.join(vanilla_banks_dir, bank + ".bankmeta")
        
        shutil.copy(zbank_file, zbankFile)
        shutil.copy(bankmeta_file, bankMetaFile)
    
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
        
for file in [metaFile, zbankFile, bankMetaFile, seqFile] + zsounds:
    assert os.path.isfile(file), f"{file} could not be found, but is referenced in {metaFile}."
    shutil.copy(file, os.path.join(sequenceName, os.path.split(file)[1]))
    
    
shutil.make_archive(sequenceName, 'zip', sequenceName)
        
os.rename(sequenceName + ".zip", sequenceName + ".ootrs")
    
    
    
if os.path.isdir(sequenceName):
    shutil.rmtree(sequenceName)
    
if os.path.isfile(sequenceName + ".zip"):
    os.remove(sequenceName + ".zip")
        
if removeZbankAndBankMetaLater:
    os.remove(zbankFile)
    os.remove(bankMetaFile)