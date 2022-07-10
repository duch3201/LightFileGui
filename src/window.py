# window.py
#
# Copyright 2022 _Ghost_
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Adw, Gio, Gtk
import zlib
import os

appdir = os.getcwd()
print(appdir)
os.chdir(appdir)
try:
    os.mkdir("temp")
except FileExistsError:
    os.rmdir("temp")
    os.mkdir("temp")

class notifsuc:
    def send_notification():
        notification = Gio.Notification()
        notification.set_title("Lunch is ready")
        notification.set_body("Today we have pancakes and salad, and fruit and cake for dessert")

        file = Gio.File.new_for_path("fruitbowl.png")
        icon = Gio.FileIcon(file=file)

        notification.set_icon(icon)

@Gtk.Template(resource_path='/app/lf/lfgui/window.ui')
class LightfileguiWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'LightfileguiWindow'

    label = Gtk.Template.Child()
    open_button = Gtk.Template.Child()




    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        open_action = Gio.SimpleAction(name="open")
        open_action.connect("activate", self.open_file_dialog)
        self.add_action(open_action)
        self.add_action(open_action)

    def ComressFile(contents, comprlevel):
        comprout = zlib.compress(contents, comprlevel)
        print(comprout)

    def DecomressFile():
        print("hello2")

    def ConfigMod():
        print("hello3")

    def ConfigLoad():
        print("hello4")

    def on_open_response(self, dialog, response):
        # If the user selected a file...
        if response == Gtk.ResponseType.ACCEPT:
            # ... retrieve the location from the dialog and open it
            self.open_file(dialog.get_file())
        # Release the reference on the file selection dialog now that we
        # do not need it any more
        self._native = None

    def open_file_dialog(self, action, _):
        print("helo")

    def open_file_dialog(self, action, parameter):
        # Create a new file selection dialog, using the "open" mode
        # and keep a reference to it
        self._native = Gtk.FileChooserNative(
            title="Open File",
            transient_for=self,
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel",
        )
        # Connect the "response" signal of the file selection dialog;
        # this signal is emitted when the user selects a file, or when
        # they cancel the operation
        self._native.connect("response", self.on_open_response)
        # Present the dialog to the user
        self._native.show()

    def open_file(self, file):
        file.load_contents_async(None, self.open_file_complete)

    def open_file_complete(self, file, result):
        contents = file.load_contents_finish(result)
        print(contents)
        newcontetns = str(contents)
        bnewcontents = str.encode(newcontetns)
        comprlevel = 6
        comprout = zlib.compress(bnewcontents, comprlevel)
        os.chdir(appdir)
        os.chdir("Documents")
        with open("output.lfc", 'wb') as writecompr:
            str(comprout)
            writecompr.write(comprout)
            writecompr.flush()
        print(comprout)

        #notifsuc.send_notification("lunch-is-ready", notification)

        if not contents[0]:
            path = file.peek_path()
            print(f"Unable to open {path}: {contents[1]}")



class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'lightfilegui'
        self.props.version = "1.0"
        self.props.authors = ['_Ghost_']
        self.props.copyright = '2022 _Ghost_'
        self.props.logo_icon_name = 'app.lf.lfgui'
        self.props.modal = True
        self.set_transient_for(parent)
