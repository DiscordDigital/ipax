<div align="center">
  
# **iPAX** - _IPA Metadata Extractor_
A **docker** image to extract common metadata from "iPA" files and also to extract and normalize app icons. If **iPAX** helped you, please don't forget to <font color=#FF0000 size=5>🌟</font> [Me](https://github.com/DiscordDigital).
</div>

## ipax Features:
- [x] App Name
- [x] App Version
- [x] App Bundle Identifier
- [x] App Icon
- [x] App Size
- [x] File Name
- [x] Time Stamp

## Building the docker image

#### clone the repository:

```console
git clone https://github.com/DiscordDigital/ipax; cd ipax
```
#### Build iPAX using following command:
```console
docker build -t ipax:latest .
```
Once it's built you can already use it.

## Usage: 

```bash
Usage: docker run --rm -e [-options1] -e [-options2] -e [-options3] -v /tmp/ipas/:/home/work/files ipax:latest

options:
-e filename="sample.ipa"           Single iPA file.
-e multiple=True                   Multiple iPA files.
-e outfile="result.json"           Extract iPA file info into .JSON file.
-e pretty="true"                   Generate debug output files. (.zsign_debug folder)
-e defaultkey="bundleId"           JSON output search by key bundleId.
-e defaultkey="filename"           JSON output search by key FileName.
-e sortkey=True                    JSON output sorted alphabetically.
-e outfiledir="Folder"             Auto-generate subdirs for JSON file. 
-e appicondir="icons"              Auto-generate subdirs for App icons.
-e appicons=False                  Avoid generating App icons.
```


## Usage Examples: 

### Single file

Create a folder and put an IPA file inside it.\
In this example the folder is /tmp/ipas/\
And the IPA file is located here: /tmp/ipas/sample.ipa

Run following to extract the metadata and app icon:

```bash
docker run --rm -e filename="sample.ipa" -v /tmp/ipas/:/home/work/files ipax:latest
```

If everything worked out you'll see a result like this:
```
{"AppName": "sampleApp", "AppVersion": "1.0.1", "AppBundleIdentifier": "digital.discord.sample", "IconName": "sample.png", "FileName": "mySampleApp.ipa", "Timestamp": 1637676732}
```
The app icon will be located in the folder you specified with the -v parameter.\
In this case /tmp/ipas/\<md5 of ipa file\>.png

_The timestamp is a unix timestamp, the filesize is in bytes._

### Multiple files

You can also use ipax to parse all \*.ipa files in the folder specified by -v.\
Syntax:\
```docker run --rm -e multiple=True -v /tmp/ipas/:/home/work/files ipax:latest```

### Save JSON content as file using outfile parameter

Keep in mind following only accepts filenames, as the container is locked to the specified folder.\
```docker run --rm -e multiple=True -e outfile="result.json" -v /tmp/ipas/:/home/work/files ipax:latest```

This will save a result.json file in /tmp/ipas, this also works for single file mode.\

### Make output pretty

You can make the output more readable using the -e pretty="true" option.\
```docker run --rm -e multiple=True -e pretty=True -v /tmp/ipas/:/home/work/files ipax:latest```

### Enable default keys for output

In case you need the JSON output so you can search by key, you can either specify "bundleId" or "filename".\
You can combine this with the pretty argument and also the sort by key option:\
```docker run --rm -e multiple=True -e defaultkey="bundleId" -v /tmp/ipas/:/home/work/files ipax:latest```

### Sort by keys

In case you need the JSON output sorted alphabetically you can do so by enabling default keys and using the sortkey option:\
```docker run --rm -e multiple=True -e defaultkey="bundleId" -e sortkey=True -v /tmp/ipas/:/home/work/files ipax:latest```

### Save to sub-directories within workdir

You can make ipax auto-generate subdirs and put appicons and the outfile in own directories:\
```docker run --rm -e multiple=True -e appicondir="icons" -e outfiledir="json" -e outfile="result.json" -v /tmp/ipas/:/home/work/files ipax:latest```

### Disable generation of appicons

Sometimes it's useful that ipax doesn't generate the appicons.\
You can do so by specifying the appicons parameter:\
```docker run --rm -e multiple=True -e appicons=False -v /tmp/ipas/:/home/work/files ipax:latest```

# Extra information about iPAX: 

The app icon is extracted and then normalized automatically using **ipin.py** which is licensed under GPLv3 and you can find the original source code: [Click Here](https://axelbrz.com/?mod=iphone-png-images-normalizer).

This version of **ipin.py** is based on a modified version by urielka which you can find here: [Click Here](https://gist.github.com/urielka/3609051)

You can find **ipin.py** in the appdata folder.
I modified ipin.py so it doesn't convert already normalized images and prevents them from corrupting that way. I also removed the original code which selects the source image files for conversion and replaced it with a line that calls the updatePNG function with the first argument passed to the file.


## License

This project is licensed under the terms of the GNU license. See the [LICENSE](LICENSE) file.

> This project is open source under the GNU license, which means you have full access to the source code and can modify it to fit your own needs. All **iPAX** tools run on your own computer or server, so your credentials or other sensitive information will never leave your own computer. You are responsible for how you use **iPAX** tool.
