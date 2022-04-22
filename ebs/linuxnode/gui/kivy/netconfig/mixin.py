

import os

from kivy_garden.ebs.cefkivy.browser import CefBrowser
from kivy_garden.ebs.core.buttons import BleedImageButton

from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui


class NetconfigGuiMixin(BaseIoTNodeGui):
    def __init__(self, *args, **kwargs):
        super(NetconfigGuiMixin, self).__init__(*args, **kwargs)
        self._netconfig_enabled = False
        self._netconfig_button = None

    def install(self):
        super(NetconfigGuiMixin, self).install()
        _elements = {
            'netconfig_enable': ElementSpec('netconfig', 'enable', ItemSpec(str, read_only=False, fallback='no_internet')),
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

    @property
    def netconfig_button(self):
        if not self._netconfig_button:
            _root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
            _source = os.path.join(_root, 'images', 'settings.png')
            self._netconfig_button = BleedImageButton(
                source=_source, pos_hint={'left': 1},
                size_hint=(None, None), height=50, width=50,
                bgcolor=(0xff / 255., 0x00 / 255., 0x00 / 255., 0.3),
            )
        return self._netconfig_button

    def _netconfig_button_show(self):
        if not self.netconfig_button.parent:
            self.gui_notification_row.add_widget(self.netconfig_button)
            self.gui_notification_update()

    def _netconfig_button_hide(self):
        if self.netconfig_button.parent:
            self.netconfig_button.parent.remove_widget(self.netconfig_button)
            self.gui_notification_update()

    @property
    def netconfig_enabled(self):
        return self._netconfig_enabled

    @netconfig_enabled.setter
    def netconfig_enabled(self, value):
        if not value:
            self._netconfig_button_show()
        else:
            self._netconfig_button_hide()
        self._netconfig_enabled = value

    def modapi_signal_internet_connected(self, value, prefix):
        super(NetconfigGuiMixin, self).modapi_signal_internet_connected(value, prefix)
        if self.config.netconfig_enable == 'no_internet':
            if not value:
                self.netconfig_enabled = True
            else:
                self.netconfig_enabled = False

    def gui_setup(self):
        gui = super(NetconfigGuiMixin, self).gui_setup()
        if self.config.netconfig_enable == 'always':
            self.netconfig_enabled = True
        return gui
