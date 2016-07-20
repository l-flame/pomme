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

@registry.add_binding(Keys.ControlW, eager=True)
def _(event):
    print event.__dict__, event.cli.__dict__


from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window, HSplit
from prompt_toolkit.layout.controls import BufferControl, FillControl, TokenListControl
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.interface import AcceptAction

from pygments.token import Token

def get_titlebar_tokens(cli):
    return [
        (Token.Title, ' Hello world '),
        (Token.Title, ' (Press [Ctrl-Q] to quit.)'),
]

def accept_action(cli, buffer):
    print buffer.document, dir(buffer.document), buffer.document.text
    buffers['RESULT'].text += buffer.document.text + '\n'
    buffer.reset()

buffers={
    DEFAULT_BUFFER: Buffer(is_multiline=True, accept_action=AcceptAction(handler=accept_action)),
    'RESULT': Buffer(is_multiline=True),
}



layout = HSplit([
    Window(height=D.exact(1),
           content=TokenListControl(get_titlebar_tokens, align_center=True)),
    Window(height=D.exact(1),
           content=FillControl('-', token=Token.Line)),

    # The 'body', like defined above.
])

layout = HSplit([layout, VSplit([

    # One window that holds the BufferControl with the default buffer on the
    # left.
    HSplit([Window(content=BufferControl(buffer_name="RESULT"),
           width=D.exact(95)),
            Window(height=D.exact(1),
           content=FillControl('-', token=Token.Line)),
           Window(content=BufferControl(buffer_name=DEFAULT_BUFFER),
           width=D.exact(95), height=D.exact(5)),
           ]
            ),

    # A vertical line in the middle. We explicitely specify the width, to make
    # sure that the layout engine will not try to divide the whole width by
    # three for all these windows. The `FillControl` will simply fill the whole
    # window by repeating this character.
    Window(width=D.exact(1),
           content=FillControl('|', token=Token.Line)),

    # Display the text 'Hello world' on the right.
    Window(content=TokenListControl(
            get_tokens=lambda cli: [(Token, 'Chat users\n'+'-'*70)]),
            width=D.exact(20)
    )
])])

loop = create_eventloop()
application = Application(key_bindings_registry=registry, layout=layout, use_alternate_screen=True, buffers=buffers)
cli = CommandLineInterface(application=application, eventloop=loop)
cli.run()
print('Exiting')
