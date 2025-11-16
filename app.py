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


    db.commit()
    db.close()
initdb()


class TheWhiteRoom(Gtk.Window):
    def __init__(self):
        super().__init__(title="The White Room")
        self.set_default_size(640,480) # TODO: Make it 16 colours only

        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.add(self.scrolled)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin=25)
        self.scrolled.add(self.box)
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

    # Make Inventory Space "page"
    def init_invspc(self, widget):
        self.clearall() # Clear box
        
        # Add all locations
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM locations")
        locations = cursor.fetchall()
        
        self.location_labels = [] # List of Tuple's ofGtk.Label objects paired with their add item button

        for location_id, location_name in locations:
            # Location name text
            label = Gtk.Label(label=location_name)
            self.box.add(label)

            # Get all items in this location
            cursor.execute("SELECT * FROM items WHERE location_id = ?", (location_id,))
            items = cursor.fetchall()
            for item in items:
                itembox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, margin=5)
                if item[2]: # item[2] is item description (TODO add input to dialog to save description)
                    itemlabel = Gtk.Label(label=f"{item[1]} - {item[2]}", margin_bottom=5)
                else:
                    itemlabel = Gtk.Label(label=f"{item[1]}", margin_bottom=5)
                itembox.add(itemlabel)

                # Edit Button
                edit_item_button = Gtk.Button(label="Edit")
                edit_item_button.item_id = item[0] # Add item ID as an attribute
                edit_item_button.connect("clicked", self.edit_item)
                itembox.add(edit_item_button)

                # Delete Button
                delete_item_button = Gtk.Button(label="Delete")
                delete_item_button.item_id = item[0]
                delete_item_button.connect("clicked", self.delete_item)
                itembox.add(delete_item_button)

                self.box.add(itembox)

            # Add item to this location button
            btn_add_item = Gtk.Button(label="Add item", margin_bottom=25)
            btn_add_item.location_id = location_id # adds attribute to button without making a sub class
            btn_add_item.connect("clicked", self.add_item_to_location)
            self.box.add(btn_add_item)

            self.location_labels.append((label, btn_add_item)) 


        # Back to dashboard button (Home screen)
        self.dashboardbutton = Gtk.Button(label="Dashboard", margin=0)
        self.dashboardbutton.connect("clicked", self.init_dashboard)
        self.box.add(self.dashboardbutton)
        db.close()
        self.box.show_all()


    def add_item_to_location(self, button):
        location_id = button.location_id

        dialog = Gtk.Dialog(title="Add Item", parent=self, flags=0)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Add", Gtk.ResponseType.OK)

        entry = Gtk.Entry()
        entry.set_placeholder_text("Item name")
        box = dialog.get_content_area()
        box.add(entry)
        dialog.show_all()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            item_name = entry.get_text()
            db = sqlite3.connect("data.db")
            cursor = db.cursor()
            cursor.execute("INSERT INTO items (name, location_id) VALUES (?, ?)", (item_name, location_id))
            item_id = cursor.lastrowid
            db.commit()
            db.close()

        dialog.destroy()
        self.init_invspc(widget=None)

    def edit_item(self, button):
        item_id = button.item_id
        
        # Get current item data
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM items WHERE id=?", (item_id,))
        item = cursor.fetchone()
        db.close()

        # Open Sub Window
        dialog = Gtk.Dialog(title="Edit Item", parent=self)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Save", Gtk.ResponseType.OK)

        box = dialog.get_content_area()

        name_entry = Gtk.Entry()
        name_entry.set_text(item[1])
        name_entry.set_placeholder_text("Item Name")
        box.add(name_entry)

        desc_entry = Gtk.Entry()
        desc_entry.set_text(item[2] or "")
        desc_entry.set_placeholder_text("Item Description")
        box.add(desc_entry)

        # Show Sub Window
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            new_name = name_entry.get_text()
            new_desc = desc_entry.get_text()
            db = sqlite3.connect("data.db")
            cursor = db.cursor()
            cursor.execute("UPDATE items SET name=?, description=? WHERE id=?", (new_name, new_desc, item_id))
            db.commit()
            db.close()

        dialog.destroy()
        self.init_invspc(None) # Refresh inventory space "page"

    def delete_item(self, button):
        return 0

win = TheWhiteRoom()
win.connect("destroy", Gtk.main_quit) # Close the program when the x button is pressed
win.show_all()
Gtk.main()