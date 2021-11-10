# ipax - IPA Metadata Extractor

A docker image to extract common metadata from IPA files and also to extract and normalize app icons.


This docker image can be used to extract following items from IPA files:

* App Name
* App Version
* App Bundle Identifier
* App Icon

The app icon is extracted and then normalized automatically using ipin.py which is licensed under GPLv3 and you can find the original source code here: <https://axelbrz.com/?mod=iphone-png-images-normalizer>

This version of ipin.py is based on a modified version by urielka which you can find here: https://gist.github.com/urielka/3609051

You can find ipin.py in the appdata folder.

I modified ipin.py so it doesn't convert already normalized images and prevents them from corrupting that way. I also removed the original code which selects the source image files for conversion and replaced it with a line that calls the updatePNG function with the first argument passed to the file.

## Building the docker image

First you clone the repository:

```git clone https://github.com/DiscordDigital/ipax```

Then you go into the ipax folder and run following:

```docker build -t ipax:latest .```

Once it's built you can already use it.

## Running the image

### Single file

Create a folder and put an IPA file inside it.\
In this example the folder is /tmp/ipas/\
And the IPA file is located here: /tmp/ipas/sample.ipa

Run following to extract the metadata and app icon:

```docker run --rm -e filename="sample.ipa" -v /tmp/ipas/:/home/work/files ipax:latest```

If everything worked out you'll see a result like this:

```
{"AppName": "sampleApp", "AppVersion": "1.0.1", "AppBundleIdentifier": "digital.discord.sample", "IconName": "sample.png"}
```
The app icon will be located in the folder you specified with the -v parameter.\
In this case /tmp/ipas/\<md5 of ipa file\>.png

### Multiple files

You can also use ipax to parse all \*.ipa files in the folder specified by -v.\
Syntax:\
```docker run --rm -e multiple="true" -v /tmp/ipas/:/home/work/files ipax:latest```

### Save JSON content as file using outfile parameter

Keep in mind following only accepts filenames, as the container is locked to the specified folder.\
```docker run --rm -e multiple="true" -e outfile="result.json" -v /tmp/ipas/:/home/work/files ipax:latest```

This will save a result.json file in /tmp/ipas, this also works for single file mode.\

### Make output pretty

You can make the output more readable using the -e pretty="true" option.\
```docker run --rm -e multiple="true" -e pretty="true" -v /tmp/ipas/:/home/work/files ipax:latest```

### Enable default keys for output

In case you need the JSON output so you can search by key, you can either specify "bundleId" or "filename".\
You can combine this with the pretty argument and also the sort by key option.\
```docker run --rm -e multiple="true" -e defaultkey="bundleId" -v /tmp/ipas/:/home/work/files ipax:latest```

### Sort by keys

In case you need the JSON output sorted alphabetically you can do so by enabling default keys and using the sortkey option:\
```docker run --rm -e multiple="true" -e defaultkey="bundleId" -e sortkey="true" -v /tmp/ipas/:/home/work/files ipax:latest```

You can clone the repository and modify the scripts to your needs, the output is in a simple JSON format which can be parsed in various of scripting and programming languages.
