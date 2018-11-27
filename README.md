# BLENDER VIDEO SEQUENCE EDITOR - REWORKED

A suggestion for reworking the Blender 2.80 VSE menus and additional functions.

### New function added to the menu:

- Select Strips Under Cursor(new function)
- Select All Strips in Selected Channel(new function)
- Select Locked Strips(new function)
- Select Muted/Hidden Strips(new function)
- Cut > Extract (Ripple Delete)(new function)
- Toggle All Modifiers On/Off(new function)
- Toggle Audio Icon-Button in Header(new function)
- Set Preview Start
- Set Preview End
- Set Preview Selected
- Split Lift Left
- Split Lift Right


### Existing functions added to menu:

- Select Time Code Style
- Render/Downmix Audio
- Rearranged the menus in the order the user will need them. Except "View" because of consistency.
- Divided them into shorter menus.
- Toggle Meta Strips
- Un-Mute/Un-Hide Deselected
- Jump to Keyframe/Start/End)
- Zoom Border...
- Flip X/Y
- Reverse

### Installation:

Download and place the two files included into these paths before starting Blender 2.80:
https://github.com/tin2tin/blender_vse_reworked/raw/master/sequencer.py
- 2.80\scripts\startup\bl_operators\sequencer.py

https://github.com/tin2tin/blender_vse_reworked/raw/master/space_sequencer.py
- 2.80\scripts\startup\bl_ui\space_sequencer.py

### Contribute:

- If you want to contribute and run the space_sequencer.py from the Blender 2.80
Text Editor you'll need to also open: "\blender-2.80.0-git.63150511a29-windows64\2.80\scripts\startup\bl_ui\properties_grease_pencil_common.py" in the Text Editor to avoid errors.

- Code clean up so it will apply with the Blender 2.80 python code guidelines. Most of the functions originates from other sources, so we need help to make it consistent, bug free and comply with the blender standarts for submittet code.

- Create and share a keymap for the new menus and functions(no coding experience needed):
Some functions can be right clicked and choose "Assing shortcut" and other functions needs to be added or changed in the 'User Preferences > Input' menu, which also is where you can save your keymap so it can be shared.
https://blendersensei.com/wp-content/uploads/2015/09/Create-Your-Own-Hotkey.jpg

- Share your opinion on what additional edit functions(existing python operators), which can be executed from the menu, should we add?
Let us know here or on the VSE chat: https://blender.chat/channel/vse

### Inspiration:

For inspiration take a look at all the add-ons created for the VSE: 
https://docs.google.com/document/d/e/2PACX-1vSBzP9e0JbKlXa-oHJYxsUoFpvGsiPfeX5MXRdnQmKB55COr4J8JGw6orlJb6r0kjR0RMM3Jv4Vz_zX/pub


