from .button import Button
from .relay import Relay


class UVLamp:

    def __init__(self, input_pin, output_pin):
        """

        :param input_pin: Button Pin
        :param output_pin: Relay Pin
        """
        self._button = Button(input_pin, self.toggle)
        self._relay = Relay(output_pin)

    def status(self):
        return self._relay.status()

    def switch_on(self):
        self._relay.switch_on()
        return self.status()

    def switch_off(self):
        self._relay.switch_off()
        return self.status()

    def toggle(self):
        self._relay.toggle()
        return self.status()


