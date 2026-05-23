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

import bpy# type: ignore
import os
import imbuf# type: ignore
from .lib import global_constructor as Pbpl
from .lib import level_constructor as Level
from bpy_extras.io_utils import ImportHelper # pyright: ignore[reportMissingModuleSource]
from bpy.props import StringProperty # pyright: ignore[reportMissingModuleSource]
from bpy.types import Operator # pyright: ignore[reportMissingModuleSource]

def imbuf_to_bpy_image(imbuf_img, image_name="ConvertedImage"):
    # 1. Define a temporary path to hold the file
    temp_path = os.path.join(bpy.app.tempdir, "temp_transfer.png")
    # 2. Use Blender's imbuf module to write out the data to disk
    imbuf.write(imbuf_img, filepath=temp_path)
    
    # 3. Load the image into bpy.data.images
    bpy_img = bpy.data.images.load(temp_path, check_existing=False)
    bpy_img.name = image_name
    
    # 4. Pack the image so it lives in memory inside the .blend file
    bpy_img.pack()
    
    # Clean up the temporary file from your disk
    os.remove(temp_path)
    
    return bpy_img

class IMPORT_OT_bbpl_format(Operator, ImportHelper):
    """Load a BB+ Level format (.pbpl)"""
    bl_idname = "import_scene.pbpl"
    bl_label = "Import BB+ Level (.pbpl)"
    bl_options = {'PRESET', 'UNDO'}
    filter_glob: StringProperty(
        default="*.pbpl;",
        options={'HIDDEN'},
    ) # type: ignore
    #i guess fake-bpy module doesnt recognise String Property yet
    def execute(self, context):
        # Call the parser function
        load_custom_file(self.filepath)
        return {'FINISHED'}

#Location Rotation pairs
pi : float = 3.14159265
wallrotations=[
    (0,0.5,0),(0,-pi/2,pi/2),
    (0.5,0,0),(0,-pi/2,0),
    (0,-0.5,0),(0,-pi/2,-pi/2),
    (-0.5,0,0),(0,-pi/2,pi),
]
def loadCells(level : Level.Level):
    cells=level.cells
    for i in range(level.width*level.height):
        x=i//level.width
        y=i%level.height
        print(level.cells[i].walls)
        loadCell(level.cells[i],[x,y,0])
        
def loadCell(cell,pos):
    for i in range(4):
        if (cell.walls)&(1<<i):
            print("the wall nybble: ",cell.walls," binary contains the ",2*i+2,"'s digit!")
            bpy.ops.mesh.primitive_plane_add(size=1, align='WORLD', location=[wallrotations[i*2][0]+pos[0],wallrotations[i*2][1]+pos[1],wallrotations[i*2][2]+pos[2]], rotation=wallrotations[i*2+1])
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
def load_custom_file(filepath):
    with open(filepath,"rb") as f:
        map=Pbpl.LevelStudioMap(f)
        freequeue=[] #array so we can free the data when we're done also i dont know the datatype for File object things so ill have to update this later
        pack_entries=map.metadata.package.entries
        for entry in pack_entries:
            if type(entry.data)=='string': #if the data is in a filepath
                #i have no clue where this data is stored btw, i guess ill just figure it out later
                file=open(filepath+entry.data,"rb")
                freequeue.append(file)
                entry.data=file
        loadCells(map.level)
        for entry in freequeue:
            entry.close()


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