from os.path import join, exists
from ..libs.blender_utils import get_data, get_material

# Avatar_Girl_Sword_Furina_Mat_Face
# Avatar_Girl_Sword_Furina_Mat_Hair
# Avatar_Girl_Sword_Furina_Mat_Body
# Avatar_Girl_Sword_Furina_Mat_Dress
# Avatar_Girl_Sword_Furina_Mat_Effect
# Avatar_Default_Mat
file_prefix = None
texture_dir = None
prefix = 'HoYoverse - Genshin '
material_map = {
  'Face': f'{ prefix }Face',
  'Hair': f'{ prefix }Hair',
  'Body': f'{ prefix }Body',
  'Dress': f'{ prefix }Body',
  'Effect': f'{ prefix }Effect'
}
body_type_map = {
  'Loli': 1,
  'Boy': 2,
  'Girl': 3,
  'Male': 4,
  'Lady': 5
}

def nodes_set_image (
  nodes, 
  image_name, 
  alpha_mode = None, 
  colorspace_settings = None
):
  for node in nodes:
    node_set_image(node, image_name, alpha_mode, colorspace_settings)


def node_set_image (
  node, 
  image_name, 
  alpha_mode = None, 
  colorspace_settings = None
):
  if not image_name:
    node.image = None

    return
  
  image_name = f'{ file_prefix }_Tex_{ image_name }'
  # 先尝试从模型获取（缺少 lightmap，shadow ramp 等）
  image = get_data().images.get(image_name)

  if not image:
    image_path = join(texture_dir, image_name)

    # 3.0 之前不存在法向贴图
    if not exists(image_path):
      return
    
    image = get_data().images.load(image_path)

  if alpha_mode:
    image.alpha_mode = 'CHANNEL_PACKED'

  if colorspace_settings:
    image.colorspace_settings.name = colorspace_settings

  node.image = image

def import_materials (material_path):
  # HoYoverse - Genshin Body
  # HoYoverse - Genshin Face
  # HoYoverse - Genshin Hair
  # HoYoverse - Genshin Outlines
  with get_data().libraries.load(material_path, link = False) as (data_from, data_to):
    data_to.materials = data_from.materials

def init_face_diffuse (nodes):
  node_set_image(nodes['Face_Diffuse'], 'Face_Diffuse.png', 'CHANNEL_PACKED')

def init_body_type (nodes):
  # 设置脸部阴影的类型
  body_type = body_type_map[file_prefix.split('_')[1]]
  nodes["Face Shader"].inputs[0].default_value = body_type

def init_shadow_ramp (type):
  node_name = f'{ type }_Shadow_Ramp'
  node = get_data().node_groups.get(f'{ type } Shadow Ramp').nodes.get(node_name)
  node_set_image(node, f'{ node_name }.png', 'CHANNEL_PACKED')

def init_diffuse (material, type):
  node, node2 = get_nodes(material, f'{ type }_Diffuse_UV')
  image_name = f'{ type }_Diffuse.png'
  nodes_set_image([node, node2], image_name, 'CHANNEL_PACKED')

def init_lightmap (material, type):
  node, node2 = get_nodes(material, f'{ type }_Lightmap_UV')
  image_name = f'{ type }_Lightmap.png'
  nodes_set_image([node, node2], image_name, colorspace_settings = 'Non-Color')

def init_normalmap (material, type):
  node, node2 = get_nodes(material, f'{ type }_Normalmap_UV')
  image_name = f'{ type }_Normalmap.png'
  nodes_set_image([node, node2], image_name, colorspace_settings = 'Non-Color')

def reset_uv_map (material):
  # material.node_tree.nodes["UV Map"].uv_map = ""
  pass

def init_face_material ():
  nodes = get_material(f"HoYoverse - Genshin Face").node_tree.nodes
  init_face_diffuse(nodes)
  init_body_type(nodes)

def init_body_material ():
  material = get_material(f"HoYoverse - Genshin Body")
  init_shadow_ramp('Body')
  init_diffuse(material, 'Body')
  init_lightmap(material, 'Body')
  init_normalmap(material, 'Body')
  reset_uv_map(material)

def init_hair_material ():
  material = get_material(f"HoYoverse - Genshin Hair")
  init_shadow_ramp('Hair')
  init_diffuse(material, 'Hair')
  init_lightmap(material, 'Hair')
  init_normalmap(material, 'Hair')
  reset_uv_map(material)

def gen_and_init_effect_material(execute):
  def gen_effect_material ():
    hair_material = get_material('HoYoverse - Genshin Hair')
    effect_material = hair_material.copy()
    effect_material.name = 'HoYoverse - Genshin Effect'

    return effect_material
  
  def init_effect_material (material):
    node, node2 = get_nodes(material, 'Hair_Diffuse_UV')
    nodes_set_image([node, node2], 'EffectHair_Diffuse.png', 'CHANNEL_PACKED')
    node, node2 = get_nodes(material, 'Hair_Lightmap_UV')
    nodes_set_image([node, node2], 'EffectHair_Lightmap.png', colorspace_settings = 'Non-Color')
    node, node2 = get_nodes(material, 'Hair_Normalmap_UV')
    nodes_set_image([node, node2], None)

  if execute:
    effect_material = gen_effect_material()
    init_effect_material(effect_material)

def related_materials (armature):
  objects = armature.children
  # 收集 mesh，初始化全局光照时给这些 mesh 添加修改器
  mesh_list = set()

  for object in objects:
    if object.type == 'MESH':
      materials = object.data.materials

      for index, material in enumerate(materials):
        suffix = material.name.split('_')[-1]

        if suffix in material_map:
          mesh_list.add(object)
          materials[index] = get_material(material_map[suffix])

  return mesh_list

def get_nodes (material, node_name):
  nodes = material.node_tree.nodes

  # Body_Lightmap_UV0, Body_Lightmap_UV1
  return nodes[f'{ node_name }0'], nodes[f'{ node_name }1']

def _init_materials ():
  init_face_material()
  init_body_material()
  init_hair_material()

def init_global_vars (_file_prefix, _texture_dir):
  global file_prefix, texture_dir
  file_prefix = _file_prefix
  texture_dir = _texture_dir

def init_materials (armature, material_path, file_prefix, texture_dir, execute):
  init_global_vars(file_prefix, texture_dir)
  import_materials(material_path)
  _init_materials()
  gen_and_init_effect_material(execute)
  mesh_list = related_materials(armature)

  return mesh_list
