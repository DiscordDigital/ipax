import sys
import os
import re
import shutil
import json
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

def extractAppIcon(IPAfile, IconNames):
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
    os.rename(max_file,'/home/work/AppIcon.png')

def uncrushPng(png_path):
    os.system('python2 /appdata/ipin.py ' + png_path)


ipaFilename = sys.argv[1]
ipaLocation = "/home/work/files/"

ipaFullPath = ipaLocation + ipaFilename

if sys.argv[1] == "none":
    print("Run this image with following arguments:\n")
    print('-e filename="sample.ipa" --rm -v /tmp/ipas/:/home/work/files\n')
    print("Replace sample.ipa with the target filename.")
    print("Replace /tmp/ipas/ with the location of the IPA file.")
    exit()

if not os.path.isfile(ipaFullPath):
    print('{"Error": "FileNotFound"}')
    exit()

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
    print('{"Error": "NotAnIPAFile"}')
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
    extractAppIcon(ipaFullPath, IconNames)
    uncrushPng('/home/work/AppIcon.png')

    genericName = os.path.splitext(ipaFilename)[0] + '.png'
    shutil.move('/home/work/AppIcon.png','/home/work/files/' + genericName)

    result = dict()
    result["AppName"] = appName
    result["AppVersion"] = appVersion
    result["AppBundleIdentifier"] = appBundleIdentifier
    result["IconName"] = genericName

    json_result = json.dumps(result)
    print(json_result)
