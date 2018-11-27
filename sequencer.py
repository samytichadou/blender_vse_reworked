# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy
from bpy.types import Operator
from operator import attrgetter
from bpy.props import IntProperty


class SequencerCrossfadeSounds(Operator):
    """Do cross-fading volume animation of two selected sound strips"""

    bl_idname = "sequencer.crossfade_sounds"
    bl_label = "Crossfade sounds"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.scene and context.scene.sequence_editor and context.scene.sequence_editor.active_strip:
            return context.scene.sequence_editor.active_strip.type == 'SOUND'
        else:
            return False

    def execute(self, context):
        seq1 = None
        seq2 = None
        for s in context.scene.sequence_editor.sequences:
            if s.select and s.type == 'SOUND':
                if seq1 is None:
                    seq1 = s
                elif seq2 is None:
                    seq2 = s
                else:
                    seq2 = None
                    break
        if seq2 is None:
            self.report({'ERROR'}, "Select 2 sound strips")
            return {'CANCELLED'}
        if seq1.frame_final_start > seq2.frame_final_start:
            s = seq1
            seq1 = seq2
            seq2 = s
        if seq1.frame_final_end > seq2.frame_final_start:
            tempcfra = context.scene.frame_current
            context.scene.frame_current = seq2.frame_final_start
            seq1.keyframe_insert("volume")
            context.scene.frame_current = seq1.frame_final_end
            seq1.volume = 0
            seq1.keyframe_insert("volume")
            seq2.keyframe_insert("volume")
            context.scene.frame_current = seq2.frame_final_start
            seq2.volume = 0
            seq2.keyframe_insert("volume")
            context.scene.frame_current = tempcfra
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "The selected strips don't overlap")
            return {'CANCELLED'}
        
        
class SequencerRippleDelete(bpy.types.Operator):
    """Ripple delete strips"""
    
    bl_idname = "sequencer.ripple_delete"
    bl_label = "Ripple Delete Selection"
    bl_options = {'REGISTER', 'UNDO'}    

    @classmethod
    def poll(cls, context):
        if context.sequences:
            return True
        return False

    def execute(self, context):
        
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}        
        
        seq = context.scene.sequence_editor.active_strip
        distance = (seq.frame_final_end - seq.frame_final_start)

        for s in context.sequences: s.select=False
        seq.select = True
        seq_len = (seq.frame_final_end - seq.frame_final_start)

        bpy.ops.sequencer.select_active_side(side='RIGHT')
        seq.select=False
        sel_seqs = bpy.context.selected_sequences

        if sel_seqs: bpy.ops.sequencer.select_all(action='TOGGLE')

        seq.select=True
        bpy.ops.sequencer.delete()

        seqs=sel_seqs
        distance=-distance
        
        if distance >=0: list.sort(seqs, key=lambda x:-x.frame_final_start)
        else: list.sort(seqs,key=lambda x:x.frame_final_start)

        for s in seqs:
            if s.type not in {
            'CROSS', 'ADD', 'SUBTRACT', 'ALPHA_OVER', 'ALPHA_UNDER',
            'GAMMA_CROSS', 'MULTIPLY', 'OVER_DROP', 'WIPE', 'GLOW',
            'TRANSFORM', 'COLOR', 'SPEED', 'MULTICAM', 'ADJUSTMENT',
            'GAUSSIAN_BLUR', 'TEXT',
            }:
                s.frame_start += distance                   

        return {'FINISHED'}          
        
        
class SequencerCutMulticam(Operator):
    """Cut multi-cam strip and select camera"""

    bl_idname = "sequencer.cut_multicam"
    bl_label = "Cut multicam"
    bl_options = {'REGISTER', 'UNDO'}

    camera: IntProperty(
        name="Camera",
        min=1, max=32,
        soft_min=1, soft_max=32,
        default=1,
    )

    @classmethod
    def poll(cls, context):
        if context.scene and context.scene.sequence_editor and context.scene.sequence_editor.active_strip:
            return context.scene.sequence_editor.active_strip.type == 'MULTICAM'
        else:
            return False

    def execute(self, context):
        camera = self.camera

        s = context.scene.sequence_editor.active_strip

        if s.multicam_source == camera or camera >= s.channel:
            return {'FINISHED'}

        if not s.select:
            s.select = True

        cfra = context.scene.frame_current
        bpy.ops.sequencer.cut(frame=cfra, type='SOFT', side='RIGHT')
        for s in context.scene.sequence_editor.sequences_all:
            if s.select and s.type == 'MULTICAM' and s.frame_final_start <= cfra and cfra < s.frame_final_end:
                context.scene.sequence_editor.active_strip = s

        context.scene.sequence_editor.active_strip.multicam_source = camera
        return {'FINISHED'}


class SequencerDeinterlaceSelectedMovies(Operator):
    """Deinterlace all selected movie sources"""

    bl_idname = "sequencer.deinterlace_selected_movies"
    bl_label = "Deinterlace Movies"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.scene and context.scene.sequence_editor)

    def execute(self, context):
        for s in context.scene.sequence_editor.sequences_all:
            if s.select and s.type == 'MOVIE':
                s.use_deinterlace = True
        return {'FINISHED'}

class SequencerReverseSelectedMovies(Operator):
    """Reverse all selected movie sources"""

    bl_idname = "sequencer.reverse_selected_movies"
    bl_label = "Reverse Movies"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.scene and context.scene.sequence_editor)

    def execute(self, context):
        for s in context.scene.sequence_editor.sequences_all:
            if s.select and s.type == 'MOVIE':
                s.use_reverse_frames = True
        return {'FINISHED'}
        

class SequencerFlipXSelectedMovies(Operator):
    """Flip X of all selected movie sources"""

    bl_idname = "sequencer.flip_x_selected_movies"
    bl_label = "Flip X Movies"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.scene and context.scene.sequence_editor)

    def execute(self, context):
        for s in context.scene.sequence_editor.sequences_all:
            if s.select and s.type == 'MOVIE':
                s.use_flip_x = True
        return {'FINISHED'}


class SequencerFlipYSelectedMovies(Operator):
    """Flip Y of all selected movie sources"""

    bl_idname = "sequencer.flip_y_selected_movies"
    bl_label = "Flip Y Movies"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.scene and context.scene.sequence_editor)

    def execute(self, context):
        for s in context.scene.sequence_editor.sequences_all:
            if s.select and s.type == 'MOVIE':
                s.use_flip_y = True
        return {'FINISHED'}

        
class SequencerShowWaveformSelectedSounds(Operator):
    """Toggle draw waveform of all selected audio sources"""

    bl_idname = "sequencer.show_waveform_selected_sounds"
    bl_label = "Show Waveform"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.scene and context.scene.sequence_editor)

    def execute(self, context):

        for strip in context.scene.sequence_editor.sequences_all:
            if strip.select and strip.type == 'SOUND':
                if (strip.show_waveform is False):
                    strip.show_waveform = True
                elif (strip.show_waveform is True):
                    strip.show_waveform = False    

        return {'FINISHED'}     
        
class SequencerSelectTimeCursor(bpy.types.Operator):
    """Select strips at current frame"""
    
    bl_idname = "sequencer.select_time_cursor"
    bl_label = "Select Current Frame"
    bl_options = {"REGISTER", "UNDO"}
    
    all=bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return bpy.context.area.type=='SEQUENCE_EDITOR' and bpy.context.scene.sequence_editor is not None

    def execute(self, context):
        scn=bpy.context.scene
        cf=scn.frame_current
        active=''
        all=True
     
        for s in scn.sequence_editor.sequences_all:
            s.select=False
            s.select_left_handle=False
            s.select_right_handle=False
            
        playing=[] 
        for i in range(32,0,-1):
            for s in scn.sequence_editor.sequences_all:
                if s.frame_final_start<=cf and s.frame_final_end > cf and s.channel==i:
                    playing.append(s)
                    
        if len(playing)!=0:
            for s in playing:
                if s.mute==False and active=='':
                    active=s
                if all==True:
                    s.select=True
                else:
                    if active!='':
                        active.select=True
        if active!='':
            scn.sequence_editor.active_strip=active
            
        return {"FINISHED"}     

class SequencerSelectChannel(Operator):
    """Add Entire Channel to Selection"""

    bl_idname = "sequencer.select_channel"
    bl_label = "Select Channel"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.scene and context.scene.sequence_editor)

    def execute(self, context):
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}

        selection = sorted(selection, key=attrgetter('channel', 'frame_final_start'))

        sequences = bpy.context.scene.sequence_editor.sequences_all
        
        for s in selection:
            for strip in sequences:        
                if s.channel == strip.channel:      
                    strip.select = strip.channel == s.channel
                    
        return {'FINISHED'}        
 
import bpy

class SequencerSelectAllLockedStrips(bpy.types.Operator):
    '''Select all locked strips'''
    bl_idname = "sequencer.select_all_locked_strips"
    bl_label = "Select All Locked Strips"
    bl_description = "Select all locked strips"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.sequences:
            return True
        return False

    def execute(self, context):
        lockedStrips = []
        for strip in bpy.context.sequences:
            if strip.lock:
                lockedStrips.append(strip)
        try:
            if lockedStrips != []:
                bpy.ops.sequencer.select_all(action='DESELECT')
                for strip in lockedStrips:
                    strip.select = True
        except:
            pass

        return {'FINISHED'}


class SequencerSelectAllMuteStrips(bpy.types.Operator):
    '''Select all muted/hidden strips'''
    bl_idname = "sequencer.select_all_mute_strips"
    bl_label = "Select All Muted/Hidden"
    bl_description = "Select all muted/hidden strips"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.sequences:
            return True
        return False

    def execute(self, context):
        muteStrips = []
        for strip in bpy.context.sequences:
            if strip.mute:
                muteStrips.append(strip)
        try:
            if muteStrips != []:
                bpy.ops.sequencer.select_all(action='DESELECT')
                for strip in muteStrips:
                    strip.select = True
        except:
            pass

        return {'FINISHED'}

class SequencerToggleAllModifiers(bpy.types.Operator):
    '''Toggle all modifiers on/off'''
    bl_idname = "sequencer.toggle_all_modifiers"
    bl_label = "Toggle all modifiers"
    bl_description = "Toggle all modifiers on/off"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.sequences:
            return True
        return False

    selection_only = bpy.props.BoolProperty(
        name="Only Selected",
        default=False,
        description="Only apply to selected strips")

    showhide = bpy.props.EnumProperty(
        items = [('show', 'Show', 'Make modifiers visible'),
                ('hide', 'Hide', 'Make modifiers not visible'),
                ('toggle', 'Toggle', 'Toggle modifier visilibity per modifier')],
        name = "show/hide",
        default="toggle",
        description = "Show, hide, or toggle all strip modifier")

    def execute(self, context):

        stps = []
        if self.selection_only==True:
            stps = [seq for seq in context.scene.sequence_editor.sequences if seq.select]
        else:
            stps = context.scene.sequence_editor.sequences

        for stp in stps:
            for mod in stp.modifiers:
                if self.showhide=="show":
                    mod.mute=False
                elif self.showhide=="hide":
                    mod.mute=True
                else:
                    mod.mute = not mod.mute

        return {'FINISHED'}     
 
class SequencerAudioMuteToggle(bpy.types.Operator):
    '''Toggle audio on/off'''
    bl_idname = "screen.audio_mute_toggle"
    bl_label = "Audio Mute Toggle"
    bl_description = "Toggle all audio on/off"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.sequences:
            return True
        return False
    
    def execute(self, context):
    
        bpy.context.scene.use_audio = not bpy.context.scene.use_audio

        return {'FINISHED'}  

class SequencerPreviewEndInCurrent(bpy.types.Operator):
    """Sets preview end to current frame"""
    bl_idname = "sequencer.preview_end_in_current"
    bl_label = "Preview End to Current"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def execute(self, context):
        scene = bpy.context.scene
        # the -1 below is because we want the scene to end where the cursor is
        # positioned, not one frame after it (as scene.frame_current behaves)
        scene.frame_end = scene.frame_current - 1
        scene.frame_preview_end = scene.frame_current - 1

        return {'FINISHED'}


class SequencerPreviewStartInCurrent(bpy.types.Operator):
    """Sets Preview start to current frame"""
    bl_idname = "sequencer.preview_start_in_current"
    bl_label = "Preview Start to Current"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def execute(self, context):
        scene = bpy.context.scene
        scene.frame_start = scene.frame_current
        scene.frame_preview_start = scene.frame_current

        return {'FINISHED'}

class SequencerPreviewSelected(bpy.types.Operator):
    """Sets preview range to selected strips"""
    bl_idname = "sequencer.preview_selected"
    bl_label = "Preview Selected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def execute(self, context):
        scene = bpy.context.scene
        selectedStrips = bpy.context.selected_sequences

        reference = 0
        for strip in selectedStrips:
            if strip.frame_final_end > reference:
                reference = strip.frame_final_end

        for strip in selectedStrips:
            stripStart = strip.frame_start + strip.frame_offset_start
            if (stripStart < reference):
                reference = stripStart

        scene.frame_start = reference
        scene.frame_preview_start = reference

        for strip in selectedStrips:
            if (strip.frame_final_end > reference):
                reference = strip.frame_final_end - 1

        scene.frame_end = reference
        scene.frame_preview_end = reference

        return {'FINISHED'}

class SequencerSplitExtractLeft(bpy.types.Operator):
    """Splits selected strips and extracts to the left"""
    bl_idname = "sequencer.split_extract_left"
    bl_label = "Split Extract Left"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def execute(self, context):
        
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}
                
        scene = bpy.context.scene
        sequencer = bpy.ops.sequencer

        sequencer.cut(frame=scene.frame_current, type='SOFT', side='LEFT')
        sequencer.delete()

        return {'FINISHED'}


class SequencerSplitExtractRight(bpy.types.Operator):
    """Splits selected strip and extracts to the right"""
    bl_idname = "sequencer.split_extract_right"
    bl_label = "Split Extract Right"
    bl_options = {'REGISTER', 'UNDO'}
    # Shortcut: Alt + K

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def execute(self, context):
        
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}
        
        scene = bpy.context.scene
        sequencer = bpy.ops.sequencer

        sequencer.cut(frame=scene.frame_current, type='SOFT', side='RIGHT')
        sequencer.delete()

        return {'FINISHED'}


classes = (
    SequencerCrossfadeSounds,
    SequencerCutMulticam,
    SequencerDeinterlaceSelectedMovies,
    SequencerReverseSelectedMovies,
    SequencerFlipXSelectedMovies,
    SequencerFlipYSelectedMovies,
    SequencerShowWaveformSelectedSounds,
    SequencerRippleDelete,
    SequencerSelectTimeCursor,
    SequencerSelectChannel,
    SequencerSelectAllLockedStrips,
    SequencerSelectAllMuteStrips,
    SequencerToggleAllModifiers,
    SequencerAudioMuteToggle,
    SequencerPreviewStartInCurrent,
    SequencerPreviewEndInCurrent,
    SequencerPreviewSelected,
    SequencerSplitExtractLeft,
    SequencerSplitExtractRight,
)
