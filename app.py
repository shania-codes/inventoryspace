import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class TheWhiteRoom(Gtk.Window):
    def __init__(self):
        super().__init__(title="The White Room")
        self.set_default_size(640,480) # TODO: Make it 16 colours only

        self.invspcbtn = Gtk.Button(label="Inventory Space", margin=200)
        self.invspcbtn.connect("clicked", self.invspcbtn_clicked)
        self.add(self.invspcbtn)

    def invspcbtn_clicked(self, widget):
        # Make it "redirect" to a new "page"



win = TheWhiteRoom()
win.connect("destroy", Gtk.main_quit) # Close the program when the x button is pressed
win.show_all()
Gtk.main()