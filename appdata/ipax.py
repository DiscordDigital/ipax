import sys
import os
import re
import shutil
import json
import hashlib
from zipfile import ZipFile

def grabAppleXMLValue(key, xml):
    lines = xml.splitlines()
    thisLine = False
    for line in lines:
        if thisLine:
            result = line.replace('  ','').replace('\t','').replace('<string>','').replace('</string>','')
            return result
        if key in line:
            thisLine = True

def grabAppleIconNames(xml):
    lines = xml.splitlines()
    startRead = False
    IconNames = []
    for line in lines:
        if startRead:
            result = line.replace('  ','').replace('\t','').replace('<string>','').replace('</string>','')
            if (not result == "<array>") and (not result == "</array>"):
                IconNames.append(result)
        if "<key>CFBundleIconFiles</key>" in line:
            startRead = True
        if "</array>" in line:
            startRead = False
    IconNames = list(dict.fromkeys(IconNames))
    return IconNames

def extractAppIcon(IPAfile, IconNames, SaveAs):
    try:
        os.rmdir('/appdata/Icons')
    except:
        pass
    try:
        os.mkdir('/appdata/Icons')
    except:
        pass
    with ZipFile(IPAfile, 'r') as zipObj:
        listOfFileNames = zipObj.namelist()
        for fileName in listOfFileNames:
            for IconName in IconNames:
                if IconName in fileName:
                    if ".png" in fileName:
                        zipObj.extract(fileName, '/appdata/tmp_icons')
                        basename = os.path.basename(fileName)
                        os.rename('/appdata/tmp_icons/'+fileName, '/appdata/Icons/'+basename)
    size = 0
    max_size = 0
    for folder, subfolders, files in os.walk('/appdata/Icons'):
        for file in files:
            size = os.stat(os.path.join(folder, file)).st_size
            if size > max_size:
                max_size = size
                max_file = os.path.join(folder, file)
    shutil.move(max_file,'/home/work/files/' + SaveAs)

def uncrushPng(png_path):
    os.system('python2 /appdata/ipin.py ' + png_path)

def processIPA(ipaFullPath):
    baseFileName = os.path.basename(ipaFullPath)
    MatchPattern = "Payload\/.+?..app/Info.plist"
    with ZipFile(ipaFullPath, 'r') as zipObj:
        listOfFileNames = zipObj.namelist()
        for fileName in listOfFileNames:
            m = re.match(MatchPattern, fileName)
            if m:
                zipObj.filename = os.path.basename(zipObj.filename)
                zipObj.extract(fileName, '/appdata/tmp_infoplist')
                os.rename('/appdata/' + 'tmp_infoplist/' + fileName, '/home/work/Info.plist')
    if not os.path.isfile('/home/work/Info.plist'):
        return 'NotAnIPAFile'
    else:
        infile = open('/home/work/Info.plist', 'rb')
        firstLine = infile.readline()
        if (firstLine.startswith(b"bplist")):
            os.system("plistutil -i " + "/home/work/Info.plist -o /home/work/Info_.plist")
            os.remove("/home/work/Info.plist")
            os.rename("/home/work/Info_.plist", "/home/work/Info.plist")
        xml = open('/home/work/Info.plist','r').read()

        appName = grabAppleXMLValue('CFBundleName', xml)
        appVersion = grabAppleXMLValue('CFBundleShortVersionString', xml)
        appBundleIdentifier = grabAppleXMLValue('CFBundleIdentifier', xml)

        IconNames = grabAppleIconNames(xml)

        md5_hash = hashlib.md5()
        a_file = open(ipaFullPath, "rb")
        content = a_file.read()
        md5_hash.update(content)
        hash = md5_hash.hexdigest()

        newImageFileName = hash + ".png"

        extractAppIcon(ipaFullPath, IconNames, newImageFileName)
        uncrushPng('/home/work/files/' + newImageFileName)

        result = dict()
        result["AppName"] = appName
        result["AppVersion"] = appVersion
        result["AppBundleIdentifier"] = appBundleIdentifier
        result["IconName"] = newImageFileName
        result["FileName"] = baseFileName
        return result

ipaLocation = "/home/work/files/"

ipaFilename = sys.argv[1]
if sys.argv[2] != "none":
    outfile = ipaLocation + sys.argv[2]
else:
    outfile = sys.argv[2]
multiple = sys.argv[3]

ipaFullPath = ipaLocation + ipaFilename

if multiple == "true":
        allFiles = os.listdir(ipaLocation)
        json_contents = []
        for f in allFiles:
            if f.lower().endswith(".ipa"):
                ipaFullPath = ipaLocation + f
                returnData = processIPA(ipaFullPath)
                if (returnData == "NotAnIPAFile"):
                    print("Warning: file " + f + " is not an ipa file.")
                    continue
                json_contents.append(returnData)
        if outfile == "none":
            print(json.dumps(json_contents))
        else:
            try:
                try:
                    os.remove(outfile)
                except:
                    pass
                outF = open(outfile, "a")
                outF.write(json.dumps(json_contents))
            except OSError as err:
                print("Couldn't save to outfile: {0}".format(err))
                pass
else:
    if sys.argv[1] == "none":
        print("Run this image with following arguments:\n")
        print('-e filename="sample.ipa" --rm -v /tmp/ipas/:/home/work/files\n')
        print("Replace sample.ipa with the target filename.")
        print("Replace /tmp/ipas/ with the location of the IPA file.\n")
        print("Alternatively you can process all ipa files like this:")
        print('-e multiple="true" --rm -v /tmp/ipas/:/home/work/files\n\n')
        print("You can output the JSON contents to a text file by using:\n")
        print('-e outfile="result.json"')
        exit()
    else:
        if not os.path.isfile(ipaFullPath):
            print('{"Error": "FileNotFound"}')
            exit()

        if outfile == "none":
            print(json.dumps(processIPA(ipaFullPath)))
        else:
            try:
                try:
                    os.remove(outfile)
                except:
                    pass
                outF = open(outfile, "a")
                outF.write(json.dumps(processIPA(ipaFullPath)))
            except OSError as err:
                print("Couldn't save to outfile: {0}".format(err))
                pass
