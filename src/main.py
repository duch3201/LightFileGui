# main.py
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

import sys
import gi
import zlib

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import LightfileguiWindow, AboutDialog


class LightfileguiApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='app.lf.lfgui',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.quit, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

        self.set_accels_for_action('win.open', ['<Ctrl>o'])

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = LightfileguiWindow(application=self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = AboutDialog(self.props.active_window)
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

class ButtonWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Button Demo")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button = Gtk.Button.new_with_label("Click Me")
        button.connect("clicked", self.on_click_me_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Open")
        button.connect("clicked", self.on_open_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Close")
        button.connect("clicked", self.on_close_clicked)
        hbox.pack_start(button, True, True, 0)

    def on_click_me_clicked(self, button):
        print('"Click me" button was clicked')

    def on_open_clicked(self, button):
        print('"Open" button was clicked')

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

def main(version):
    """The application's entry point."""
    app = LightfileguiApplication()
    return app.run(sys.argv)


