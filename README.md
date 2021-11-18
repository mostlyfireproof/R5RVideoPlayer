# R5Fresh

A video player for the Apex Legends mod R5Reloaded.

Here's a video of it playing Bad Apple: https://youtu.be/q6AvpuOgAvw

Huge credit to treyzania for his [rottenplayer](https://gitlab.com/delbonis/rottenplayer) for Minecraft.

My code is pretty bad at the moment, but I'll fix it up and make it easier to use in the future.

# Instructions:
1. Break up the video in to frames with something like ffmpeg, and place them in a folder called img/
2. Run `rotten.py <output file> <width> <height>` to process the images and turn them in to frames (the player only supports 32x18 video)
3. Run `freshparser.py <file from rotten> <final output>` to process it for Apex
4. Get and install the scripts from [here](https://github.com/mostlyfireproof/scripts_r5/tree/BadApple) for R5R
5. Copy the contents of the final output file in to `vscripts/mp/levels/animation.nut`
6. Launch Kings Canyon, find and press the button, then enjoy!
