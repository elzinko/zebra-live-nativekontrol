from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import subject_slot, subject_slot_group

from SLDisplayLine import SLDisplayLine, HALF_SEGMENT, HALF_SEGMENT_OFFSETS

NUM_PARAMS_TO_MONITOR = 16

""" Parameter names that need to be translated for displaying purposes. """
TRANSLATED_PARAM_NAMES = {
    'Track Volume': 'Volume',
    'Track Panning': 'Pan',
}


class DisplayAdapter(ControlSurfaceComponent):

    def __init__(self, device_component, *a, **k):
        super(DisplayAdapter, self).__init__(name='Display_Adapter', *a, **k)
        self._display_lines = [SLDisplayLine(i + 1) for i in xrange(4)]
        self._device_component = device_component
        self._parameters_to_monitor = None
        self._on_encoder_parameters_changed.subject = self._device_component

    def on_script_close(self):
        for line in self._display_lines:
            line.clear()

    @subject_slot('encoder_parameters')
    def _on_encoder_parameters_changed(self):
        self._parameters_to_monitor = []
        for index in xrange(NUM_PARAMS_TO_MONITOR):
            param = self._device_component.encoder_parameters[index]
            self._parameters_to_monitor.append(param)
            self._on_encoder_parameter_name_changed(param, index)
            self._on_encoder_parameter_value_changed(param, index)
        self._on_encoder_parameter_value_changed.\
            replace_subjects(self._parameters_to_monitor)

    def _on_encoder_parameter_name_changed(self, parameter, index):
        param_name = (TRANSLATED_PARAM_NAMES.get(parameter.name, parameter.name)
                      if parameter is not None else '-')
        self._display_lines[0 if index < 8 else 1].write(HALF_SEGMENT_OFFSETS[index % 8],
                                                         HALF_SEGMENT, param_name, True)

    @subject_slot_group('value')
    def _on_encoder_parameter_value_changed(self, parameter, index=None):
        param_index = (index if index is not None else
                       self._parameters_to_monitor.index(parameter))
        param_value = unicode(parameter) if parameter is not None else '-'
        self._display_lines[2 if param_index < 8 else 3].\
            write(HALF_SEGMENT_OFFSETS[param_index % 8], HALF_SEGMENT, param_value, True)
