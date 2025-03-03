from ..libs.blender_utils import register_classes, unregister_classes
from .add_armature import add_armature
from .add_head_bone_name import add_head_bone_name
from .add_avatar import add_avatar

# classes = ()

def register():
  # register_classes(classes)
  add_armature()
  add_head_bone_name()
  add_avatar()
  
def unregister():
  # unregister_classes(classes)
  pass
