import sys
import os
import re
import shutil
import json
import hashlib
import plistlib

from zipfile import ZipFile
from time import time


def convertToExpression(expression):
    expressionLower = expression.lower()
    if expressionLower == "true":
        return True
    if expressionLower == "false":
        return False
    if expressionLower == "none":
        return None
    return expression


def mergeDicts(x, y):
    newDict = x.copy()
    newDict.update(y)
    return newDict


def grabAppleXMLValue(key, xml):
    lines = xml.splitlines()
    thisLine = False
    for line in lines:
        if thisLine:
            result = line.replace(
                '  ',
                '').replace(
                '\t',
                '').replace(
                '<string>',
                '').replace(
                '</string>',
                '')
            return result
        if key in line:
            thisLine = True


def grabAppleIconNames(xml):
    lines = xml.splitlines()
    startRead = False
    multiMode = True
    readOnce = False
    iconNames = []
    for line in lines:
        if startRead:
            result = line.replace(
                '  ',
                '').replace(
                '\t',
                '').replace(
                '<string>',
                '').replace(
                '</string>',
                '')
            if (not result == "<array>") and (not result == "</array>"):
                iconNames.append(result)
        if readOnce:
            startRead = False
        if ("<key>CFBundleIconFile</key>" in line):
            startRead = True
            multiMode = False
        if ("<key>CFBundleIconFiles</key>" in line):
            startRead = True
            multiMode = True
        if multiMode:
            if "</array>" in line:
                startRead = False
        else:
            readOnce = True
    iconNames = list(dict.fromkeys(iconNames))
    return iconNames


def extractAppIcon(IPAfile, iconNames, SaveAs):
    try:
        shutil.rmtree('/appdata/Icons')
    except BaseException:
        pass
    try:
        os.mkdir('/appdata/Icons')
    except BaseException:
        pass
    with ZipFile(IPAfile, 'r') as zipObj:
        listOfFileNames = zipObj.namelist()
        for fileName in listOfFileNames:
            for iconName in iconNames:
                if iconName in fileName:
                    if ".png" in fileName:
                        zipObj.extract(fileName, '/appdata/tmp_icons')
                        basename = os.path.basename(fileName)
                        os.rename(
                            '/appdata/tmp_icons/' + fileName,
                            '/appdata/Icons/' + basename)
    size = 0
    max_size = 0
    for folder, subfolders, files in os.walk('/appdata/Icons'):
        for file in files:
            size = os.stat(os.path.join(folder, file)).st_size
            if size > max_size:
                max_size = size
                max_file = os.path.join(folder, file)
    shutil.move(max_file, '/home/work/files/' + SaveAs)


def uncrushPng(png_path):
    os.system('python2 /appdata/ipin.py ' + png_path)


def processIPA(ipaFullPath, defaultkey, appicons, appicondir):
    baseFileName = os.path.basename(ipaFullPath)
    MatchPattern = "Payload\\/.+?..app/Info.plist"
    with ZipFile(ipaFullPath, 'r') as zipObj:
        listOfFileNames = zipObj.namelist()
        for fileName in listOfFileNames:
            m = re.match(MatchPattern, fileName)
            if m:
                zipObj.filename = os.path.basename(zipObj.filename)
                zipObj.extract(fileName, '/appdata/tmp_infoplist')
                os.rename('/appdata/' + 'tmp_infoplist/' + fileName,
                          '/home/work/Info.plist')
    if not os.path.isfile('/home/work/Info.plist'):
        return 'NotAnIPAFile'
    else:
        filename = '/home/work/Info.plist'
        infile = open(filename, 'rb')
        firstLine = infile.readline()
        if (firstLine.startswith(b"bplist")):
            with open(filename, 'rb') as fp:
                plistFormatted = plistlib.load(fp)
                with open(filename, 'wb') as fp:
                    plistlib.dump(plistFormatted, fp)
        xml = open('/home/work/Info.plist', 'r').read()

        appName = grabAppleXMLValue('CFBundleName', xml)
        appVersion = grabAppleXMLValue('CFBundleShortVersionString', xml)
        appBundleIdentifier = grabAppleXMLValue('CFBundleIdentifier', xml)
        appSize = os.path.getsize(ipaFullPath)

        iconNames = grabAppleIconNames(xml)

        if (appicons):
            if (len(iconNames) > 0):
                md5_hash = hashlib.md5()
                a_file = open(ipaFullPath, "rb")
                content = a_file.read()
                md5_hash.update(content)
                hash = md5_hash.hexdigest()

                newImageFileName = hash + ".png"

                extractAppIcon(ipaFullPath, iconNames, appicondir + "/" + newImageFileName)
                uncrushPng('/home/work/files/' + appicondir + "/" + newImageFileName)
            else:
                print("Warning: " + baseFileName + " has no icon or the parser failed.")
                newImageFileName = False
        else:
            newImageFileName = False

        result = dict()
        if (defaultkey == "filename"):
            result[baseFileName] = dict()
            result[baseFileName]["AppName"] = appName
            result[baseFileName]["AppVersion"] = appVersion
            result[baseFileName]["AppBundleIdentifier"] = appBundleIdentifier
            result[baseFileName]["AppSize"] = appSize
            result[baseFileName]["IconName"] = newImageFileName
            result[baseFileName]["Timestamp"] = int(time())
        elif (defaultkey == "bundleId"):
            result[appBundleIdentifier] = dict()
            result[appBundleIdentifier]["AppName"] = appName
            result[appBundleIdentifier]["AppVersion"] = appVersion
            result[appBundleIdentifier]["AppSize"] = appSize
            result[appBundleIdentifier]["IconName"] = newImageFileName
            result[appBundleIdentifier]["FileName"] = baseFileName
            result[appBundleIdentifier]["Timestamp"] = int(time())
        else:
            result["AppName"] = appName
            result["AppVersion"] = appVersion
            result["AppBundleIdentifier"] = appBundleIdentifier
            result["AppSize"] = appSize
            result["IconName"] = newImageFileName
            result["FileName"] = baseFileName
            result["Timestamp"] = int(time())
        return result


ipaLocation = "/home/work/files/"
outfiledir = convertToExpression(sys.argv[9])
ipaFilename = convertToExpression(sys.argv[1])

if convertToExpression(sys.argv[2]) is not None:
    outfile = ipaLocation + outfiledir + "/" + sys.argv[2]
else:
    outfile = convertToExpression(sys.argv[2])
multiple = convertToExpression(sys.argv[3])

if ipaFilename is not None:
    ipaFullPath = ipaLocation + ipaFilename

pretty = convertToExpression(sys.argv[4])
sortkey = convertToExpression(sys.argv[5])
defaultkey = convertToExpression(sys.argv[6])
appicons = convertToExpression(sys.argv[7])
appicondir = convertToExpression(sys.argv[8])

if outfiledir != "/":
    os.makedirs(ipaLocation + outfiledir, exist_ok=True)

if appicondir != "/":
    os.makedirs(ipaLocation + appicondir, exist_ok=True)

if multiple:
    allFiles = os.listdir(ipaLocation)
    if (defaultkey is None):
        json_contents = []
    else:
        json_contents = {}
    for f in allFiles:
        if f.lower().endswith(".ipa"):
            ipaFullPath = ipaLocation + f
            returnData = processIPA(
                ipaFullPath, defaultkey, appicons, appicondir)
            if (returnData == "NotAnIPAFile"):
                print("Warning: file " + f + " is not an ipa file.")
                continue
            if (defaultkey is not None):
                json_contents = mergeDicts(json_contents, returnData)
            else:
                json_contents.append(returnData)
    if outfile is None:
        if (sortkey) and (pretty):
            print(json.dumps(json_contents, indent=4, sort_keys=True))
        elif (sortkey):
            print(json.dumps(json_contents, sort_keys=True))
        elif (pretty):
            print(json.dumps(json_contents, indent=4))
        else:
            print(json.dumps(json_contents))
    else:
        try:
            outF = open(outfile, "w")
            if (sortkey) and (pretty):
                outF.write(json.dumps(json_contents, indent=4, sort_keys=True))
            else:
                if (sortkey):
                    outF.write(json.dumps(json_contents, sort_keys=True))
                elif (pretty):
                    outF.write(json.dumps(json_contents, indent=4))
                else:
                    outF.write(json.dumps(json_contents))
        except OSError as err:
            print("Couldn't save to outfile: {0}".format(err))
            pass
else:
    if convertToExpression(sys.argv[1]) is None:
        print("Run this image with following arguments:\n")
        print('-e filename="sample.ipa" --rm -v /tmp/ipas/:/home/work/files\n')
        print("Replace sample.ipa with the target filename.")
        print("Replace /tmp/ipas/ with the location of the IPA file.\n")
        print("Alternatively you can process all ipa files like this:")
        print('-e multiple=True --rm -v /tmp/ipas/:/home/work/files\n\n')
        print("You can output the JSON contents to a text file by using:\n")
        print('-e outfile="result.json"\n\n')
        print('You can make the output pretty by using -e pretty=True\n')
        print('To set the default key you can either specify -e defaultkey="filename" or -e defaultkey="bundleId".\n')
        print('To make the keynames sorted you can specify -e sortkey=True.\n\n')
        print('If you want to save in a subfolder or subfolders within the workdir you can specify following:')
        print('-e appicondir="appicons"')
        print('-e outfiledir="json"')
        print("appicondir specifies the subfolder for appicons.\noutfiledir specifies the subfolder for the json file.\n\n")
        print('You can disable image generation by using: -e appicons=False')
        exit()
    else:
        if not os.path.isfile(ipaFullPath):
            print("Debug: " + ipaFullPath)
            print('{"Error": "FileNotFound"}')
            exit()

        if outfile is None:
            if (pretty):
                print(
                    json.dumps(
                        processIPA(
                            ipaFullPath,
                            defaultkey,
                            appicons,
                            appicondir),
                        indent=4))
            else:
                print(
                    json.dumps(
                        processIPA(
                            ipaFullPath,
                            defaultkey,
                            appicons,
                            appicondir)))
        else:
            try:
                try:
                    os.remove(outfile)
                except BaseException:
                    pass
                outF = open(outfile, "a")
                if (pretty):
                    outF.write(
                        json.dumps(
                            processIPA(
                                ipaFullPath,
                                defaultkey,
                                appicons,
                                appicondir),
                            indent=4,
                            sort_keys=True))
                elif (pretty):
                    outF.write(
                        json.dumps(
                            processIPA(
                                ipaFullPath,
                                defaultkey,
                                appicons,
                                appicondir),
                            indent=4))
                else:
                    outF.write(json.dumps(processIPA(
                        ipaFullPath, defaultkey, appicons, appicondir)))
            except OSError as err:
                print("Couldn't save to outfile: {0}".format(err))
                pass
