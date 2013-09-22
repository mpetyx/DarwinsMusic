import sys
from glob import glob

sys.path.append('lastFm')
from lastFm import lastFm

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Not enough arguments:\n\nUsage: python <script.py> <tag> <dataFolder>\n\n"
        exit()

    tag = sys.argv[1]
    dataFolder = sys.argv[2]

    key = "9d8eec456625c74e02a7e23bd1d7c68a"
    fmObj = lastFm(key, tag, dataFolder, )
    #fmObj.storeTopRecs()

    files = glob(dataFolder + "/" + tag + "/toptracks/*.json")
    for f in files:
        fmObj.storeRecInfo(f)
 
