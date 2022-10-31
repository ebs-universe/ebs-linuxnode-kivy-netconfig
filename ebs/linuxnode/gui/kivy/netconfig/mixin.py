

import os

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout

from kivy_garden.ebs.core.colors import ColorBoxLayout
from kivy_garden.ebs.core.buttons import BleedImageButton
from kivy_garden.ebs.cefkivy.browser import CefBrowser

from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui


class CapturingRelativeLayout(RelativeLayout):
    def on_touch_down(self, touch):
        super(CapturingRelativeLayout, self).on_touch_down(touch)
        return True


class NetconfigGuiMixin(BaseIoTNodeGui):
    def __init__(self, *args, **kwargs):
        super(NetconfigGuiMixin, self).__init__(*args, **kwargs)
        self._netconfig_enabled = False
        self._netconfig_button = None
        self._netconfig_close_button = None
        self._gui_netconfig_containter = None
        self._gui_netconfig = None
        self._gui_netconfig_layout = None
        self._gui_netconfig_navbar = None
        self._gui_netconfig_browser = None

    def install(self):
        super(NetconfigGuiMixin, self).install()
        _elements = {
            'netconfig_enable': ElementSpec('netconfig', 'enable', ItemSpec(str, read_only=False, fallback='no_internet')),
            'netconfig_indicator_duration': ElementSpec('netconfig', 'indicator_duration', ItemSpec(int, fallback=0))
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

    @property
    def gui_netconfig_container(self):
        if not self._gui_netconfig_containter:
            self._gui_netconfig_layout = CapturingRelativeLayout()

            self._gui_netconfig = ColorBoxLayout(bgcolor=(1, 1, 1, 1), size_hint=(0.6, 0.6),
                                                 pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                                 orientation='vertical')

            self._gui_netconfig_navbar = StackLayout(orientation='rl-tb',
                                                     size_hint=(1, None), height=40)
            self._gui_netconfig_navbar.add_widget(self.netconfig_close_button)
            self._gui_netconfig.add_widget(self._gui_netconfig_navbar)

            self._gui_netconfig_browser = CefBrowser(start_url='http://localhost:8039',
                                                     keyboard_container=self._gui_netconfig_layout)
            self._gui_netconfig.add_widget(self._gui_netconfig_browser)

            self._gui_netconfig_layout.add_widget(self._gui_netconfig)

            self._gui_netconfig_containter = ColorBoxLayout(bgcolor=(0, 0, 0, 0.5))
            self._gui_netconfig_containter.add_widget(self._gui_netconfig_layout)
        return self._gui_netconfig_containter

    def _netconfig_click_handler(self, *_):
        if not self.gui_netconfig_container.parent:
            self.gui_primary_anchor.add_widget(self.gui_netconfig_container)

    def _netconfig_close_handler(self, *_):
        if self.gui_netconfig_container.parent:
            self.gui_primary_anchor.remove_widget(self.gui_netconfig_container)
            self._gui_netconfig_containter = None
            self._gui_netconfig_navbar = None
            self._netconfig_close_button = None
            self._gui_netconfig_layout = None
            self._gui_netconfig = None

    @property
    def netconfig_button(self):
        if not self._netconfig_button:
            _root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
            _source = os.path.join(_root, 'images', 'settings.png')
            self._netconfig_button = BleedImageButton(
                source=_source, pos_hint={'left': 1},
                size_hint=(None, None), height=50, width=50,
                bgcolor=(0 / 255., 0 / 255., 0 / 255., 0.3),
            )
            self._netconfig_button.bind(on_press=self._netconfig_click_handler)
        return self._netconfig_button

    @property
    def netconfig_close_button(self):
        if not self._netconfig_close_button:
            _root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
            _source = os.path.join(_root, 'images', 'close.png')
            self._netconfig_close_button = BleedImageButton(
                source=_source,
                size_hint=(None, 1), width=40,
                bgcolor=(0xff / 255., 0xff / 255., 0xff / 255., 1),
            )
            self._netconfig_close_button.bind(on_press=self._netconfig_close_handler)
        return self._netconfig_close_button

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
        if value:
            if self.config.netconfig_indicator_duration:
                self.reactor.callLater(self.config.netconfig_indicator_duration,
                                       self._netconfig_disable)
            self._netconfig_button_show()
        else:
            self._netconfig_button_hide()
        self._netconfig_enabled = value

    def _netconfig_disable(self):
        self.netconfig_enabled = False

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
