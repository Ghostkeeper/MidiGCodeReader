# Cura plug-in to read MIDI files and produce toolpaths for the stepper motors to create that music.
# Copyright (C) 2020 Ghostkeeper
# This plug-in is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This plug-in is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this plug-in. If not, see <https://gnu.org/licenses/>.

from . import MidiToolpathReader

def getMetaData():
	return {
		"mesh_reader": [
			{
				"extension": "mid",
				"description": "MIDI music file as toolpath"
			}
		]
	}

def register(application):
	application.addNonSliceableExtension(".mid")
	application.addNonSliceableExtension(".midi")
	return {"mesh_reader": MidiToolpathReader.MidiToolpathReader()}