from os import path

join = path.join
dirname = path.dirname
abspath = path.abspath

texture_dir = join(dirname(abspath(__file__)), './assets/textures')
bl_category = 'GI Shaders'
material_prefix = 'HoYoverse - Genshin '
outline_material_prefix = 'HoYoverse - Genshin Outlines '
