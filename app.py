import sys
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk
#TODO find the right docs, check if it's these first:
# https://api.pygobject.gnome.org/Gtk-4.0/index.html
# https://api.pygobject.gnome.org/GLib-2.0/index.html
# GObject isn't the right one
# https://developer.gnome.org/documentation/tutorials/beginners/components.html
# https://pygobject.gnome.org/tutorials/gtk4/introduction.html

# TODO is Gtk ugly on KDE/LXQt/non gnome DE/WMs?
# TODO add something that makes it not work on Windows and Mac, just because


class MyApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="dev.sapphire.thewhiteroom") # https://developer.gnome.org/documentation/tutorials/application-id.html
        GLib.set_application_name("The White Room") # Doesn't do anything?
        
        

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self, title="The White Room") # Initial Window
        window.set_default_size(800,600)

        box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10) # https://docs.gtk.org/gtk4/class.Box.html this is the C docs not Python
        window.set_child(box)

        # TODO use grid instead https://docs.gtk.org/gtk4/class.Grid.html <-- C not Python

        label = Gtk.Label(label='Welcome to The White Room', halign=Gtk.Align.CENTER, valign=Gtk.Align.START, margin_top=15)
        box.append(label)

        #print(dir(label.props))

        button = Gtk.Label(label="Inventory Space")
        box.append(button)

        window.present()


app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)