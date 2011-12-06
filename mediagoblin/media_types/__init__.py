# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2011 MediaGoblin contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from mediagoblin import mg_globals
from mediagoblin.tools.translate import lazy_pass_to_ugettext as _


class FileTypeNotSupported(Exception):
    pass

class InvalidFileType(Exception):
    pass


def get_media_types():
    """
    Generator that returns the available media types
    """
    for media_type in mg_globals.app_config['media_types']:
        yield media_type


def get_media_managers():
    '''
    Generator that returns all available media managers
    '''
    for media_type in get_media_types():
        __import__(media_type)
            
        yield media_type, sys.modules[media_type].MEDIA_MANAGER


def get_media_manager(_media_type = None):
    for media_type, manager in get_media_managers():
        if media_type in _media_type:
            return manager

    # Nope?  Then raise an error
    raise FileTypeNotSupported(
        "MediaManager not in enabled types.  Check media_types in config?")


def get_media_type_and_manager(filename):
    for media_type, manager in get_media_managers():
        if filename.find('.') > 0:
            ext = os.path.splitext(filename)[1].lower()
        else:
            raise InvalidFileType(
                _('Could not find any file extension in "{filename}"').format(
                    filename=filename))

        if ext[1:] in manager['accepted_extensions']:
            return media_type, manager
