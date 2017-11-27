'''
Created on Oct 2, 2015

@author: nyga
'''
import base64
import json
from collections import OrderedDict

import sys
from dnutils import out
from dnutils.threads import sleep, ThreadInterrupt
from dnutils.tools import ifnone

import pyrap
from pyrap import session
from pyrap.dialogs import msg_ok, msg_warn, msg_err, ask_yesno, ask_yesnocancel, \
    ask_okcancel, open_progress, ask_color
from pyrap.layout import GridLayout, RowLayout, CellLayout, ColumnLayout
from pyrap.ptypes import BoolVar, Color, px, Image, Font
# from pyrap.pwt.cluster.cluster import Cluster
# from pyrap.pwt.radar.radar import RadarChart
# from pyrap.pwt.radar_redesign.radar_redesign import RadarChartRed
from pyrap.widgets import Label, Button, RWT, Shell, Checkbox, Composite, Edit, \
    Group, ScrolledComposite, Browser, List, Canvas, StackedComposite, Scale, \
    Menu, MenuItem, Spinner, info, FileUpload, TabFolder, Table, Sash, Toggle, DropDown, Combo


class Images:
    IMG_UP = Image('images/icons/up.gif')
    IMG_DOWN = Image('images/icons/down.gif')
    IMG_CHECK = Image('images/icons/tick.png')
    IMG_RED = Image('images/icons/bullet_red.png')
    IMG_GREEN = Image('images/icons/bullet_green.png')
    IMG_WHITE = Image('images/icons/bullet_white.png')


class ControlsDemo():
    
    @staticmethod
    def setup(application): pass

    def desktop(self, **kwargs):
        self.shell = Shell(maximized=True, titlebar=False)
        self.shell.on_resize += self.shell.dolayout
        shell = self.shell
        self.mainwnd = shell
        
        #=======================================================================
        # main layout
        #=======================================================================
        scroll = ScrolledComposite(shell.content, vscroll=1, hscroll=0, halign='fill', valign='fill', minwidth=100, minheight=100)
        outer = scroll.content
        outer.layout = RowLayout(halign='fill', valign='fill', flexrows=2)
        
        #=======================================================================
        # header
        #=======================================================================
        header = Composite(outer)
        header.layout = ColumnLayout(halign='fill', minheight='90px', flexcols=1)
        header.bgimg = Image('images/background-green.jpg')
        header.css = 'header'
        
        #=======================================================================
        # nav bar
        #=======================================================================
        navbar = Composite(outer, minheight=px(30), halign='fill', valign='fill', padding=0, padding_bottom=15)
        navbar.css = 'navbar'
        
        self.beny_logo = Image('images/pyrap-logo.png').resize(height='75px')
        logo = Label(header, img=self.beny_logo, valign='center', halign='fill')
        logo.bg = 'transp'    
        welcome = Label(header, text='pyRAP - Controls Demo', halign='center', valign='center')
#         welcome.color = 'white'
        welcome.css = 'header'
        welcome.bg = 'transp'
#         welcome.font = welcome.font.modify(size=24, bf=True, it=True)
        #=======================================================================
        # main area
        #=======================================================================
        main = Composite(outer)
        main.layout = ColumnLayout(halign='fill', valign='fill', flexcols=2, minheight=500)
        self.navigation = List(main, border=1, valign='fill', 
                          minwidth=px(250),
                          vscroll=1)
        # =======================================================================
        # footer
        # =======================================================================
        sash = Sash(main, orientation='v', valign='fill')

        def resize(event):
            out(event, 'x', event.x, 'y', event.y)

        sash.on_select += resize

        #=======================================================================
        # footer
        #=======================================================================
        footer = Composite(outer, border=True)
        footer.layout = ColumnLayout(halign='fill', flexcols=0, minheight=50)
        footer.bgimg = Image('images/background_grey.png')
        footer.bg = 'light grey'
        pyversion = '.'.join(map(str, sys.version_info[:3]))
        Label(footer, halign='left', valign='bottom', text='powered by pyRAP v%s on Python %s' % (pyrap.__version__, pyversion)).bg = 'transp'

        #=======================================================================
        # content area
        #=======================================================================
        self.content = StackedComposite(main, halign='fill', valign='fill')
        self.create_pages()
        self.navigation.on_select += self.switch_page
        self.navigation.selection = self.pages['Tables']
        self.switch_page()

        self.shell.show(True)

    def switch_page(self, *args):
        for page in (self.pages.values()):
            page.layout.exclude = self.navigation.selection is not page
        self.content.selection = self.navigation.selection
        self.shell.onresize_shell()

    def create_pages(self):
        self.pages = OrderedDict()
        #=======================================================================
        # create scale page
        #=======================================================================
        page  = self.create_page_template('Scale Widget Demo')
        self.create_scale_page(page)
        self.pages['Scale'] = page
        
        # =======================================================================
        # crete canvas page
        # =======================================================================
        page = self.create_page_template('Canvas Demo')
        self.create_canvas_page(page)
        self.pages['Canvas'] = page
        
        #=======================================================================
        # create button page
        #=======================================================================
        page = self.create_page_template('Button Widget Demo')
        self.create_button_page(page)
        self.pages['Button'] = page
        
        #=======================================================================
        # create browser page
        #=======================================================================
        page = self.create_page_template('Browser Widget Demo')
        self.create_browser_page(page)
        self.pages['Browser'] = page
        
        #=======================================================================
        # crete menu page
        #=======================================================================
        page = self.create_page_template('Menu Demo')
        self.create_menu_page(page)
        self.pages['Menu'] = page
        
        #=======================================================================
        # crete list page
        #=======================================================================
        page = self.create_page_template('List Demo')
        self.create_list_page(page)
        self.pages['List'] = page
        
        #=======================================================================
        # create dialogs page
        #=======================================================================
        page  = self.create_page_template('Dialog Demo')
        self.create_dialogs_page(page)
        self.pages['Dialogs'] = page
        
        #=======================================================================
        # create spinner page
        #=======================================================================
        page  = self.create_page_template('Spinner Demo')
        self.create_spinner_page(page)
        self.pages['Spinner'] = page
        
        #=======================================================================
        # create fileupload
        #=======================================================================
        page  = self.create_page_template('File Upload Demo')
        self.create_upload_page(page)
        self.pages['FileUpload'] = page

        # =======================================================================
        # create tab folders
        # =======================================================================
        page = self.create_page_template('Tab Folders')
        self.create_tabfolder_page(page)
        self.pages['TabFolders'] = page

        # =======================================================================
        # create tab folders
        # =======================================================================
        page = self.create_page_template('Scrolled Composite')
        self.create_scrolled_page(page)
        self.pages['Scrolled'] = page

        page = self.create_page_template('Table Demo')
        self.create_table_page(page)
        self.pages['Tables'] = page

        page = self.create_page_template('Sash Demo')
        self.create_sash_page(page)
        self.pages['Sash'] = page

        #=======================================================================
        # create radar chart
        #=======================================================================
        # page  = self.create_page_template('Radar Chart Demo')
        # self.create_radar_page(page)
        # self.pages['Radar'] = page

        #=======================================================================
        # create D3 cluster chart
        #=======================================================================
        # page = self.create_page_template('D3 Cluster')
        # self.create_cluster_page(page)
        # self.pages['Cluster'] = page
        
        for page in [self.pages[k] for k in sorted(self.pages.keys())][1:]:
            page.layout.exclude = True
        self.navigation.items = self.pages

    def create_page_template(self, heading):
        # content area
        tab = Composite(self.content)
        tab.layout = RowLayout(halign='fill', valign='fill', flexrows={1: 2, 2: 1, 3: .5})
        #heading
        header = Label(tab, text=heading, halign='left')
        header.css = 'headline'#font = header.font.modify(size='16px', bf=1)
        return tab

    def create_sash_page(self, parent):
        container = Composite(parent, layout=ColumnLayout(halign='fill', valign='fill', flexcols=[0,2]))

        left = Label(container, 'LEFT', halign='fill', valign='fill', border=True)
        sash = Sash(container, orientation='v', valign='fill')

        right = Label(container, 'RIGHT', halign='fill', valign='fill', border=True)


    def create_table_page(self, parent):
        table = Table(parent, halign='fill', valign='fill', headervisible=True, colsmoveable=True, check=True)
        table.addcol('Last Name', img=Images.IMG_RED)
        table.addcol('First Name')
        table.addcol('Title')

        table.additem(['Nyga', 'Daniel', 'Dr.'], images=[Images.IMG_CHECK, None, Images.IMG_GREEN, None])
        table.additem(['Picklum', 'Mareike', 'M.Sc.'], images=[Images.IMG_CHECK, None, Images.IMG_GREEN, None])
        table.additem(['Beetz', 'Michael', 'Prof. PhD.'], images=[Images.IMG_DOWN, None, Images.IMG_WHITE, None])
        table.additem(['Balint-Benczedi', 'Ferenc', 'M.Sc.'], images=[Images.IMG_DOWN, None, Images.IMG_RED, None])

        m = Menu(table, popup=True)
        insert = MenuItem(m, 'Insert...')
        delete = MenuItem(m, 'Delete...')

        def insertitem(event):
            dlg = Shell(parent=self.shell, title='Create new entry')
            dlg.content.layout = GridLayout(valign='fill', equalheights=True, cols=2, padding=20)
            Label(dlg.content, 'First Name:', halign='right')
            fname = Edit(dlg.content, minwidth=200)
            Label(dlg.content, 'Last Name:', halign='right')
            lname = Edit(dlg.content, minwidth=200)
            Label(dlg.content, 'Title', halign='right')
            title = Combo(dlg.content, halign='fill')
            title.items = ['M. Sc.', 'Dr.', 'Prof.']
            Composite(dlg.content)
            buttons = Composite(dlg.content, layout=ColumnLayout(equalwidths=True))
            ok = Button(buttons, 'OK')
            cancel = Button(buttons, 'Cancel')
            dlg.tabseq = (fname, lname, title, ok, cancel)

            def insert(event):
                table.additem([lname.text, fname.text, title.text])
                dlg.close()

            ok.on_select += insert
            cancel.on_select += lambda _: dlg.close()
            dlg.show(True)

        insert.on_select += insertitem

        def rmitem(*_):
            if table.selection:
                doit = ask_yesno(self.shell, 'Please confirm', 'Are you sure you want to delete %s' % table.selection) == 'yes'
                if doit:
                    table.rmitem(table.selection)
            if not table.items:
                delete.enabled = False

        delete.on_select += rmitem

        table.menu = m

    def create_scrolled_page(self, parent):
        page = Composite(parent, layout=CellLayout(halign='fill', valign='fill'))
        container = Composite(page, layout=RowLayout())
        Label(container, 'This frame is scrollable:', halign='left')
        scrolled = ScrolledComposite(container, vscroll=True, hscroll=True, minwidth=300, minheight=300, border=True)
        scrolled.content.layout = CellLayout(minwidth=700, minheight=700)  #RowLayout(halign='fill', valign='fill')
        Label(scrolled.content, halign='fill', valign='fill', padding=20).css = 'bgrepeat'

    def create_tabfolder_page(self, parent):
        page = Composite(parent, layout=RowLayout(halign='fill', valign='fill', equalheights=True))
        tabs = TabFolder(page, halign='center', valign='center', tabpos='bottom', minheight=200)
        page1 = tabs.addtab('First Page')
        Label(page1, 'Hello', halign='fill', valign='fill').bg = 'red'
        page2 = tabs.addtab('Second Page')
        Label(page2, 'pyRAP!', halign='center', valign='center').bg = 'yellow'
        tabs.selected = 0

    def create_upload_page(self, parent):
        body = Composite(parent)
        body.layout = RowLayout(halign='fill', valign='fill', flexrows=3)
        upload = FileUpload(body, text='Browse...', multi=True, halign='left', valign='top')
        cont = Composite(body)
        cont.layout = GridLayout(cols=2, halign='fill', flexcols=1)
        Label(cont, 'Filename:')
        filename = Label(cont, halign='fill')
        Label(cont, 'File size:')
        filesize = Label(cont, halign='fill')
        Label(cont, 'File Type:')
        filetype = Label(cont, halign='fill')
        Label(body, text='Content:', halign='fill')
        content = Edit(body, halign='fill', valign='fill', multiline=True, wrap=True)
        content.font = Font(family='monospace', size='11px')
        def uploaded():
            files = session.runtime.servicehandlers.fileuploadhandler.files[upload.token]
            filename.text = ', '.join([f['filename'] for f in files])
            fullcnt = ''
            for f in files:
                try:
                    if filetype.text.startswith('application'): raise UnicodeDecodeError()
                    fullcnt += f['filecontent'].decode('utf8')
                except UnicodeDecodeError:
                    fullcnt += base64.b64encode(f['filecontent']).decode()
                fullcnt += '\n\n'
            filesize.text = '%d Byte' % (len(fullcnt)-2)
            filetype.text = ', '.join([f['filetype'] for f in files])
            content.text = fullcnt
        upload.on_finished += uploaded
    
    def create_spinner_page(self, parent):
        body = Composite(parent, layout=ColumnLayout(valign='fill', halign='fill', equalwidths=True))
        # spinners
        grp = Group(body, 'Spinners')
        grp.layout = GridLayout(cols=2, equalheights=True)
        Label(grp, text='Simple Spinner:', halign='left')
        s1 = Spinner(grp)
        Label(grp, text='Spinner:', halign='left')
        s2 = Spinner(grp)        
        Label(grp, 'Current value:', halign='left')
        l = Label(grp, halign='fill')
        
        def onchange(*_):
            l.text = str(s2.asfloat(s2.selection))
        
        s2.on_modify += onchange
        
        # settings
        settings = Group(body, 'Settings')
        settings.layout = GridLayout(cols=2, equalheights=True)
        
        Label(settings, 'Minimum:', halign='right')
        min_ = Edit(settings, text=str(s1.min), halign='fill')

        Label(settings, 'Maximum:', halign='right')
        max_ = Edit(settings, text=str(s1.max), halign='fill')
        
        Label(settings, 'Digits:', halign='right')
        digs = Spinner(settings, vmin=0, vmax=10, digits=0, sel=s1.digits)
        
        Label(settings, 'Selection', halign='right')
        sel = Edit(settings, text=ifnone(s2.selection, '', str), halign='fill')
        
        Label(settings)
        apply = Button(settings, halign='right', text='Apply')
        
        def apply_settings(*_):
            s1.min = int(min_.text)
            s2.min = int(min_.text)
            s1.max = int(max_.text)
            s2.max = int(max_.text)
            s1.digits = digs.selection
            s2.digits = digs.selection
            s2.selection = s1.selection = None if sel.text == '' else int(sel.text)
            
        apply.on_select += apply_settings
        self.shell.tabseq = (s1, s2, min_, max_, digs, sel, apply)
            
    def create_dialogs_page(self, parent):
        grp_info_dlgs = Composite(parent)#, text='Info Dialogs')
        grp_info_dlgs.layout = ColumnLayout(valign='fill', minheight=100)
        grp_info_dlgs.bg = Color('blue')

        b = Button(grp_info_dlgs, 'Show Info', halign='fill')
        b.decorator = info('this is a decorator description.')

        def showinfo(*_):
            ret = msg_ok(self.shell,
                   title='pyRAP Message Box', 
                   text='This is my first message. It can also span multiple lines. You just have to put\nnewline in the message box text.')
            out('message box returned', ret)
        b.on_select += showinfo
        
        b = Button(grp_info_dlgs, 'Show Warning', halign='fill')
        def showwarn(*_):
            msg_warn(self.shell, title='pyRAP Warning', text='This is my first message. It can also span multiple lines. You just have to put\nnewline in the message box text.')
        b.on_select += showwarn
        
        b = Button(grp_info_dlgs, 'Show Error', halign='fill')
        def showerr(*_):
            msg_err(self.shell, title='Error Box', text='This is my first message. It can also span multiple lines. You just have to put\nnewline in the message box text.')
        b.on_select += showerr
        
        grp_progress_dlgs = Composite(parent)#, text='Other Dialogs')
        grp_progress_dlgs.layout = ColumnLayout(valign='fill')
        grp_progress_dlgs.bg = Color('yellow')

        def process(dlg):
            try:
                dlg.status = 'Preparing a time-consuming task...'
                dlg.setloop(1)
                sleep(2.5)
                dlg.setloop(0)
                dlg.max = 100
                for i in range(100):
                    dlg.status = 'Step %d completed' % (i+1)
                    dlg.inc()
                    if dlg.interrupted: return
                    dlg.push.flush()
                    sleep(.1)
                dlg.status = 'Done. All tasks completed.'
                dlg.setfinished()
                dlg.push.flush()
            except ThreadInterrupt:
                out('process was interrupted.')

        b = Button(grp_progress_dlgs, 'Open Progress...', halign='fill')
        def showprog(*_):
            open_progress(self.shell, 'Progress Report', 'Running a long procedure...', target=process)
        b.on_select += showprog
        
        b = Button(grp_progress_dlgs, 'Change color...', valign='center')
        def showcolor(*_):
            color = ask_color(self.shell)
            out('user picked', color)
            grp_progress_dlgs.bg = color
        b.on_select += showcolor
        
        grp_info_dlgs = Composite(parent)#, text='Question Dialogs')
        grp_info_dlgs.layout = ColumnLayout(valign='fill')
        grp_info_dlgs.bg = Color('red')

        b = Button(grp_info_dlgs, 'Yes-No Question')
        def ask_yesno_(*_):
            resp = ask_yesno(self.shell, title='pyRAP Message Box', text='This is my first message. It can also span multiple lines. You just have to put\nnewline in the message box text.\n\nAre you OK with that?')
            msg_ok(self.shell, 'Info', 'The user clicked %s' % resp)
        b.on_select += ask_yesno_
        
        b = Button(grp_info_dlgs, 'Yes-No-Cancel Question')
        def ask_yesnocancel_(*_):
            resp = ask_yesnocancel(self.shell, title='pyRAP Message Box', text='This is my first message. It can also span multiple lines. You just have to put\nnewline in the message box text.\n\nAre you OK with that?')
            msg_ok(self.shell, 'Info', 'The user clicked %s' % resp)
        b.on_select += ask_yesnocancel_
        
        b = Button(grp_info_dlgs, 'OK-Cancel Question')
        def ask_okcancel_(*_):
            resp = ask_okcancel(self.shell, title='pyRAP Message Box', text='This is my first message. It can also span multiple lines. You just have to put\nnewline in the message box text.\n\nAre you OK with that?')
            msg_ok(self.shell, 'Info', 'The user clicked %s' % resp)
        b.on_select += ask_okcancel_
        
    
    def create_list_page(self, parent):
        grp_ctxmenu = Group(parent, text='Lists')
        grp_ctxmenu.layout = CellLayout(minwidth=200, minheight=200)
        list = List(grp_ctxmenu, halign='fill', valign='fill', minheight=200, minwidth=200)
        list.items = OrderedDict([('str1', 'bla')])
    

    def create_menu_page(self, parent):
        grp_ctxmenu = Group(parent, text='Context Menus')
        grp_ctxmenu.layout = CellLayout()
        label = Label(grp_ctxmenu, text='Right-click in this label\nto open the context menu', halign='fill', valign='fill')
        label.font = label.font.modify(family='Debby', size=48)
        menu = Menu(label, popup=True)
        item1 = MenuItem(menu, index=0, push=True, text='MenuItem 1', img=Image('images/pyrap-logo.png').resize(height='32px'))
        
        def ask(*_):
            resp = ask_yesnocancel(self.shell, title='pyRAP Message Box', text='This is my first message. It can also span multiple lines. You just have to put\nnewline in the message box text.\n\nAre you OK with that?')
            out('user clicked', resp)
            
        item1.on_select += ask
        
        item2 = MenuItem(menu, index=1, check=True, text='MenuItem 2')
        item3 = MenuItem(menu, index=2, check=True, text='MenuItem 3')
        item4 = MenuItem(menu, index=5, cascade=True, text='MenuItem 4')
        submenu = Menu(item4, dropdown=True)
        item4.menu = submenu
        subitem = MenuItem(submenu, index=0, push=True, text='this is the submenu...')
        item5 = MenuItem(menu, index=4, push=True, text='MenuItem 5')
        
        label.menu = menu
        

    def create_scale_page(self, parent):
        eq = Group(parent, text='Equalizer', halign='fill', valign='fill')
        eq.layout = ColumnLayout(halign='fill', valign='fill', equalwidths=1)
        scales = []
        for _ in range(20):
            c = Composite(eq, layout=RowLayout(valign='fill', flexrows=1))
            Label(c, '+')
            s = Scale(c, valign='fill', orientation=RWT.VERTICAL)
            Label(c, '-')
            scales.append(s)
        self.mainwnd.tabseq = [self.navigation] + scales
        lower = Composite(parent)
        lower.layout = ColumnLayout(halign='fill', valign='fill', equalwidths=1, padding_right=5, hspace=10)
        
        grpleft = Group(lower, text='Balance')
        grpleft.layout = ColumnLayout(valign='fill', halign='fill', flexcols=1)
        Label(grpleft, '-')
        Scale(grpleft, halign='fill', orientation=RWT.HORIZONTAL)
        Label(grpleft, '+')
        grpright = Group(lower, text='Fader', valign='fill', halign='fill')
        grpright.layout = ColumnLayout(valign='fill', halign='fill', flexcols=1)
        Label(grpright, '-')
        Scale(grpright, halign='fill', orientation=RWT.HORIZONTAL)
        Label(grpright, '+')
        
    
    def create_canvas_page(self, parent):
        grp_ctxmenu = Group(parent, text='Canvas')
        grp_ctxmenu.layout = CellLayout(halign='fill', valign='fill')
        canvas = Canvas(grp_ctxmenu, halign='fill', valign='fill')
        context = canvas.gc
        canvas << context.draw_grid(10, 10, 'lightgrey')

        canvas << context.begin_path()
        canvas << context.rect(50, 50, 300, 100)
        canvas << context.fill_style(Color('white'))
        canvas << context.fill()
        canvas << context.linewidth(1)
        canvas << context.stroke_style(Color('black'))
        canvas << context.stroke()

        canvas << context.fill_style(Color('red'))
        canvas << context.font('Arial', 30)
        canvas << context.stroke_text("Hello World!\nThis is Awesome!", 200, 100, aligncenterx=True, aligncentery=True)

        canvas << context.begin_path()
        canvas << context.rect(50, 150, 300, 100)
        canvas << context.fill_style(Color('light grey'))
        canvas << context.fill()
        canvas << context.linewidth(1)
        canvas << context.stroke_style(Color('black'))
        canvas << context.stroke()

        canvas << context.fill_style(Color('green'))
        canvas << context.font('Arial', 30)
        canvas << context.fill_text("Hello World!\nThis is Awesome!", 60, 200, aligncenterx=False, aligncentery=True)
        canvas.draw()    
       
    
    def create_button_page(self, parent):
        grp = Group(parent, text='Push Buttons')
        grp.layout = RowLayout(halign='fill', valign='center')
        for i in range(10):
            b = Checkbox(grp, text='click-%s' % i)
            b.bind(BoolVar())
            b.badge = str(i+1)

        pushbuttons = Group(parent, layout=ColumnLayout(halign='fill', equalwidths=True))
        button = Button(pushbuttons, 'Pushbutton')
        toggle = Toggle(pushbuttons, 'Togglebutton')

    def create_browser_page(self, parent):
        grp = Group(parent, text='Browser')
        # grp.layout = GridLayout(cols=1, minheight=200, minwidth=200, flexcols=0)
        # container = Composite(grp)
        grp.layout = ColumnLayout(minheight=200, minwidth=200, flexcols=0)
        # grp.bg = 'yellow'
        # grp.bg = 'green'
        Label(grp, 'Click:', halign='center')
        browser = Button(grp, text='Open Browser', halign='center')
        browser.on_select += self.open_browser

    def create_radar_page(self, parent):
        grp = Group(parent, text='Radar')
        grp.layout = CellLayout(halign='fill', valign='fill')
        comp_pracgraph = Composite(grp)
        comp_pracgraph.layout = CellLayout(halign='fill', valign='fill')
        comp_pracgraph.bg = Color('white')

        # user-defined configuration of the number of radar levels, min and max
        # values of the respective axes, intervals (can be understood as 'acceptable range of
        # values' the respective datapoint should take), and the units of the
        # axes. If no units are given, all values are assumed to be percentages,
        # so make sure the values of the datapoints as well as min/max/interval
        # values are in [0,1]
        mycfg = {
            'w': 500,
            'h': 500,
            'levels': 6,
            'ExtraWidthX': 300
        }

        # radar_req = RadarChartRed(comp_pracgraph, opts=mycfg, legendtext='The material properties in relation to the property intervals of the requirement profile', halign='fill', valign='fill')
        radar_req = RadarChart(comp_pracgraph, opts=mycfg, legendtext='The material properties in relation to the property intervals of the requirement profile', halign='fill', valign='fill')

        # the legend title and names of the data sets (in the same order as
        # the data point lists are given)
        radar_req.addaxis('ElasticModulus', minval=150, maxval=250, unit='GPa', intervalmin=200, intervalmax=220)
        radar_req.addaxis('YieldStrength', minval=220, maxval=2500, unit='MPa', intervalmin=500, intervalmax=900)
        radar_req.addaxis('TensileStrength', minval=300, maxval=2500, unit='MPa', intervalmin=700, intervalmax=2200)
        radar_req.addaxis('CorrosionBehavior', minval=-2, maxval=2, unit='', intervalmin=-1, intervalmax=1)
        radar_req.addaxis('Hardness', minval=100, maxval=1000, unit='HV', intervalmin=200, intervalmax=700)
        radar_req.addaxis('FatigueStrength', minval=150, maxval=1000, unit='MPa', intervalmin=200, intervalmax=500)
        radar_req.addaxis('ElongationAtBreak', minval=0., maxval=1., unit='%', intervalmin=.1, intervalmax=.2)
        radar_req.addaxis('NotchImpactEnergy', minval=5, maxval=45, unit='J', intervalmin=15, intervalmax=30)

        radar_req.setdata({'test': [170, 500, 700, 0, 900, 170, .3, 15]})


    def create_cluster_page(self, parent):
        grp = Group(parent, text='Radar')
        grp.layout = CellLayout(halign='fill', valign='fill')

        comp_body = Composite(grp)
        comp_body.layout = RowLayout(halign='fill', valign='fill', flexrows=0)

        # comp_cluster = Composite(comp_body)
        # comp_cluster.layout = CellLayout(halign='fill', valign='fill')
        # comp_cluster.bg = Color('black')

        cluster = Cluster(comp_body, halign='fill', valign='fill')
        cluster.bg = Color('black')

        with open('resources/materials.json') as f:
            data = json.load(f)
            cluster.setdata(data)

        txt = Edit(comp_body, text='28Mn6', halign='fill', valign='fill')
        btn = Button(comp_body, text='Highlight', halign='fill', valign='fill')

        def highlight(*_):
            cluster.highlight(txt.text)


        btn.on_select += highlight

    def open_browser(self, data):
        dlg = Shell(title='pyRAP Browser', border=True,
                    btnclose=True, btnmax=True, resize=True, modal=False, titlebar=True)
        dlg.on_resize += dlg.dolayout
        dlg.bounds = self.mainwnd.width / 2 - 150, self.mainwnd.height / 2 - 100, 500, 300
        content = Composite(dlg.content)
        content.layout = RowLayout(halign='fill', valign='fill', flexrows=1)

        address_bar = Composite(content)
        address_bar.layout = ColumnLayout(halign='fill', valign='fill', flexcols=1)
        Label(address_bar, text='URL:')
        address = Edit(address_bar, text='http://www.tagesschau.de', message='Type your address here', halign='fill', valign='fill')
        btngo = Button(address_bar, text='Go!')
        browser = Browser(content, halign='fill', valign='fill', border=True)
        browser.url = address.text
        def load(*_):
            browser.url = address.text
        btngo.on_select += load
        dlg.dolayout()
        # current_thread().setsuspended()
        dlg.on_close.wait()
        out('browser window closed')
        
        
    def mobile(self, shell, **kwargs):
        parent = shell.content
        parent.layout.halign = 'fill'   
        parent.layout.valign = 'fill'
        scroll = ScrolledComposite(parent, vscroll=True)
        scroll.layout = CellLayout(valign='fill', halign='fill')
        container = Composite(scroll)
        container.layout = RowLayout(halign='fill', valign='top')
        for i in range(200):
            Checkbox(container, text='this is the %d-th item' % (i+1), halign='left', checked=False)
        scroll.content = container


if __name__ == '__main__':
#     pyraplog.level(pyraplog.DEBUG)
    pyrap.register_app(clazz=ControlsDemo, 
                       path='controls', 
                       name='pyRAP Controls Demo', 
                       entrypoints={'desktop': ControlsDemo.desktop},
                                    # 'mobile': ControlsDemo.mobile},
                       theme='mytheme.css',
                       setup=ControlsDemo.setup)#, default=lambda: 'mobile' if 'mobile' in pyrap.session.client.useragent else 'desktop')
    pyrap.run(admintool=True)

