import gi
import os

from populus import Project

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


def get_chain():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),
             '..', '..', 'core'))
    project = Project()
    chain_name = os.environ.get('CHAIN', 'external')
    return project.get_chain(chain_name)


class WalletWindow(Gtk.Window):

    def __init__(self, root):
        super(WalletWindow, self).__init__()
        self.set_border_width(10)

        self.app = root
        self.set_title('{} - Wallet'.format(self.app.name))

        self.load_wallet()
        self.create_ui()

        self.update_balance()

    def load_wallet(self):
        with get_chain() as chain:
            LotusToken = chain.provider.get_contract_factory('LotusToken')
            token_address = os.environ['TOKEN_CONTRACT_ADDRESS']
            self.lotus_token = LotusToken(address=token_address)
            self.account = chain.web3.eth.coinbase

    def transfer(self, widget):
        with get_chain() as chain:

            amount = int(self.amount_field.get_text())
            bob = self.to_address_field.get_text()

            set_txn_hash = self.lotus_token.transact().transfer(bob, amount)
            chain.wait.for_receipt(set_txn_hash)

            self.update_balance()

    def update_balance(self):
        balance = self.lotus_token.call().balanceOf(self.account)
        self.balance_label.set_text('Balance: {}'.format(balance))

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
        amount_label = Gtk.Label("Amount", xalign=0)
        to_address_label = Gtk.Label("To Address", xalign=0)
        self.amount_field = Gtk.Entry()
        self.amount_field.set_text('100')
        self.to_address_field = Gtk.Entry()
        self.to_address_field.set_text(
            '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae')
        self.to_address_field.set_width_chars(42)
        # Layout construction, it is a 2x2 box
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)
        row = Gtk.ListBoxRow()
        container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(container)
        column1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.pack_start(column1, True, True, 0)
        column1.pack_start(amount_label, True, True, 0)
        column1.pack_start(to_address_label, True, True, 0)
        column2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        column2.pack_start(self.amount_field, True, True, 0)
        column2.pack_start(self.to_address_field, True, True, 0)
        container.pack_start(column2, False, True, 0)

        listbox.add(row)

        self.grid.attach(box_outer, 0, 2, 4, 1)

        # Add action button
        button = Gtk.Button(label="Send Lotus Token")
        button.connect("clicked", self.transfer)
        self.grid.attach(button, 1, 4, 2, 1)

    def cb_show(self, w, data):
        self.show_all()
