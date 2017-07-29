import gi
import os
import webbrowser

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3 as appindicator  # noqa

APPINDICATOR_ID = 'lotus-core'


class LotusIndicator:
    def __init__(self, root):
        self.app = root
        self.indicator = appindicator.Indicator.new(
            APPINDICATOR_ID,
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'lotus.svg'),
            appindicator.IndicatorCategory.SYSTEM_SERVICES
        )
        menu = self.build_menu()

        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(menu)

    def build_menu(self):
        menu = Gtk.Menu()

        item_store = Gtk.MenuItem('Store')
        item_store.connect('activate', self.open_store)

        item_wallet = Gtk.MenuItem('Wallet')
        item_wallet.connect("activate", self.app.wallet_window.cb_show, '')

        item_library = Gtk.MenuItem('Library')
        item_settings = Gtk.MenuItem('Settings')

        item_exit = Gtk.MenuItem('Exit')
        item_exit.connect('activate', quit)

        menu.append(item_store)
        menu.append(item_wallet)
        menu.append(item_library)
        menu.append(item_settings)
        menu.append(item_exit)
        menu.show_all()
        return menu

    def open_store(self, source):
        webbrowser.open('https://lotuscore.io/store')

    def quit(self, source):
        Gtk.main_quit()
