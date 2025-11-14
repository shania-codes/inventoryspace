import sys
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
# https://pygobject.gnome.org/tutorials/gtk4/introduction.html

# TODO is Gtk4 ugly on KDE/XFCE?
# TODO add something that makes it not work on Windows and Mac


def on_activate(self):
    win = Gtk.ApplicationWindow(application=app)
    win.set_default_size(800,600)

    dashboardbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    win.set_child(dashboardbox)

    label = Gtk.Label(label='Welcome to The White Room', halign=Gtk.Align.CENTER, valign=Gtk.Align.START, margin_top=15)
    dashboardbox.append(label)

    button = Gtk.Button(label="Inventory Space") # TODO Takes up max width
    button.connect('clicked', inventoryspace)
    dashboardbox.append(button)

    

    win.present()


def inventoryspace(button):
    inventoryspacebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    win.set_child(inventoryspacebox)
    


# Craete a new application
app = Gtk.Application(application_id="dev.sapphire.thewhiteroom")
app.connect("activate", on_activate)
# Run the application
app.run(None) 