import os

import pyrap
from pyrap.layout import ColumnLayout, RowLayout, StackLayout
from pyrap.ptypes import Color, Pixels, Image
from pyrap.widgets import Shell, Label, Composite, Button


class MultiPage:
    '''My pyRAP application'''

    def __init__(self):
        self.visible = 2  # initialize variable that indicates which page is visible

    def main(self, **kwargs):
        self._shell = Shell(maximized=True, titlebar=False)
        self._shell.bg = Color('red')
        self._shell.on_resize += self._shell.dolayout

        comp_mainframe = Composite(self._shell.content)
        comp_mainframe.layout = RowLayout(halign='fill', valign='fill', flexrows=1, vspace=0)

        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        # HEADER - we may not need this.. or maybe we do. You decide.
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        comp_header = Composite(comp_mainframe)
        comp_header.layout = ColumnLayout(halign='fill', valign='fill', flexcols=1, padding=Pixels(0))
        comp_header.bg = Color('green')

        btn_switch = Button(comp_header, text='Switch', halign='fill', valign='fill')
        lbl_header = Label(comp_header, text='<b>Click button to switch pages!</b>', markup=True, halign='fill', valign='fill')
        lbl_header.bg = 'transp'
        lbl_header.color = Color('white')

        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        # BODY - this is the 'main' composite that for the content. The visibility of the composites inside changes
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        self.comp_body = Composite(comp_mainframe, border=True)
        self.comp_body.layout = StackLayout(halign='fill', valign='fill')
        self.comp_body.bg = Color('white')

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # HOME PAGE #
        self.comp_home = Composite(self.comp_body)
        self.comp_home.layout = RowLayout(flexrows=0, halign='fill', valign='fill')
        self.comp_home.bg = Color('yellow')
        self.comp_home.visible = True
        Label(self.comp_home, text='<b>Page 1</b>', markup=True)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # ANOTHER PAGE #
        self.comp_second = Composite(self.comp_body)
        self.comp_second.layout = RowLayout(flexrows=0, halign='fill', valign='fill')
        self.comp_second.bg = Color('green')
        self.comp_second.bgimg = Image(os.path.join('..', 'controls', 'images', 'pyrap-logo.png'))
        # .resize(height='550px'))
        self.comp_second.visible = False
        Label(self.comp_second, text='<b>Page 2</b>', markup=True)


        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # THIRD PAGE #
        self.comp_third = Composite(self.comp_body)
        self.comp_third.layout = RowLayout(flexrows=0, halign='fill', valign='fill')
        self.comp_third.bg = Color('yellow')
        self.comp_third.visible = False
        Label(self.comp_third, text='<b>Page 3</b>', markup=True)

        # THIRD PAGE #
        self.comp_four = Composite(self.comp_body)
        self.comp_four.layout = RowLayout(flexrows=0, halign='fill', valign='fill')
        self.comp_four.bg = Color('red')
        self.comp_four.visible = False
        Label(self.comp_four, text='<b>Page 4</b>', markup=True)

        # LISTENER FUNCTION TO SWITCH PAGE VISIBILITY
        def open_menu(*_):
            self.visible = (self.visible + 1) % 4  # if you don't understand this, learn about the modulo operator (Euclidean division)

            # switch the three pages all around
            self.comp_home.visible = self.visible == 0
            self.comp_home.layer = (0 - self.visible) % 4
            self.comp_second.visible = self.visible == 1
            self.comp_second.layer = (1 - self.visible) % 4
            self.comp_third.visible = self.visible == 2
            self.comp_third.layer = (2 - self.visible) % 4
            self.comp_four.visible = self.visible == 3
            self.comp_four.layer = (3 - self.visible) % 4

        # assign listener function to button click
        btn_switch.on_select += open_menu

        self._shell.show()


def main():
    pyrap.register(clazz=MultiPage,
                   entrypoints={'start': MultiPage.main},
                   path='multipage',
                   name='How stacklayouting works!')
    pyrap.run()


if __name__ == '__main__':
    main()
