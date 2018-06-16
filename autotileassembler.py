#!/usr/bin/env python
from gimpfu import *

#enum
BLANK = 0
CENTER = 1
VERT = 2
HORIZ = 3
INSIDE = 4
FILL = 5

class Autoload():
    def __init__(self, image, layer, x, y):
        self.image = image 
        self.layer = layer
        self.original_width, self.original_height = pdb.gimp_image_width(image), pdb.gimp_image_height(image)
        self.tile_size = self.original_height
        self.sub_size = self.tile_size/2 #minitile size
        self.x_tiles, self.y_tiles = x, y
        self.width, self.height = self.tile_size*self.x_tiles, self.tile_size*self.y_tiles
        self.write_layer = gimp.Layer(image, "3x3 sprite", self.width, self.height, RGBA_IMAGE, 100, NORMAL_MODE)

    def run(self, map):

        # Set up an undo group, so the operation will be undone in one step.
        pdb.gimp_image_undo_group_start(self.image)
        self.image.add_layer(self.write_layer, 0)

        pdb.gimp_image_resize(self.image, self.width, self.height, 0, 0)
        #create new layer for writing
                # write_layer.flush()
        for y, row in enumerate(map):
            for x, cell in enumerate(row):
                args = cell + (x, y)
                self.copy_minitile(*args)
        

        # Close the undo group.
        pdb.gimp_drawable_set_visible(self.layer, False)
        pdb.gimp_image_undo_group_end(self.image)

    def copy_minitile(self, nw, ne, sw, se, tox, toy):
        tiles = [nw, ne, sw, se]
        for id in range(4):
            # pdb.gimp_image_set_active_layer(image, layer)
            if tiles[id] == 0: continue #skip blanks
            x_offset = self.sub_size if id in [1, 3] else 0
            y_offset = self.sub_size if id > 1 else 0
            x = self.tile_size*(tiles[id]-1) + x_offset
            y = y_offset
            #copy tile
            pdb.gimp_image_select_rectangle(self.image, CHANNEL_OP_REPLACE, x, y, self.sub_size, self.sub_size)
            pdb.gimp_edit_copy(self.layer)
            #paste tile
            pdb.gimp_image_select_rectangle(self.image, CHANNEL_OP_REPLACE, tox*self.tile_size+x_offset, toy*self.tile_size+y_offset,self.sub_size, self.sub_size)
            floating_sel = pdb.gimp_edit_paste(self.write_layer, True)
            pdb.gimp_floating_sel_to_layer(floating_sel)
            # num_layers, layer_ids = pdb.gimp_image_get_layers(self.image)
            self.write_layer = pdb.gimp_image_merge_down(self.image, floating_sel, CLIP_TO_IMAGE)
            # assert(merged_layer == write_layer)
            # pdb.gimp_floating_sel_attach(write_layer, floating_sel)

# BLANK = 0
# CENTER = 1
# VERT = 2
# HORIZ = 3
# INSIDE = 4
# FILL = 5
three_by_three_map = [
    [(1,1,2,2),(1,3,2,4),(3,3,4,4),(3,1,4,2),(5,4,4,4),(3,3,4,5),(3,3,5,4),(4,5,4,4),(1,3,2,5),(4,4,5,5),(3,3,5,5),(3,1,5,2)],
    [(2,2,2,2),(2,4,2,4),(4,4,4,4),(4,2,4,2),(2,4,2,5),(4,5,5,5),(5,4,5,5),(4,2,5,2),(2,5,2,5),(4,5,5,4),(0,0,0,0),(5,4,5,4)],
    [(2,2,1,1),(2,4,1,3),(4,4,3,3),(4,2,3,1),(2,5,2,4),(5,5,4,5),(5,5,5,4),(5,2,4,2),(4,5,4,5),(5,5,5,5),(5,4,4,5),(5,2,5,2)],
    [(1,1,1,1),(1,3,1,3),(3,3,3,3),(3,1,3,1),(4,4,5,4),(4,5,3,3),(5,4,3,3),(4,4,4,5),(2,5,1,3),(5,5,3,3),(5,5,4,4),(5,2,3,1)],
]
def plugin(image, layer):
    al = Autoload(image, layer, 12, 4)
    al.run(three_by_three_map)

register(
    "python_fu_autotile_assembler", 
    "Assemble 3x3 bitmask tileset for Godot using a 5 tile minitileset.", 
    "Run on a sprite using the template format (center/corners, vert, horiz, inside corners, solid fill).", 
    "JGV", 
    "MIT", 
    "2018", 
    "<Image>/Filters/Tileset/AutotileAssembler", 
    "*", 
    [], 
    [], 
    plugin
)

main()
