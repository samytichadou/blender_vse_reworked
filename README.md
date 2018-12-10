# BLENDER VIDEO SEQUENCE EDITOR - REWORKED

A suggestion for reworking the Blender 2.80 VSE menus and additional functions.

### New functions added to the menu:

- Select Strips Under Cursor
- Select All Strips in Selected Channel
- Select Locked Strips
- Select Muted/Hidden Strips
- Cut > Extract (Ripple Delete)
- Toggle All Modifiers On/Off
- Toggle Audio Icon-Button in Header
- Show Waveform in Selected
- Set Preview Start
- Set Preview End
- Set Preview Selected
- Split & Lift Left
- Split & Lift Right
- Split & Extract Left
- Split & Extract Right
- Zoom X/Y
- Match Frame
- Proper Soft/Hard Split
- Preserve Locked Strips from split, extract and delete
- Extend to fill
- Move in Steps


### Existing functions added to menu:

- Select Time Code Style
- Render/Downmix Audio
- Rearranged the menus in the order the user will need them. Except "View" because of consistency.
- Divided them into shorter menus.
- Toggle Meta Strips
- Un-Mute/Un-Hide Deselected
- Jump to Keyframe/Start/End
- Zoom Border...
- Flip X/Y
- Reverse
- Remove All Gaps
- Select Box...


### Installation:

Video tutorial: https://youtu.be/nN4xG3FMH-o

Download and place the two files included into these paths before starting Blender 2.80:

Download: https://github.com/tin2tin/blender_vse_reworked/raw/master/sequencer.py

Overwrite this file: 2.80\scripts\startup\bl_operators\sequencer.py


Download: https://github.com/tin2tin/blender_vse_reworked/raw/master/space_sequencer.py

Overwrite this file: 2.80\scripts\startup\bl_ui\space_sequencer.py


Download: https://raw.githubusercontent.com/tin2tin/blender_vse_reworked/master/vse_keymap.blend.py

Import the keymap: Edit > Settings... > Input > Import Key Configuration 

### Contribute:

- Share your opinion on what additional edit functions(existing python operators), which can be executed from the menu, should we add?
Let us know here or on the VSE chat: https://blender.chat/channel/vse

- Create and share a keymap for the new menus and functions(no coding experience needed):
Some functions can be right clicked and choose "Assing shortcut" and other functions needs to be added or changed in the 'User Preferences > Input' menu, which also is where you can save your keymap so it can be shared.
https://blendersensei.com/wp-content/uploads/2015/09/Create-Your-Own-Hotkey.jpg

- Code clean up so it will apply with the Blender 2.80 python code guidelines. Most of the functions originates from other sources, so we need help to make it consistent, bug free and comply with the blender standarts for submittet code.

- If you want to contribute and run the space_sequencer.py from the Blender 2.80
Text Editor you'll need to also open: 
"\2.80\scripts\startup\bl_ui\properties_grease_pencil_common.py"
"2.80\scripts\startup\bl_ui\space_time.py"
in the Text Editor to avoid errors.


### Inspiration:

For inspiration take a look at all the add-ons created for the VSE: 
https://docs.google.com/document/d/e/2PACX-1vSBzP9e0JbKlXa-oHJYxsUoFpvGsiPfeX5MXRdnQmKB55COr4J8JGw6orlJb6r0kjR0RMM3Jv4Vz_zX/pub


