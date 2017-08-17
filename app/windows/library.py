import gi

from db import DB
from utils import get_chain, get_settings

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa

db = DB()


class LibraryWindow(Gtk.Window):

    def __init__(self, root):
        super(LibraryWindow, self).__init__()
        self.set_border_width(10)

        self.app = root
        self.set_title('{} - Library'.format(self.app.name))
        self.load_library()
        self.create_ui()

    def load_library(self):
        with get_chain() as chain:
            Library = chain.provider.get_contract_factory('Library')
            settings = get_settings()
            library_address = settings.library_address
            self.library = Library(address=library_address)

    def create_ui(self):
        # Add header bar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = self.get_title()
        self.set_titlebar(hb)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        hb.pack_start(box)

        # Create Grid
        self.grid = Gtk.Grid()
        self.add(self.grid)

        library = self.library.call().list()
        for index, cartridge in enumerate(library):
            print(cartridge)
            label = Gtk.Label(cartridge)
            self.grid.attach(label, 0, index, 4, 1)

    def cb_show(self, w, data):
        self.show_all()
