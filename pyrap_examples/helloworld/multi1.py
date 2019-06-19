import os

import pyrap
from pyrap import session
from pyrap.layout import ColumnLayout, RowLayout, StackLayout
from pyrap.ptypes import Color, Pixels, Image
from pyrap.widgets import Shell, Label, Composite, Button, Edit


class MultiPage:
    '''My pyRAP application'''

    def __init__(self):
        self.visible = 0  # initialize variable that indicates which page is visible

    def main(self, **kwargs):
        self._shell = Shell(maximized=True, titlebar=False)
        self._shell.bg = Color('red')
        self._shell.on_resize += self._shell.dolayout

        comp_mainframe = Composite(self._shell.content)
        comp_mainframe.layout = RowLayout(halign='fill', valign='fill', flexrows=1, vspace=0)
        #
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        # HEADER - we may not need this.. or maybe we do. You decide.
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        comp_header = Composite(comp_mainframe)
        comp_header.layout = ColumnLayout(halign='fill', valign='fill', flexcols=1, padding=Pixels(0))
        comp_header.bg = Color('green')
        #
        # btn_switch = Button(comp_header, text='Switch', halign='fill', valign='fill')
        # lbl_header = Label(comp_header, text='<b>Click button to switch pages!</b>', markup=True, halign='fill', valign='fill')
        # lbl_header.bg = 'transp'
        # lbl_header.color = Color('white')

        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        # BODY - this is the 'main' composite that for the content. The visibility of the composites inside changes
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        self.comp_body = Composite(comp_mainframe, border=True)
        self.comp_body.layout = StackLayout(halign='fill', valign='fill')
        self.comp_body.bg = Color('white')

        # Button comp

        self.comp_cont = Composite(comp_mainframe)
        self.comp_cont.layout = ColumnLayout(halign='fill', valign='fill', equalwidths=True)
        self.comp_cont.bg = Color('white')

        # Create Button for control pages next and back

        btn_cont = Button(comp_mainframe, text='Next', halign='fill', valign='fill')
        btn_cont.bg = 'transp'

        btn_cont1 = Button(comp_mainframe, text='Back', halign='fill', valign='fill')
        # img=Image(os.path.join('..', 'controls', 'images', 'pyrap-logo.png'))
        btn_cont1.bg = 'transp'

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # HOME PAGE #
        self.comp_home = Composite(self.comp_body)
        self.comp_home.layout = ColumnLayout(flexcols={0: 2, 1: 2}, halign='fill', valign='fill')
        self.comp_home.bg = Color('yellow')
        self.comp_home.bgimg = Image(os.path.join('..', 'controls', 'images', 'al5.png'))
        # self.comp_home.bgimg = Image(os.path.join('..', 'controls', 'images', 'al2.png'))
        Label(self.comp_home, img=Image(os.path.join('..', 'controls', 'images', 'al5.png')))
        self.comp_home.visible = True
        lbl=Label(self.comp_home, text='Welcome to Kids Space Station.I \n' 
                                   'have exciting info and service for you', markup=False, multiline=True)
        lbl.font=lbl.font.modify(size=10)
        lbl.color=Color("#00ff00")


        comp_hm = Composite(self.comp_home)
        comp_hm.layout = ColumnLayout(halign='fill', valign='fill', equalwidths=True)
        comp_hm.bg = Color('white')

        # Create Button for control pages next and back

        btn_hm = Button(comp_hm, text='Next')
        btn_hm.bg = 'transp'

        btn_hm1 = Button(comp_hm, text='Back')
        # img=Image(os.path.join('..', 'controls', 'images', 'pyrap-logo.png'))
        btn_hm1.bg = 'transp'



        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # ANOTHER PAGE #
        self.comp_second = Composite(self.comp_body)
        self.comp_second.layout = ColumnLayout(flexcols=0, halign='fill', valign='fill')
        self.comp_second.bg = Color('black')
        self.comp_second.bgimg = Image(os.path.join('..', 'controls', 'images', 'al2.png')).resize(height= Pixels(550))
        self.comp_second.visible = False
        Label(self.comp_second, text='<b><font size="5" color="#00ff00">I have exciting info and service for you </font></b>', markup=True)

        comp_sd = Composite(self.comp_second)
        comp_sd.layout = ColumnLayout(halign='fill', valign='fill', flexcols=0)
        comp_sd.bg = Color('white')

        # Create Button for control pages next and back

        btn_sd = Button(comp_sd, text='Info', halign='fill', valign='fill')
        btn_sd.bg = 'transp'

        comp_sd1 = Composite(self.comp_second)
        comp_sd1.layout = ColumnLayout(halign='fill', valign='fill', flexcols=0)
        comp_sd1.bg = Color('white')

        btn_sd1 = Button(comp_sd1, text='Info2', halign='fill', valign='fill')
        btn_sd1.bg = 'transp'


        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # THIRD PAGE #
        self.comp_third = Composite(self.comp_body)
        self.comp_third.layout = RowLayout(flexrows=0, halign='fill', valign='fill')
        self.comp_third.bg = Color('yellow')
        self.comp_third.bgimg = Image(os.path.join('..', 'controls', 'images', 'al4.jpeg'))
        self.comp_third.visible = False
        lblbuttn=Label(self.comp_third, img=Image(os.path.join('..', 'controls', 'images', 'al5.png')), markup=True)
        lblbuttn.bg = 'transp'

        # THIRD PAGE #
        self.comp_four = Composite(self.comp_body)
        self.comp_four.layout = RowLayout(flexrows=0, halign='fill', valign='fill')
        self.comp_four.bg = Color('red')
        self.comp_four.bgimg = Image(os.path.join('..', 'controls', 'images', 'al5.png'))
        self.comp_four.visible = False
        Label(self.comp_four, text='<b>Page 4</b>', markup=True)
        btn_showdialog = Button(self.comp_four, text='Show Dialog', halign='fill', valign='fill')

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

        # LISTENER FUNCTION TO SWITCH PAGE VISIBILITY
        def back_menu(*_):
            self.visible = (self.visible - 1) % 4  # if you don't understand this, learn about the modulo operator (Euclidean division)

            # switch the three pages all around
            self.comp_home.visible = self.visible == 0
            self.comp_home.layer = (0 - self.visible) % 4
            self.comp_second.visible = self.visible == 1
            self.comp_second.layer = (1 - self.visible) % 4
            self.comp_third.visible = self.visible == 2
            self.comp_third.layer = (2 - self.visible) % 4
            self.comp_four.visible = self.visible == 3
            self.comp_four.layer = (3 - self.visible) % 4

        def resize_bg (*_):

            w = session.runtime.display.width.value
            h = session.runtime.display.height.value
            self.comp_home.bgimg = self.comp_home.bgimg.resize(width= Pixels(w), height=Pixels(h))
            self.comp_second.bgimg = self.comp_second.bgimg.resize(width=Pixels(w), height=Pixels(h))
            self.comp_third.bgimg = self.comp_third.bgimg.resize(width=Pixels(w), height=Pixels(h))
            self.comp_four.bgimg = self.comp_four.bgimg.resize(width=Pixels(w), height=Pixels(h))
            print(w,h)
            self._shell.dolayout()


        def showdialog(*_):
            # this will create a new dialog every time the button is clicked. You can also create it when setting
            # up the layout and set its visibility to false after calling wnd_dialog.show(), then set the visibility
            # to true in the listener function that is called when the button is clicked (will only work if the window
            # was hidden before. Closing the window will destroy the widget and an error will be thrown when trying
            # to make it visible again.
            wnd_dialog = Shell(parent=self._shell, titlebar=True, border=True, resize=False, modal=True,
                               halign='center', valign='center', btnmin= False)
            wnd_dialog.create_content()
            wnd_dialog.content.bg = Color('white')

            w = session.runtime.display.width.value
            h = session.runtime.display.height.value
            wnd_dialog.bounds = w / 2 - 200, h / 2 - 150, 400, 300

            cmp_dialog = Composite(wnd_dialog.content)
            cmp_dialog.layout = RowLayout(valign='fill', halign='fill', flexrows=0)

            lbl_wnd = Label(cmp_dialog, text='Blafasel <b> This is really important</b>', markup=True, valign='fill', halign='fill')
            lbl_wnd.bg = Color('red')

            wnd_dialog.show()

        def dosomething(*_):
            lbl_wnd.text = '<b>I did something!</b>'

            btn_dosomething = Button(cmp_dialog, text='Do something', valign='fill', halign='fill')
            btn_dosomething.on_select += dosomething

            wnd_dialog.show()


        # assign listener function to button click
        # btn_switch.on_select += open_menu
        btn_cont.on_select += open_menu

        btn_cont1.on_select += back_menu

        btn_hm.on_select += open_menu

        btn_hm1.on_select += back_menu

        lblbuttn.on_mousedown += resize_bg
        lblbuttn.on_mousedown += showdialog

        btn_sd.on_select += showdialog

        self._shell.on_resize +=resize_bg
        resize_bg()

        btn_showdialog.on_select += showdialog


        self._shell.show()


def main():
    pyrap.register(clazz=MultiPage,
                   entrypoints={'start': MultiPage.main},
                   path='multipage',
                   name='How stacklayouting works!')
    pyrap.run()


if __name__ == '__main__':
    main()
