import gi

from utils import check_succesful_tx, get_chain

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


class DevToolsWindow(Gtk.Window):

    def __init__(self, root):
        super(DevToolsWindow, self).__init__()
        self.set_border_width(10)

        self.app = root
        self.set_title('{} - Developer Tools'.format(self.app.name))

        self.create_ui()

    def deploy_cartridge(self, widget):
        with get_chain() as chain:
            # Load Populus contract proxy classes
            Cartridge = chain.provider.get_contract_factory('Cartridge')

            web3 = chain.web3
            print("Web3 provider is", web3.currentProvider)

            # The address who will be the owner of the contracts
            beneficiary = web3.eth.accounts[1]
            assert beneficiary

            # Deploy cartridge
            txhash = Cartridge.deploy(transaction={
                "from": beneficiary
            }, args=[
                self.name_entry.get_text(),
                self.genre_entry.get_text(),
                self.rating_entry.get_text(),
                int(self.platforms_entry.get_text()),
                int(self.price_entry.get_text())
            ])
            print("Deploying token, tx hash is", txhash)
            receipt = check_succesful_tx(web3, txhash)
            cartridge_address = receipt["contractAddress"]
            print("Cartridge contract address is", cartridge_address)

            # testing contract
            cartridge = Cartridge(address=cartridge_address)
            print("Cartridge name:", cartridge.call().get_name())

    def create_ui(self):
        # Add header bar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = self.get_title()
        self.set_titlebar(hb)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(button)

        hb.pack_start(box)

        # Create Grid
        self.grid = Gtk.Grid()
        self.add(self.grid)

        # Add title
        self.balance_label = Gtk.Label()
        self.grid.attach(self.balance_label, 0, 1, 4, 1)

        # Add input fields
        name_label = Gtk.Label("Name", xalign=0)
        genre_label = Gtk.Label("Genre", xalign=0)
        rating_label = Gtk.Label("Rating", xalign=0)
        platforms_label = Gtk.Label("Platforms", xalign=0)
        price_label = Gtk.Label("Price", xalign=0)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_text('Cartridge Name')

        self.genre_entry = Gtk.Entry()
        self.genre_entry.set_text('RPG')

        self.rating_entry = Gtk.Entry()
        self.rating_entry.set_text('E')

        self.platforms_entry = Gtk.Entry()
        self.platforms_entry.set_text('1')

        self.price_entry = Gtk.Entry()
        self.price_entry.set_text('100')

        # Layout construction, it is a 2x5 box
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)
        row = Gtk.ListBoxRow()
        container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(container)

        column1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.pack_start(column1, True, True, 0)

        column1.pack_start(name_label, True, True, 0)
        column1.pack_start(genre_label, True, True, 0)
        column1.pack_start(rating_label, True, True, 0)
        column1.pack_start(platforms_label, True, True, 0)
        column1.pack_start(price_label, True, True, 0)

        column2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.pack_start(column2, False, True, 0)

        column2.pack_start(self.name_entry, True, True, 0)
        column2.pack_start(self.genre_entry, True, True, 0)
        column2.pack_start(self.rating_entry, True, True, 0)
        column2.pack_start(self.platforms_entry, True, True, 0)
        column2.pack_start(self.price_entry, True, True, 0)

        listbox.add(row)

        self.grid.attach(box_outer, 0, 2, 4, 1)

        # Add action button
        button = Gtk.Button(label="Deploy Cartridge")
        button.connect("clicked", self.deploy_cartridge)
        self.grid.attach(button, 1, 4, 2, 1)

    def cb_show(self, w, data):
        self.show_all()
