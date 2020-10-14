# ipax - IPA Metadata Extractor

A docker image to extract common metadata from IPA files and also to extract and normalize app icons.

---

This docker image can be used to extract following items from IPA files:

* App Name
* App Version
* App Bundle Identifier
* App Icon

The app icon is extracted and then normalized automatically using ipin.py which is licensed under GPLv3 and you can find the original source code here: <https://axelbrz.com/?mod=iphone-png-images-normalizer>

This version of ipin.py is based on a modified version by urielka which you can find here: https://gist.github.com/urielka/3609051

You can find ipin.py in the appdata folder.

I modified ipin.py so it doesn't convert already normalized images and prevents them from corrupting that way. I also removed the original code which selects the source image files for conversion and replaced it with a line that calls the important function with the first argument passed to the file.

## Building the docker image

First you clone the repository:

```git clone https://github.com/DiscordDigital/ipax```

Then you go into the ipax folder and run following:

```docker build -t ipax:latest .```

Once it's built you can already use it.

## Running the image

Create a folder and put an IPA file inside it.\
In this example the folder is /tmp/ipas/\
And the IPA file is located here: /tmp/ipas/sample.ipa

Run following to extract the metadata and app icon:

```docker run --rm -e filename="sample.ipa" -v /tmp/ipas/:/home/work/files ipax:latest```

If everything worked out you'll see a result like this:

```
{"AppName": "sampleApp", "AppVersion": "1.0.1", "AppBundleIdentifier": "digital.discord.sample", "IconName": "sample.png"}
```

You can clone the repository and modify the scripts to your needs, the output is in a simple JSON format which can be parsed in various of scripting and programming languages.
