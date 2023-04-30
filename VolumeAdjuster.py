import sys
import ModuleUpdate
import os
import shutil
import zipfile

commandLengths = {
    b'\xD3': 1,
    b'\xD5': 1,
    b'\xD7': 2,
    b'\x90': 2,
    b'\x91': 2,
    b'\x92': 2,
    b'\x93': 2,
    b'\x94': 2,
    b'\x95': 2,
    b'\x96': 2,
    b'\x97': 2,
    b'\x98': 2,
    b'\x99': 2,
    b'\x9A': 2,
    b'\x9B': 2,
    b'\x9C': 2,
    b'\x9D': 2,
    b'\x9E': 2,
    b'\x9F': 2,
    b'\xD6': 2,
    b'\xDD': 1,
    b'\xFD': 1,
    b'\xFB': 2,
}

def verifyOnlyOneVolume(filepath):
    volumeFound = False

    with open(filepath, "rb+") as f:
        while (byte := f.read(1)): 
            if byte == b'\xFF':
                break
            elif byte == b'\xDB':
                if volumeFound:
                    raise ValueError("Multiple volume commands. Reworking the volume will take additional work.")
                volumeFound = True
                f.read(1)
            else:
                if byte not in commandLengths:
                    raise ValueError("Unknown command: " + hex(int.from_bytes(byte, byteorder='big')))
                else:
                    if byte == b'\xFD':
                        nextbyte = int.from_bytes(f.read(1), byteorder='big')
                        if nextbyte >= 0x80:
                            f.read(1)
                        continue
                    f.read(commandLengths[byte])

def setupOotrs(filepath):
    baseFolder = os.path.dirname(os.path.realpath(__file__))

    extractedOotr = baseFolder + "\\Testsong"

    if os.path.isdir(extractedOotr):
        shutil.rmtree(extractedOotr)
        
    if os.path.isfile(extractedOotr + ".zip"):
        os.remove(extractedOotr + ".zip")
        
    if os.path.isfile(extractedOotr + ".ootrs"):
        os.remove(extractedOotr + ".ootrs")
        
    with zipfile.ZipFile(filepath,"r") as zip_ref:
        zip_ref.extractall(extractedOotr)
        
    seqFile = [extractedOotr + "\\" + file for file in os.listdir(extractedOotr) if file.endswith(".seq")]
    assert len(seqFile) == 1, "There should be exactly 1 meta file in an .ootrs"
    
    return seqFile[0]
    
def repackOotrs(originalFilePath):
    baseFolder = os.path.dirname(os.path.realpath(__file__))

    extractedOotr = baseFolder + "\\Testsong"

    shutil.make_archive(extractedOotr, 'zip', extractedOotr)
        
    os.rename(extractedOotr + ".zip", extractedOotr + ".ootrs")
    
    shutil.copyfile(extractedOotr + ".ootrs", originalFilePath)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        import easygui

        filepath = easygui.fileopenbox()
        
        if filepath is None:
            raise RuntimeError("Please select a file.")
            
    isOotrs = filepath.endswith(".ootrs")
    
    if isOotrs:
        ootrsFilePath = filepath
        filepath = setupOotrs(filepath)
        
    verifyOnlyOneVolume(filepath)
        
    with open(filepath, "rb+") as f:
        while (byte := f.read(1)): 
            if byte == b'\xDB':
                volume = f.read(1)
                volume = int.from_bytes(volume, byteorder='big')
                break
            else:
                if byte not in commandLengths:
                    raise ValueError("Unknown command: " + str(byte))
                else:
                    f.read(commandLengths[byte])
                    
        print("Current volume is: " + hex(volume))
        newVolume = input("What should the volume be changed to? (Hex)\n")

        newVolume = int(newVolume, 16)
        newVolume = newVolume.to_bytes(1, byteorder='big')
        
        f.seek(-1, 1)
        f.write(newVolume)
        
    if isOotrs:
        repackOotrs(ootrsFilePath)

