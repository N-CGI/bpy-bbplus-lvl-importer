# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Baldis Basics+ Level Studio Map Importer",
    "author": "N_CGI",
    "description": "a simple blender importer designed to help make baldi basics maps easy to make",
    "blender": (5, 1, 1),
    "version": (0, 0, 1),
    "category": "Import-Export",
}

import bpy
from .lib import global_constructor as Pbpl
from bpy_extras.io_utils import ImportHelper # pyright: ignore[reportMissingModuleSource]
from bpy.props import StringProperty # pyright: ignore[reportMissingModuleSource]
from bpy.types import Operator # pyright: ignore[reportMissingModuleSource]

class IMPORT_OT_bbpl_format(Operator, ImportHelper):
    """Load a BB+ Level format (.pbpl)"""
    bl_idname = "import_scene.pbpl"
    bl_label = "Import BB+ Level (.pbpl)"
    bl_options = {'PRESET', 'UNDO'}

    def execute(self, context):
        # Call the parser function
        load_custom_file(self.filepath)
        return {'FINISHED'}

def load_custom_file(filepath):
    with open(filepath,"rb") as f:
        map=Pbpl.LevelStudioMap(f)
        
        
        

def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_bbpl_format.bl_idname, text="BB+ Level (.pbpl)")

def register():
    bpy.utils.register_class(IMPORT_OT_bbpl_format)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(IMPORT_OT_bbpl_format)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    print("Initializing BB+ Importer")
    register()