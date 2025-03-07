from ..libs.blender_utils import (
  register_classes, 
  unregister_classes, 
  get_props, 
  get_types
)

from ..const import bl_idname

class Preferences (get_types('AddonPreferences')):
  bl_idname = bl_idname

  texture_dir: get_props().StringProperty(
    name = 'Directory',
    subtype = 'DIR_PATH',
    default = 'D:\gi_assets' # For test
  )
  language: get_props().EnumProperty(
    name = 'language',
    items = [
       ('ZH', 'ZH', ''),
       ('EN', 'EN', '')
    ]
  )

  def draw(self, context):
    layout = self.layout
    row = layout.row()
    row.prop(self, 'texture_dir', text = 'Texture Dir')
    row = layout.row()
    row.prop(self, 'language', text = 'Language')

classes = (Preferences, )

def register():
  register_classes(classes)
  
def unregister():
  unregister_classes(classes)
