# Cura plug-in to read MIDI files and produce toolpaths for the stepper motors to create that music.
# Copyright (C) 2020 Ghostkeeper
# This plug-in is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This plug-in is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this plug-in. If not, see <https://gnu.org/licenses/>.

import cura.CuraApplication  # To access the build plate.
import cura.Scene.GCodeListDecorator  # To store the output g-code.
import cura.Scene.CuraSceneNode  # To create a mesh node in the scene as result of our read.
import UM.Backend.Backend  # To disable slicing while the toolpath is loaded.
import UM.Mesh.MeshReader  # The class we're extending.
from . import MidiReader  # To read the symbols from the MIDI files.
from . import Muxer  # To interweave the tracks from the MIDI file.
from . import SpeedVectors  # To convert the notes to speed vectors.
from . import PathGenerator  # Plan the paths within the build volume.

class MidiToolpathReader(UM.Mesh.MeshReader):
	def _read(self, file_name) -> cura.Scene.CuraSceneNode.CuraSceneNode:
		tracks = MidiReader.MidiReader.read_midi(file_name)  # First read the MIDI notes from the file.
		tones = Muxer.Muxer.mux(tracks)  # Interweave these MIDI notes into one single track with multi-dimensional notes.
		speed_vectors = SpeedVectors.SpeedVectors.convert(tones)  # Convert each tone to a 5D movement.
		toolpath = PathGenerator.PathGenerator.plan(speed_vectors)  # Convert each movement vector (with speed) to actual g-code, fitting it within the build volume.

		# Put that toolpath in a scene node.
		gcode_list_decorator = cura.Scene.GCodeListDecorator.GCodeListDecorator()
		gcode_list = [toolpath]
		gcode_list_decorator.setGCodeList(gcode_list)
		scene_node = cura.Scene.CuraSceneNode.CuraSceneNode()
		scene_node.addDecorator(gcode_list_decorator)
		active_build_plate_id = cura.CuraApplication.CuraApplication.getInstance().getMultiBuildPlateModel().activeBuildPlate
		gcode_dict = {active_build_plate_id: gcode_list}
		cura.CuraApplication.CuraApplication.getInstance().getController().getScene().gcode_dict = gcode_dict

		cura.CuraApplication.CuraApplication.getInstance().getBackend().backendStateChange.emit(UM.Backend.Backend.BackendState.Disabled)  # Don't try slicing this node.

		return scene_node