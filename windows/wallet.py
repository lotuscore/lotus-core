import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


class WalletWindow(Gtk.Window):

    def __init__(self, root):
        super(WalletWindow, self).__init__()
        self.app = root
        self.set_title('{} - Wallet'.format(self.app.name))

    def on_button_clicked(self, widget):
        print("Hello")

    def cb_show(self, w, data):
        self.button = Gtk.Button(label="Transaction")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)
        self.show_all()
