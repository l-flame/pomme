#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys


manager = KeyBindingManager()
registry = manager.registry


@registry.add_binding(Keys.ControlQ, eager=True)
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `CommandLineInterface.run()` call.
    """
    event.cli.set_return_value(-1)


from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FillControl, TokenListControl
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.shortcuts import create_eventloop

from pygments.token import Token

layout = VSplit([
    # One window that holds the BufferControl with the default buffer on the
    # left.
    Window(content=BufferControl(buffer_name=DEFAULT_BUFFER)),

    # A vertical line in the middle. We explicitely specify the width, to make
    # sure that the layout engine will not try to divide the whole width by
    # three for all these windows. The `FillControl` will simply fill the whole
    # window by repeating this character.
    Window(width=D.exact(1),
           content=FillControl('|', token=Token.Line)),

    # Display the text 'Hello world' on the right.
    Window(content=TokenListControl(
        get_tokens=lambda cli: [(Token, 'Hello world')])),
])

loop = create_eventloop()
application = Application(key_bindings_registry=registry, layout=layout, use_alternate_screen=True)
cli = CommandLineInterface(application=application, eventloop=loop)
cli.run()
print('Exiting')