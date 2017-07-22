import gi
import os
import signal

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator  # noqa

APPINDICATOR_ID = 'lotus-core'


def main():
    indicator = appindicator.Indicator.new(
        APPINDICATOR_ID,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lotus.svg'),
        appindicator.IndicatorCategory.SYSTEM_SERVICES
    )
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()


def build_menu():
    menu = gtk.Menu()

    item_store = gtk.MenuItem('Store')
    item_wallet = gtk.MenuItem('Wallet')
    item_library = gtk.MenuItem('Library')
    item_settings = gtk.MenuItem('Settings')

    item_exit = gtk.MenuItem('Exit')
    item_exit.connect('activate', quit)

    menu.append(item_store)
    menu.append(item_wallet)
    menu.append(item_library)
    menu.append(item_settings)
    menu.append(item_exit)
    menu.show_all()
    return menu


def quit(source):
    gtk.main_quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
