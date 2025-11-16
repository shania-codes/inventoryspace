import sqlite3
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


# DB
def initdb():
    db = sqlite3.connect("data.db")
    cursor = db.cursor()

    # Locations Table
    cursor.execute("CREATE TABLE IF NOT EXISTS locations (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)")

    # Items Table
    cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, location_id INTEGER, FOREIGN KEY(location_id) REFERENCES locations(id) ON DELETE SET NULL)")
    
    # Attributes Table
    cursor.execute("CREATE TABLE IF NOT EXISTS attributes (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE)")

    # Item's Attributes Table
    cursor.execute("CREATE TABLE IF NOT EXISTS item_attributes (item_id INTEGER NOT NULL, attribute_id INTEGER NOT NULL, value TEXT, FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE, FOREIGN KEY(attribute_id) REFERENCES attributes(id) ON DELETE CASCADE)")

    # Tags Table
    cursor.execute("CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)")

    # ItemsTags Table
    cursor.execute("CREATE TABLE IF NOT EXISTS item_tags (item_id INTEGER NOT NULL, tag_id INTEGER NOT NULL, PRIMARY KEY (item_id, tag_id), FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE, FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE)")

    
    # Add initial "location" for items with no location
    cursor.execute("INSERT OR IGNORE INTO locations (id, name) VALUES (0, 'No Location')")

    #cursor.execute("INSERT INTO locations (id, name) VALUES (2, 'Freezer')")


    db.commit()
    db.close()
initdb()


class TheWhiteRoom(Gtk.Window):
    def __init__(self):
        super().__init__(title="The White Room")
        self.set_default_size(640,480) # TODO: Make it 16 colours only

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)
        self.init_dashboard()

    def clearall(self):
        # Removes all widgets in self.box "clearing" the screen"
        for child in self.box.get_children():
            self.box.remove(child)

    def init_dashboard(self, widget=None):
        self.clearall()
        self.welcomelabel = Gtk.Label(label="Welcome to The White Room", margin_top=20)
        self.box.add(self.welcomelabel)

        self.invspcbtn = Gtk.Button(label="Inventory Space", margin=200)
        self.invspcbtn.connect("clicked", self.init_invspc)
        self.box.add(self.invspcbtn) # make a grid to pack multiple different sub programs buttons like a phone home screen
        #https://lazka.github.io/pgi-docs/Gtk-3.0/classes/Grid.html#Gtk.Grid
        self.box.show_all()

    def init_invspc(self, widget):
        self.clearall() # Clear box
        
        # Add all locations
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM LOCATIONS")
        locations = cursor.fetchall()
        db.close()
        print(locations)
        self.location_labels = []
        for location in locations:
            label = Gtk.Label(label=location[1])
            self.box.add(label)
            self.location_labels.append(label)
            
        #print(self.location_labels) List of Gtk.Label objects


        self.dashboardbutton = Gtk.Button(label="Dashboard", margin=0)
        self.dashboardbutton.connect("clicked", self.init_dashboard)
        self.box.add(self.dashboardbutton)

        self.box.show_all()



win = TheWhiteRoom()
win.connect("destroy", Gtk.main_quit) # Close the program when the x button is pressed
win.show_all()
Gtk.main()