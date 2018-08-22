# Minitiles: auto-autotiling for Godot! (and others)

The autotiling in Godot is great, but it requires a *lot* of copy and pasting in your sprite sheet to create a full tileset, as you need 47 tiles to make a fully functional set. Now you can make Gimp do all the hard work for you, using only 5 tiles!

From this:  
![minitiles](https://github.com/lunarfyre7/GodotAutotileAssembler/raw/master/demo/minitiles.png)  
To this:  
![autotile](https://github.com/lunarfyre7/GodotAutotileAssembler/raw/master/demo/autotiles.png)

## Installation

* Copy `autotileassembler.py` to your gimp plug-ins directory.
* Copy `autotiles_template.tres` and `minitiles-template.png` to your project.

## Usage
#### Godot

Before you do anything you need to setup your art, the minitiles template is actually 20 tiles, but it's essentially the same amount of effort as making 5 tiles variants as long as you keep in mind that the tiles need to be cut into quarters easily. The structure of the minitile sprite is corners/single, vertical, horizontal, inner-corners, and seamless-fill. You can typically create the seamless fill tile and modify it for the other variants.

In Gimp load the finished minitile set and run the assembler script `Filters/Tileset/AutotileAssembler` and save the result. Next add the new sprite to your tileset scene, export it, and enable autotiling in the resource. Now open the template tileset in the inspector and in the autotile tab and copy the bitmask, then paste it into your own tileset resource. Also you need to set the tile size in the autotile panel, the spacing to 0, and the bitmask mode to 3x3.

#### Other Engines

You can also just use the Gimp script to create tilesets for other engines as well, just follow the above steps for processing the sprite in Gimp and ignore the godot steps.

#### Other Implementations and Alternatives
[autotile generator (cli version)](https://github.com/HeartoLazor/autotile_generator)

### license
CC-0
