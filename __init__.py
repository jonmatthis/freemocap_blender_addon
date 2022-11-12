'''
Copyright (C) cgtinker, cgtinker.com, hello@cgtinker.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


bl_info = {
    "name":        "freemocap_blender_addon",
    "description": "Blender addon to bind `freemocap` data to `rigify` human meta rig - based on fork off `cgtinker/BlendArMocap` ",
    "author":      "jonmatthis",
    "version":     (0, 0, 1),
    "blender":     (2, 90, 0),
    "location":    "3D View > Tool",    
    "wiki_url":    "https://github.com/jonmatthis/freemocap_blender_addon",
    "tracker_url": "https://github.com/jonmatthis/freemocap_blender_addon/issues",
    "support":     "COMMUNITY",
    "category":    "Animation"
}


def reload_modules():
    from .src import cgt_imports
    cgt_imports.manage_imports()


if "bl_info" in locals():
    reload_modules()

from .src.cgt_blender.interface import ui_registration


def register():
    from .src.cgt_blender.utils import dependencies
    # ugly fix to delete packages to remove on restart
    dependencies.force_remove_remains()
    ui_registration.register()


def unregister():
    ui_registration.unregister()


if __name__ == '__main__':
    register()
