import gi
import os

from populus import Project

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


class WalletWindow(Gtk.Window):

    def __init__(self, root):
        super(WalletWindow, self).__init__()
        self.app = root
        self.set_title('{} - Wallet'.format(self.app.name))

    def on_button_clicked(self, widget):
        os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '..', 'core'))

        project = Project()
        with project.get_chain('external') as chain:
            contract, _ = chain.provider.get_or_deploy_contract('Greeter')
            print(contract.call().greet())

    def cb_show(self, w, data):
        self.button = Gtk.Button(label="Transaction")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)
        self.show_all()
