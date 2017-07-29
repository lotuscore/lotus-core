import gi
import signal

from windows import WalletWindow
from indicator import LotusIndicator

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3 as appindicator  # noqa


class LotusApp(Gtk.Application):
    def __init__(self):
        super(LotusApp, self).__init__()
        self.name = 'Lotus'
        self.wallet_window = WalletWindow(self)
        self.indicator = LotusIndicator(self)

    def run(self):
        Gtk.main()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = LotusApp()
    app.run()