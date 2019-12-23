# MilkdropBatchScreenshot
During the early versions of NestDrop, I needed a way to automatically capture screenshots of about 10,000 presets.

_Code by Nathan Williams - Concept by Jason Fletcher_

### Dependencies
Winamp v5.66  
Python 2.7.16 x86  
[Pyautowin](https://pywinauto.github.io/)  
[Pillow](https://python-pillow.org/)  

### Usage
```
python MilkdropBatchScreenshot.py
```

### Prior to running, here are some things to setup in Winamp
* Within the presets folder _(C:\Program Files (x86)\Winamp\Plugins\Milkdrop2\presets)_ create four folders: DONE, PRIOR, SCREENSHOTS, TODO. Then move all of your presets into the TODO folder.
* Here is a hack to avoid the song title annoucement being visible in the Milkdrop visuals. Grab an MP3 that you are ok deleting later on. In the Winamp playlist window, right-click on a song, select "edit metadata for selection", and delete any metadata info within. Then in the Windows browser, rename the MP3 to literally be "..mp3" (yes the filename is a single period). Add this renamed mp3 to be the only song in the Winamp playlist window. Now only a period will show up for the song title annoucement when Milkdrop starts up. This playlist will be automatically saved between each session. (FYI the Milkdrop 'VJ MODE' does not disable the initial song title annoucement, hence this hack.)
* In the Milkdrop settings, make sure that 'VJ MODE' is disabled. Even though this setting hides all alerts from the visualizer window, it sometimes steals the focus of the python script.
* Close any other Winamp windows, just have Winamp and Milkdrop window open. Set the desired size and aspect ratio of Milkdrop window (for the screenshots). Close and re-open Winamp to confirm that the Milkdrop window size has been saved. If you find that Milkdrop window size will not save, then try changing the size AND location of the Winamp and Milkdrop window to force a refresh of the cached settings.
* Within Milkdrop, load a preset (hotkey: L) and make sure that it is pointed to the root preset folder _(C:\Program Files (x86)\Winamp\Plugins\Milkdrop2\presets)_. If it is instead pointed to a different folder then the script will not function correctly and the screenshots filenames will not match the correct presets.
* If the preset filename is too long and exceeds the max file path of Windows, then the python script will fail ("IOerror: no such file or directory").
* This script is currently set to automatically capture 3 screenshots of each preset. If you rather capture a different amount, then just edit line #112 of the python script. <for i in range(1,4):>
* When you're ready to start the python script, make sure to close Winamp prior to executing. The python script will open Winamp on its own.
* To stop a session that is currently running, hit CTRL-ALT-DEL and wait two seconds. This will force a time out of the python script.

### After the screenshots are completed
If you want to crop out the Milkdrop window frame and be left with just the preset visuals, then I suggest using Photoshop. This can be achieved in Photoshop by creating a custom action which crops a precise region of an image. Then this action can be automatically applied to a whole folder of images by running it as a batch (file > automate > batch). Although this assumes that all of your screenshots are the exact same resolution, otherwise the crop will not all line up for all images.
