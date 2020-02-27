# Cura plug-in to read MIDI files and produce toolpaths for the stepper motors to create that music.
# Copyright (C) 2020 Ghostkeeper
# This plug-in is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This plug-in is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for details.
# You should have received a copy of the GNU Affero General Public License along with this plug-in. If not, see <https://gnu.org/licenses/>.

import mido  # To parse the MIDI files.

class MidiReader:
	@classmethod
	def read_midi(cls, file_name):
		midi = mido.MidiFile(file_name)
		track = midi.tracks[0]

		current_time = 0
		for msg in track:
			current_time += msg.time
			msg.time = current_time
			if msg.type == "note_on" and msg.velocity == 0:
				msg.type = "note_off"

		# Schedule the notes in each of the channels.
		channels = [[]] * 4
		current_notes = {}
		for msg in track:
			if msg.type == "note_on":
				for channel in channels:
					pass  # TODO