import _Framework.Task
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

SELECTED_CHAR = 127
UP_ARROW_CHAR = 0
DOWN_ARROW_CHAR = 1
HORZ_STACK_CHAR = 2
FULL_BLOCK_CHAR = 29
RIGHT_ARROW_CHAR = 30
LEFT_ARROW_CHAR = 31
SPECIAL_CHARS = (SELECTED_CHAR, UP_ARROW_CHAR, DOWN_ARROW_CHAR, HORZ_STACK_CHAR,
                 RIGHT_ARROW_CHAR, LEFT_ARROW_CHAR, FULL_BLOCK_CHAR)
CHARS_TO_REMOVE = (' ', 'I', 'i', 'O', 'o', 'U', 'u', 'E', 'e', 'A', 'a')
HALF_SEGMENT = 9
FULL_SEGMENT = 18
FULL_SEGMENT_OFFSETS = (0, 17, 34, 51)
HALF_SEGMENT_OFFSETS = (0, 9, 18, 27, 36, 45, 54, 63)
BLANK_LINE = [32 for i in range(72)]


class SLDisplayLine(ControlSurfaceComponent):
    """ SLDisplayLine handles one of the SL's 4 display lines. """

    def __init__(self, line_index):
        assert line_index in (1, 2, 3, 4)
        super(SLDisplayLine, self).__init__(name='Display_Line_%d' % line_index)
        self._header = [240, 0, 32, 41, 3, 3, 18, 0, 4, 0, 2, 1, 0, line_index, 4]
        self._current_line = list(BLANK_LINE)
        self._momentary_line = []
        self._last_sent_message = None
        self._send_message_task = self._tasks.add(_Framework.Task.run(self._send_message))
        self._send_message_task.kill()

    def write(self, offset, length, string_to_write, center=False, spc_start_char=-1,
              spc_end_char=-1):
        """ Writes the given string at the given offset and crops to the given length.
            Can also center string if specified and can also write a special char at the
            start or end of the string if specified. """
        self._current_line = self._do_write(self._current_line, offset, length,
                                            string_to_write, False, center,
                                            spc_start_char, spc_end_char)
        self._request_send_message()

    def write_momentary(self, offset, length, string_to_write, clear=False, center=False):
        """ Momentarily writes the given string at the given offset and crops to the
        given length.  Call revert to reset back to default. Can also clear rest of line
        and center string if specified. """
        self._momentary_line = self._do_write(self._momentary_line, offset, length,
                                              string_to_write, clear, center, -1, -1)
        self._request_send_message()

    def _do_write(self, var, offset, length, string_to_write, clear, center,
                  spc_start_char, spc_end_char):
        """ Performs the actual write and returns modified variable to caller. """
        assert offset in HALF_SEGMENT_OFFSETS
        assert length in range(FULL_SEGMENT + 1)
        assert spc_start_char == -1 or spc_start_char in SPECIAL_CHARS
        assert spc_end_char == -1 or spc_end_char in SPECIAL_CHARS
        if spc_start_char != -1:
            new_chars = [spc_start_char] + self._get_chars(string_to_write, length - 1,
                                                           center)
        else:
            new_chars = self._get_chars(string_to_write, length, center)
        if spc_end_char != -1:
            insert_index = -1
            for index in range(length - 1, -1, -1):
                if new_chars[index] == 32:
                    insert_index = index
                    break
            new_chars[insert_index] = spc_end_char
        if clear:
            if self._momentary_line:
                var = list(self._momentary_line)
            else:
                var = list(BLANK_LINE)
        elif var != self._current_line:
            var = list(self._current_line)
        for index in range(length):
            var[offset + index] = new_chars[index]
        return var

    def clear(self):
        """ Clears the display line. """
        self._momentary_line = []
        self._current_line = list(BLANK_LINE)
        self._last_sent_message = None
        self._request_send_message()

    def revert(self):
        """ Reverts momentary display back to default. """
        self._momentary_line = []
        self._request_send_message()

    def update(self):
        if self.is_enabled():
            self._last_sent_message = None
            self._request_send_message()

    def _request_send_message(self):
        """ Requests that a message be sent and schedules it via Task. """
        self._send_message_task.restart()

    def _send_message(self):
        """ Determines which message should be sent. """
        if self.is_enabled():
            if self._momentary_line:
                self.send_midi(tuple(self._header + self._momentary_line + [247]))
            else:
                self.send_midi(tuple(self._header + self._current_line + [247]))

    def send_midi(self, midi_bytes):
        """ Sends the given bytes out if they aren't equal to the last sent bytes. """
        if midi_bytes != self._last_sent_message:
            self.canonical_parent._send_midi(midi_bytes)
            self._last_sent_message = midi_bytes

    def _get_chars(self, string, num_chars, should_center):
        """ Returns a list of MIDI values derived from the string. Crops if necessary and
        centers if specified. """
        assert isinstance(string, (str, unicode)) and isinstance(num_chars, int)
        # used to prevent issues with reading really long clip names like ClyphX Snaps
        if len(string) > 75:
            string = string[0:num_chars]
        if len(string) > num_chars:
            for um in CHARS_TO_REMOVE:
                while ((len(string) > num_chars) and (string.rfind(um, 1) != -1)):
                    um_pos = string.rfind(um, 1)
                    string = (string[:um_pos] + string[(um_pos + 1):])
            if len(string) > num_chars:
                string = string[0:num_chars]
        else:
            if should_center:
                string = string.center(num_chars)
            else:
                string = string.ljust(num_chars)
        converted_string = []
        for c in string:
            new_char = ord(c)
            if new_char > 127:
                new_char = 63
            converted_string.append(new_char)
        return converted_string