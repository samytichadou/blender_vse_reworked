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
from bpy.props import (
    IntProperty,
    BoolProperty,
    EnumProperty,
    StringProperty,
)


class SEQUENCER_OT_CrossfadeSounds(Operator):
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
        
                                   
class SEQUENCER_OT_CutMulticam(Operator):
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


class SEQUENCER_OT_DeinterlaceSelectedMovies(Operator):
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


class SEQUENCER_OT_ReverseSelectedMovies(Operator):
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
        

class SEQUENCER_OT_FlipXSelectedMovies(Operator):
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


class SEQUENCER_OT_FlipYSelectedMovies(Operator):
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

        
class SEQUENCER_OT_ShowWaveformSelectedSounds(Operator):
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

        
class SEQUENCER_OT_SelectTimeCursor(bpy.types.Operator):
    """Select strips at current frame"""
    
    bl_idname = "sequencer.select_time_cursor"
    bl_label = "Select Current Frame"
    bl_options = {"REGISTER", "UNDO"}
    
    all=bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return bpy.context.area.type=='SEQUENCE_EDITOR' and bpy.context.scene.sequence_editor is not None

    def execute(self, context):
        cFrame = bpy.context.scene.frame_current
        selStrips = []
        lockNum = 0                                     
        lockSelNum = 0                                      
        reportMessage = ""
        for strip in bpy.context.sequences:
            if strip.lock and strip.select:                         
                lockSelNum += 1
            try:
                if strip.frame_final_end >= cFrame:
                    if strip.frame_final_start <= cFrame:
                        if strip.lock and not strip.select:
                            lockNum += 1
                        else:
                            strip.select=True               
                            selStrips.append(strip)
            except:
                pass
        if selStrips != []:
            for strip in selStrips:
                try:
                    if strip.frame_final_end == cFrame:
                        strip.select_right_handle = True
                    elif strip.frame_final_start == cFrame:
                        strip.select_left_handle = True
                except:
                    pass
            
        return {"FINISHED"}     


class SEQUENCER_OT_SelectChannel(Operator):
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
    

class SEQUENCER_OT_SelectAllLockedStrips(bpy.types.Operator):
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


class SEQUENCER_OT_SelectAllMuteStrips(bpy.types.Operator):
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


class SEQUENCER_OT_ToggleAllModifiers(bpy.types.Operator):
    '''Toggle all modifiers on/off'''
    bl_idname = "sequencer.toggle_all_modifiers"
    bl_label = "Toggle all modifiers"
    bl_description = "Toggle all modifiers on/off"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

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

 
class SEQUENCER_OT_AudioMuteToggle(bpy.types.Operator):
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


class SEQUENCER_OT_SetPreviewRange(bpy.types.Operator):
    """Sets preview end to current frame"""
    bl_idname = "sequencer.set_preview_range"
    bl_label = "Preview End to Current"
    bl_options = {'REGISTER', 'UNDO'}
    type: EnumProperty(
        name="Type", description="Set Type",
        items=(
            ('IN', "In", "Set In"),
            ('OUT', "Out", "Set Out"),
        ),
    )
    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def execute(self, context):
        scene = bpy.context.scene
        if self.type == "OUT":
            # the -1 below is because we want the scene to end where the cursor is
            # positioned, not one frame after it (as scene.frame_current behaves)
            scene.frame_end = scene.frame_current - 1
            scene.frame_preview_end = scene.frame_current - 1
        else:
            scene.frame_start = scene.frame_current
            scene.frame_preview_start = scene.frame_current            

        return {'FINISHED'}


class SEQUENCER_OT_PreviewSelected(bpy.types.Operator):
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


class SEQUENCER_OT_SplitExtract(bpy.types.Operator):
    """Splits selected strips and extracts"""
    bl_idname = "sequencer.split_extract"
    bl_label = "Split Extract"
    bl_options = {'REGISTER', 'UNDO'}
    direction: EnumProperty(
        name="Direction", description="Split Extract Direction",
        items=(
            ('LEFT', "Left", "Split Extract Direction Left"),
            ('RIGHT', "Right", "Split Extract Direction Right"),
        ),
    )
    @classmethod
    def poll(cls, context):
        if context.sequences:
            return True
        return False

    def execute(self, context):
        scene = bpy.context.scene
        sequencer = bpy.ops.sequencer        
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}
          
        for s in selection:
            if not s.lock:
                bpy.ops.sequencer.select_all(action='DESELECT') 
                s.select = True
                sequencer.cut(frame=scene.frame_current, type='SOFT', side=self.direction)
                sequencer.ripple_delete()
                s.select = False                        
                for s in selection: s.select = True 

        return {'FINISHED'}


class SEQUENCER_OT_SplitLift(bpy.types.Operator):
    """Splits selected strips and lifts"""
    bl_idname = "sequencer.split_lift"
    bl_label = "Split Lift"
    bl_options = {'REGISTER', 'UNDO'}

    direction: EnumProperty(
        name="Direction", description="Split Lift Direction",
        items=(
            ('LEFT', "Left", "Split Lift Direction Left"),
            ('RIGHT', "Right", "Split Lift Direction Right"),
        ),
    )

    @classmethod
    def poll(cls, context):
        if context.sequences:
            return True
        return False

    def execute(self, context):
        
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}
                
        scene = bpy.context.scene
        sequencer = bpy.ops.sequencer

        sequencer.cut(frame=scene.frame_current, type='SOFT', side=self.direction)
        sequencer.delete_lift()

        return {'FINISHED'}


class SEQUENCER_OT_DeleteLift(bpy.types.Operator):
    """Lift strips"""
    
    bl_idname = "sequencer.delete_lift"
    bl_label = "Lift Selection"
    bl_options = {'REGISTER', 'UNDO'}    

    @classmethod
    def poll(cls, context):
        if context.sequences:
            return True
        return False

    def execute(self, context):

        selection = context.selected_sequences
        #bpy.ops.sequencer.copy() #Can't copy strips involved in transitions        
        if not selection:
            return {'CANCELLED'}        

        for s in selection:
            if not s.lock:
                bpy.ops.sequencer.select_all(action='DESELECT') 
                s.select = True
                bpy.ops.sequencer.delete()  
                s.select = False                        
                for s in selection: s.select = True 

        return {'FINISHED'} 


class SEQUENCER_OT_RippleDelete(bpy.types.Operator):
    """Ripple Delete strips"""
    
    bl_idname = "sequencer.ripple_delete"
    bl_label = "Ripple Delete Selection"
    bl_options = {'REGISTER', 'UNDO'}    

    @classmethod
    def poll(cls, context):
        if context.sequences:
            return True
        return False

    def execute(self, context):

        #bpy.ops.sequencer.copy() #Can't copy strips involved in transitions
        selection = context.selected_sequences
        selection = sorted(selection, key=attrgetter('channel', 'frame_final_start'))
        
        if not selection:
            return {'CANCELLED'}  
                            
        for seq in selection:
            if seq.lock == False:            
                context.scene.sequence_editor.active_strip = seq # set as active or it won't work
                distance = (seq.frame_final_end - seq.frame_final_start) 
                bpy.ops.sequencer.select_all(action='DESELECT') 
                seq.select = True

                bpy.ops.sequencer.select_active_side(side='RIGHT') # Select to the right
                seq.select=False
                seqs = context.selected_sequences

                bpy.ops.sequencer.select_all(action='DESELECT') # cut only active strip
                seq.select=True   
                seq_out= seq.frame_final_end      
                bpy.ops.sequencer.delete()

                seqs = sorted(seqs, key=attrgetter('channel', 'frame_final_start'))
                
                # delete effect strips(ex. dissolves) if they are adjoined selected strips:
                if len(seqs)-1 > 1:
                    if seqs[1].type in {
                    'CROSS', 'ADD', 'SUBTRACT', 'ALPHA_OVER', 'ALPHA_UNDER',
                    'GAMMA_CROSS', 'MULTIPLY', 'OVER_DROP', 'WIPE', 'GLOW',
                    'TRANSFORM', 'COLOR', 'SPEED', 'MULTICAM', 'ADJUSTMENT',
                    'GAUSSIAN_BLUR', 'TEXT',
                    }:    
                        seqs[1].select=True  
                        #distance = distance + (seqs[1].frame_final_duration) # can't get the duration of the transition?         
                        bpy.ops.sequencer.delete()                                

                distance=-distance
                
                for s in seqs:
                    if s.lock == True:
                        break
                    if s.type not in {
                    'CROSS', 'ADD', 'SUBTRACT', 'ALPHA_OVER', 'ALPHA_UNDER',
                    'GAMMA_CROSS', 'MULTIPLY', 'OVER_DROP', 'WIPE', 'GLOW',
                    'TRANSFORM', 'COLOR', 'SPEED', 'MULTICAM', 'ADJUSTMENT',
                    'GAUSSIAN_BLUR', 'TEXT',
                    }:
                        s.frame_start += distance                   

        return {'FINISHED'}  


class SEQUENCER_OT_ZoomVertical(bpy.types.Operator):
    """Zoom Vertical"""
    
    bl_idname = "sequencer.zoom_vertical"
    bl_label = "Zoom Vertical"
    bl_options = {'REGISTER', 'UNDO'}    

    direction: EnumProperty(
        name="Direction", description="Vertical Zoom Direction",
        items=(
            ('OUT', "Out", "Zoom Vertical Out"),
            ('IN', "In", "Zoom Vertical In"),
        ),
    )

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def execute(self, context):
      
        if self.direction == "OUT": 
            bpy.ops.view2d.zoom(deltay=-1) 
        else:         
            bpy.ops.view2d.zoom(deltay=1) 

        return {'FINISHED'} 


class SEQUENCER_OT_MatchFrame(bpy.types.Operator):
    """Add full source to empty channel and match frame"""
    
    bl_idname = "sequencer.match_frame"
    bl_label = "Match Frame"
    bl_options = {'REGISTER', 'UNDO'}    

    @classmethod
    def poll(cls, context):
        return bpy.context.scene is not None

    def execute(self, context):
        
        selection = context.selected_sequences
        selection = sorted(selection, key=attrgetter('channel', 'frame_final_start'))
        
        if not selection:
            return {'CANCELLED'}  
                            
        for seq in selection: 

            if seq.type not in {
            'CROSS', 'ADD', 'SUBTRACT', 'ALPHA_OVER', 'ALPHA_UNDER',
            'GAMMA_CROSS', 'MULTIPLY', 'OVER_DROP', 'WIPE', 'GLOW',
            'TRANSFORM', 'COLOR', 'SPEED', 'MULTICAM', 'ADJUSTMENT',
            'GAUSSIAN_BLUR', 'TEXT',
            }:
                 
                # Find empty channel:
                sequences = bpy.context.sequences
                if not sequences:
                    return 1
                channels = [s.channel for s in sequences]
                channels = sorted(list(set(channels)))
                empty_channel = channels[-1] + 1 
                
                # Duplicate strip to first empty channel and clear offsets
                if empty_channel < 33:
                    bpy.ops.sequencer.select_all(action='DESELECT')
                    seq.select = True
                    context.scene.sequence_editor.active_strip = seq # set as active or it won't work
                    bpy.ops.sequencer.duplicate_move(
                    SEQUENCER_OT_duplicate={"mode":'TRANSLATION'},
                    TRANSFORM_OT_seq_slide={
                    "value":(0, empty_channel-seq.channel),
                    "snap":False,
                    "snap_target":'CLOSEST',
                    "snap_point":(0, 0, 0),
                    "snap_align":False,
                    "snap_normal":(0, 0, 0),
                    "release_confirm":False,
                    "use_accurate":False},
                    )
                    bpy.ops.sequencer.offset_clear()

        #re-select previous selection
        for seq in selection:                
            seq.select = True

        return {'FINISHED'} 


class SEQUENCER_OT_Split(bpy.types.Operator):
    """Split Unlocked Un/Seleted Strips Soft"""
    
    bl_idname = "sequencer.split"
    bl_label = "Split Soft"
    bl_options = {'REGISTER', 'UNDO'}    

    type: EnumProperty(
        name="Type", description="Split Type",
        items=(
            ('SOFT', "Soft", "Split Soft"),
            ('HARD', "Hard", "Split Hard"),
        ),
    )

    @classmethod
    def poll(cls, context):
        if context.sequences:
            return True
        return False

    def execute(self, context):
        selection = context.selected_sequences
        sequences = bpy.context.scene.sequence_editor.sequences_all
        cf = bpy.context.scene.frame_current
        at_cursor = [] 
        cut_selected = False

        #find unlocked strips at cursor 
        for s in sequences:
            if s.frame_final_start<=cf and s.frame_final_end > cf:
                if s.lock == False:
                    at_cursor.append(s)
                    if s.select == True: 
                        cut_selected = True

        for s in at_cursor:
            if cut_selected: 
                if s.select:    #only cut selected  
                    bpy.ops.sequencer.select_all(action='DESELECT') 
                    s.select = True
                    bpy.ops.sequencer.cut(frame=bpy.context.scene.frame_current, type = self.type)                                            
                    bpy.ops.sequencer.select_all(action='DESELECT')                        
                    for s in selection: s.select = True     
                                  
            else:               #cut unselected
                bpy.ops.sequencer.select_all(action='DESELECT') 
                s.select = True
                bpy.ops.sequencer.cut(frame=bpy.context.scene.frame_current, type = self.type)                 
                bpy.ops.sequencer.select_all(action='DESELECT')                       
                for s in selection: s.select = True         
        return {'FINISHED'}   


class SEQUENCER_OT_ExtendToFill(bpy.types.Operator):
    bl_idname = 'sequencer.extend_to_fill'
    bl_label = 'Extend to Fill'
    bl_description = 'Extend selected strips forward to fill adjacent space'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        scn = context.scene
        if scn and scn.sequence_editor:
            return True
        else:
            return False

    def execute(self, context):
        scn = context.scene
        seq = scn.sequence_editor
        selection = context.selected_sequences        
        meta_level = len(seq.meta_stack)

        if meta_level > 0:
            seq = seq.meta_stack[meta_level - 1]
        
        if not selection:
            return {'CANCELLED'}  
                            
        for strip in selection:
            if strip.lock == False and strip.type not in {
            'CROSS', 'ADD', 'SUBTRACT', 'ALPHA_OVER', 'ALPHA_UNDER',
            'GAMMA_CROSS', 'MULTIPLY', 'OVER_DROP', 'WIPE', 'GLOW',
            'TRANSFORM', 'COLOR', 'SPEED', 'MULTICAM', 'ADJUSTMENT',
            'GAUSSIAN_BLUR', 'TEXT',
            }:            
                context.scene.sequence_editor.active_strip = strip # set as active or it won't work            
        
                chn = strip.channel
                stf = strip.frame_final_end
                enf = 300000

                for i in seq.sequences:
                    ffs = i.frame_final_start
                    if (i.channel == chn and ffs > stf):
                        if ffs < enf:
                            enf = ffs
                if enf == 300000 and stf < scn.frame_end:
                    enf = scn.frame_end

                if enf == 300000 or enf == stf:
                    self.report({'ERROR_INVALID_INPUT'}, 'Unable to extend')
                    return {'CANCELLED'}
                else:
                    strip.frame_final_end = enf

        bpy.ops.sequencer.reload()
        return {'FINISHED'}


classes = (
    SEQUENCER_OT_CrossfadeSounds,
    SEQUENCER_OT_CutMulticam,
    SEQUENCER_OT_DeinterlaceSelectedMovies,
    SEQUENCER_OT_ReverseSelectedMovies,
    SEQUENCER_OT_FlipXSelectedMovies,
    SEQUENCER_OT_FlipYSelectedMovies,
    SEQUENCER_OT_ShowWaveformSelectedSounds,
    SEQUENCER_OT_SelectTimeCursor,
    SEQUENCER_OT_SelectChannel,
    SEQUENCER_OT_SelectAllLockedStrips,
    SEQUENCER_OT_SelectAllMuteStrips,
    SEQUENCER_OT_ToggleAllModifiers,
    SEQUENCER_OT_AudioMuteToggle,
    SEQUENCER_OT_SetPreviewRange,
    SEQUENCER_OT_PreviewSelected,
    SEQUENCER_OT_SplitExtract,
    SEQUENCER_OT_SplitLift,
    SEQUENCER_OT_DeleteLift, 
    SEQUENCER_OT_RippleDelete, 
    SEQUENCER_OT_ZoomVertical,
    SEQUENCER_OT_MatchFrame,
    SEQUENCER_OT_Split,  
    SEQUENCER_OT_ExtendToFill,  
)
