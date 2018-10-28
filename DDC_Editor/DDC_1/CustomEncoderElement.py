#----------------------------------------------------------------------------------------
# In this file, you can define a list of parameters that should use a particular LED ring mode.
# Instructions on how to do this can be found about halfway through this file.
#
# --> Do not change the spacing or punctuation in this file.
# --> Do not change the name of this file.
#----------------------------------------------------------------------------------------

import Live

from _Framework.ButtonElement import ButtonElement

from _DDC.RingedEncoderElement import *

WALK_VALUE = 64
FILL_VALUE = 65
EQ_VALUE = 66
SPREAD_VALUE = 67

SKIP_MODES = (MAP_NONE, MAP_MANUAL)

PARAM_DICT = {}


def add(device_name, param_name, num_steps):
    assert isinstance(num_steps, int) and num_steps in xrange(64, 68)
    if device_name not in PARAM_DICT:
        PARAM_DICT[device_name] = {}
    PARAM_DICT[device_name][param_name] = num_steps


""" For each parameter that you'd like to define a custom LED ring mode for, you will use
the following example line as a template.  The values within the parentheses are as
follows:

- DeviceClassName - The devices class name.  For non-native devices, you can find this by
                    looking in the .ddc_dev file you created for the device.  This file
                    is located within your user directory in:
                    nativeKONTROL/DDC_Editor/Devices.

                    For native Live devices, you can find the class name in the
                    Live Device Info.html file in the Miscellaneous folder on the
                    repository. It's the name listed in parentheses (such as
                    LoungeLizard), which is the class name for Electric.

- ParameterName -   The name of the parameter.  You can find this in the same place as
                    you'll find the DeviceClassName.

- RingMode (WALK_VALUE) -   This value determines the LED ring mode to use. The possible
                            ring modes are:
                            WALK_VALUE
                            FILL_VALUE
                            EQ_VALUE
                            SPREAD_VALUE
"""

# Copy and paste this line and just change the three settings within the parentheses.
# DO NOT remove/change any of the punctuation.  You can define as many parameters as you like.
add('Instrument Rack', 'Macro 1', WALK_VALUE)
add('Instrument Rack', 'Macro 2', WALK_VALUE)
add('Instrument Rack', 'Macro 3', WALK_VALUE)
add('Instrument Rack', 'Macro 4', WALK_VALUE)
add('Instrument Rack', 'Chain Selector', WALK_VALUE)


class CustomEncoderElement(RingedEncoderElement):
    """ CustomEncoderElement for use with LI Code that handles updating LED ring types
    depending on the type of parameter being controlled. """

    def __init__(self, msg_type, channel, identifier, map_mode, name='', *a, **k):
        self._ring_mode_button = ButtonElement(False, 1, 15, identifier + 32, name=name +
                                               ' Ring_Mode_Button')
        super(CustomEncoderElement, self).__init__(msg_type, channel, identifier,
                                                   map_mode, name=name, *a, **k)

    def disconnect(self):
        self._ring_mode_button = None
        super(CustomEncoderElement, self).disconnect()

    def set_ring_mode(self, mode):
        if mode in SKIP_MODES:
            self._ring_mode_button.send_value(FILL_VALUE, True)
        else:
            self._ring_mode_button.send_value(self._get_ring_value(mode), True)

    def _get_ring_value(self, mode):
        param = self.mapped_parameter()
        parent = ('MixerDevice' if type(param.canonical_parent) ==
                  Live.MixerDevice.MixerDevice else param.canonical_parent.class_name)
        if parent in PARAM_DICT and param.original_name in PARAM_DICT[parent]:
            return PARAM_DICT[parent][param.original_name]
        if mode == MAP_BIPOLAR:
            return EQ_VALUE
        elif mode == MAP_QUANTIZED:
            return WALK_VALUE
        return FILL_VALUE
