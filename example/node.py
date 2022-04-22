

from twisted.internet import reactor
from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui
from ebs.linuxnode.gui.kivy.netconfig.mixin import NetconfigGuiMixin


class ExampleNode(NetconfigGuiMixin, BaseIoTNodeGui):
    def start(self):
        super(ExampleNode, self).start()
