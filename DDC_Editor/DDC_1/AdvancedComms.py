#----------------------------------------------------------------------------------------
# This file allows you to handle advanced communication with a controller.
#
# PLEASE NOTE:
# This is strictly intended for use by users who understand Python.  Incorrect formatting
# or code written in this file could cause the script to stop working.
#----------------------------------------------------------------------------------------

from _Framework.ControlSurfaceComponent import ControlSurfaceComponent


class AdvancedComms(ControlSurfaceComponent):
    """ AdvancedComms allows you to send/receive SysEx and other forms of MIDI messages
    to a controller. """

    def __init__(self, *a, **k):
        super(AdvancedComms, self).__init__(name='Advanced_Controller_Comms', *a, **k)

    def on_init(self):
        """ This method is called upon the script loading (as well as a new set being
        loaded) and would typically be used to send some sort of initialization message
        to the controller.  The example below shows how that can be done. _send_midi can
        send a tuple containing any valid MIDI messages. """
        self.canonical_parent._send_midi((240, 0, 32, 41, 3, 3, 18, 0, 4, 0, 1, 1, 247))

    def on_disconnect(self):
        """ This method is called upon the script disconnecting and would typically be
        used to send some sort of reset or goodbye message to the controller.  The
        example below shows how that can be done. _send_midi can send a tuple containing
        any valid MIDI messages. """
        self.canonical_parent._send_midi((240, 0, 32, 41, 3, 3, 18, 0, 4, 0, 1, 0, 247))

    def on_sysex_received(self, received_bytes):
        """ This method is called any time SysEx is received from the controller.
        received_bytes is a tuple containing the SyxEx message that was received. """
        pass
