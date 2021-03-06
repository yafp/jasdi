#!/usr/bin/env python
"""main script of jasdi."""

# ------------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------------
from __future__ import print_function
import os  # to walk directories
import datetime  # to generate timestamps
import webbrowser  # for opening urls
import wx  # wxpython

# from . import helpers


# ------------------------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------------------------
APP_NAME = "jasdi"
APP_DESC = "just a simple directory indexer"
VERSION = "0.0.1"
AUTHOR = "Florian Poeck"
APP_URL = "https://www.github.com/yafp/jasdi"
APP_URL_SHORT = "www.github.com/jasdi"

SUFFIXES = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


# ------------------------------------------------------------------------------
# VAR
# ------------------------------------------------------------------------------
child_dir = False


class DirectoryIndexer(wx.Frame):
    """UI class."""

    def __init__(self, parent, title):
        """Init the app."""
        super(DirectoryIndexer, self).__init__(parent, title=title, size=(480, 620))

        self.SetMinSize(self.GetSize())

        # define window icon
        icon_path = '../assets/logo.ico'
        self.SetIcon(wx.Icon(icon_path))

        self.init_ui()
        self.Centre()
        self.Show()


    def init_ui(self):
        """Initialize the UI."""
        # p = wx.Panel(self)

        self.SetSizeHintsSz(wx.Size(480, 620), wx.DefaultSize)

        # menubar
        #
        self.menubar = wx.MenuBar(0)
        # menu: file
        self.menu_file = wx.Menu()
        self.menuitem_exit = wx.MenuItem(self.menu_file, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_file.AppendItem(self.menuitem_exit)
        self.menubar.Append(self.menu_file, u"File")
        # menu: help
        self.menu_help = wx.Menu()
        self.menuitem_about = wx.MenuItem(self.menu_help, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_help.AppendItem(self.menuitem_about)
        self.menuitem_doc = wx.MenuItem(self.menu_help, wx.ID_ANY, u"Documentation", wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_help.AppendItem(self.menuitem_doc)
        self.menubar.Append(self.menu_help, u"Help")

        self.SetMenuBar(self.menubar)

        # Create Sizers
        sizer_main = wx.BoxSizer(wx.VERTICAL)  # main sizer
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)  # sizer for row 1
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)  # sizer for row 2
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)  # sizer for row 3
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)  # sizer for row 4
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)  # sizer for row 4

        # Source: Label
        self.statictext_source = wx.StaticText(self, wx.ID_ANY, u"Source", wx.DefaultPosition, wx.DefaultSize, 0)
        self.statictext_source.SetForegroundColour('gray')
        self.statictext_source.Wrap(-1)
        sizer_1.Add(self.statictext_source, 0, wx.ALL, 20)

        # Source: dir picker
        self.dirpicker_source = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a source folder", wx.Point(0, 0), wx.DefaultSize, wx.DIRP_DEFAULT_STYLE | wx.DIRP_DIR_MUST_EXIST)
        self.dirpicker_source.SetToolTipString(u"Select the source folder here")
        sizer_1.Add(self.dirpicker_source, 0, wx.ALL | wx.EXPAND, 20)

        # Target: label
        self.statictext_target = wx.StaticText(self, wx.ID_ANY, u"Target", wx.DefaultPosition, wx.DefaultSize, 0)
        self.statictext_target.SetForegroundColour('gray')
        self.statictext_target.Wrap(-1)
        sizer_2.Add(self.statictext_target, 0, wx.ALL, 20)

        # Target: dir picker
        self.dirpicker_target = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a target folder", wx.Point(1, 0), wx.DefaultSize, wx.DIRP_DEFAULT_STYLE | wx.DIRP_DIR_MUST_EXIST)
        self.dirpicker_target.SetToolTipString(u"Select the target folder here")
        sizer_2.Add(self.dirpicker_target, 0, wx.ALL, 20)

        # Button: start
        self.button_start = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_3.Add(self.button_start, -1, wx.ALL, 20)  # -1 for width

        # log
        self.textctrl_log = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(100, 200), wx.TE_MULTILINE | wx.TE_READONLY)
        sizer_4.Add(self.textctrl_log, -1, wx.ALL, 20)  # -1 for width

        # checkbox
        self.cb_open_result = wx.CheckBox(self, label='Open index after generation', pos=(20, 20))
        self.cb_open_result.SetValue(True)
        sizer_5.Add(self.cb_open_result, -1, wx.ALL, 20)  # -1 for width

        # Statusbar
        self.statusbar_main = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)
        self.statusbar_main.SetForegroundColour('gray')
        self.statusbar_main.SetStatusText('Ready')

        # Add all sizers to main sizer
        sizer_main.Add(sizer_1, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizer_main.Add(sizer_2, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizer_main.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_main.Add(sizer_4, 0, wx.EXPAND, 0)
        sizer_main.Add(sizer_5, 0, wx.EXPAND, 0)

        # Set the main sizer
        self.SetAutoLayout(True)
        self.SetSizer(sizer_main)
        self.Layout()

        # Connect Events
        self.Bind(wx.EVT_MENU, self.on_exit, id=self.menuitem_exit.GetId())
        self.Bind(wx.EVT_MENU, self.on_about, id=self.menuitem_about.GetId())
        self.Bind(wx.EVT_MENU, self.on_doc, id=self.menuitem_doc.GetId())
        self.button_start.Bind(wx.EVT_BUTTON, self.on_start)


    def on_exit(self, event):
        """Close the application."""
        self.Close()


    def on_about(self, event):
        """Handle menu click on_about."""
        info = wx.AboutDialogInfo()
        info.Name = APP_NAME
        info.Version = VERSION
        # info.Copyright = "(C) 2008 Python Geeks Everywhere"
        info.Description = (
            "Just a simple directory indexer.\n\n"
            "Gets a source directory and generates a browseable html index for the entire content"
            )
        info.WebSite = (APP_URL, APP_URL_SHORT)
        info.Developers = AUTHOR,
        info.License = ("GPL3")

        # Show the wx.AboutBox
        wx.AboutBox(info)


    def on_doc(self, event):
        """Open online documentation."""
        alink = APP_URL
        new = 2
        webbrowser.open(alink, new=new)


    def on_start(self, event):
        """Pressing Start button."""
        self.validate_user_input()


    def get_size(self, start_path='.'):
        """Get size of folder."""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        total_size = self.humansize(total_size)
        return total_size


    def humansize(self, nbytes):
        """Make sizes human readable."""
        i = 0
        while nbytes >= 1024 and i < len(SUFFIXES)-1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, SUFFIXES[i])


    def get_file_type_icon(self, extension):
        """Get a file extension and return a FontAwesome icon code."""
        if any(extension in item for item in [".txt"]):  # txt
            icon_code = "<i class='fas fa-file-alt'></i>"
        elif any(extension in item for item in [".h", ".cpp"]):  # code
            icon_code = "<i class='fas fa-file-code'></i>"
        elif any(extension in item for item in [".zip", ".7z"]):  # archive
            icon_code = "<i class='fas fa-file-archive'></i>"
        elif any(extension in item for item in [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".svg"]):  # image
            icon_code = "<i class='fas fa-file-image'></i>"
        elif any(extension in item for item in [".mp3", ".ogg", ".wav", ".aiff", "aac", ".wma", ".flac"]):  # audio
            icon_code = "<i class='fas fa-file-audio'></i>"
        elif any(extension in item for item in [".mpg", ".avi", ".webm", ".mkv", ".vob", ".mts", ".m2ts", ".wmv", ".mp4", ".mpeg", ".flv"]):  # video
            icon_code = "<i class='fas fa-file-video'></i>"
        elif extension == ".pdf":  # pdf
            icon_code = "<i class='fas fa-file-pdf'></i>"
        elif any(extension in item for item in [".doc", ".docx"]):  # doc
            icon_code = "<i class='fas fa-file-word'></i>"
        elif any(extension in item for item in [".xls", ".xlsx"]):  # excel
            icon_code = "<i class='fas fa-file-excel'></i>"
        elif any(extension in item for item in [".ppt", ".pptx"]):  # powerpoint
            icon_code = "<i class='fas fa-file-powerpoint'></i>"
        else:  # default
            icon_code = "<i class='fas fa-file'></i>"
        return icon_code


    def append_text_to_ui_log(self, text):
        """Append text to UI log."""
        self.textctrl_log.AppendText(text)


    def validate_user_input(self):
        """Validate the user input before starting the indexing."""
        # source
        source_path = self.dirpicker_source.GetPath()
        if source_path == "":
            # display error dialog
            message = "Please define a source directory and try again."
            caption = "Error: missing source"
            dlg = wx.MessageDialog(self, message, caption, wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            print(caption)
        else:
            print("Source: " + source_path)

        # target
        target_path = self.dirpicker_target.GetPath()
        if target_path == "":
            # display error dialog
            message = "Please define a target directory and try again."
            caption = "Error: missing target"
            dlg = wx.MessageDialog(self, message, caption, wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            print(caption)
        else:
            print("Target: " + target_path)

        if(source_path != "") and (target_path != ""):
            # source_path: add trailing / if needed
            if source_path.endswith("/"):
                print("source_path ok")
            else:
                source_path = source_path + "/"

            # target_path: add trailing / if needed
            if target_path.endswith("/"):
                print("target path ok")
            else:
                target_path = target_path + "/"

            # adjust target_path to be date-specific
            timestamp = datetime.datetime.today().strftime('%Y%m%d-%H%M%S')
            target_path = target_path + timestamp + "/"
            os.mkdir(target_path)  # create target path directory

            # start index generation
            self.start_indexing(source_path, target_path)


    def start_indexing(self, source_path, target_path):
        """Start the indexing process."""
        # update statusbar
        self.statusbar_main.SetStatusText('Started index generation')

        # disable the start button
        self.button_start.Disable()

        # index the source
        self.append_text_to_ui_log("Indexing: " + source_path + "\n")
        self.make_single_index(source_path, target_path)

        # enable the start button
        self.button_start.Enable()

        # display info dialog
        message = 'Finished indexing: ' + source_path
        # caption = "Finished indexing"
        # dlg = wx.MessageDialog(self, message, caption, wx.OK | wx.ICON_INFORMATION)
        # dlg.ShowModal()
        # dlg.Destroy()
        print("\n" + message)

        # update statusbar
        self.statusbar_main.SetStatusText(message)

        # update log
        self.append_text_to_ui_log(message + "\n")

        # open result if checkbox is True
        if self.cb_open_result.GetValue() is True:
            alink = target_path + "index.html"
            new = 2
            webbrowser.open(alink, new=new)


    def make_single_index(self, current_path, target_path):
        """Create index for single directory."""
        print("Creating index for: " + current_path + " in " + target_path + "index.html")

        # update ui log
        self.append_text_to_ui_log("Processing: " + current_path)

        # update statusbar
        self.statusbar_main.SetStatusText('Processing ' + current_path)

        # create target file
        file = open(target_path + "index.html", "w")

        # create lists for files & directories
        cur_sub_directories = []  # directories
        cur_sub_directories_sizes = []
        cur_file_name = []  # file names
        cur_file_typs = []  # file type
        cur_file_sizes = []  # file sizes

        for item in os.listdir(current_path):

            # folder
            if os.path.isdir(os.path.join(current_path, item)):
                # get folder size
                folder_size = self.get_size(current_path+item)
                # append to related list
                cur_sub_directories.append(item)
                cur_sub_directories_sizes.append(folder_size)

            # file
            if os.path.isfile(os.path.join(current_path, item)):
                # get file informations
                name, ext = os.path.splitext(item)
                size = self.humansize(os.path.getsize(current_path+item))
                # append to related lists
                cur_file_name.append(name)
                cur_file_typs.append(ext)
                cur_file_sizes.append(size)

        # sort lists
        # cur_sub_directories = sorted(cur_sub_directories, key=str.lower)

        # html head
        #
        file.write("<!DOCTYPE html>\n")
        file.write("<html lang='en'>\n")
        file.write("<head>\n")
        file.write("<meta charset='UTF-8'>")
        file.write("<meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>\n")
        file.write("<meta name='description' content=''>\n")
        file.write("<meta name='author' content=''>\n")
        file.write("<title>" + APP_NAME + "</title>\n")
        file.write("<link rel='shortcut icon'' type='image/png'' href='https://raw.githubusercontent.com/yafp/jasdi/master/assets/jasdi.ico'/>\n")
        # jquery
        file.write("<script src='https://code.jquery.com/jquery-3.3.1.min.js'></script>\n")
        # bootstrap
        file.write("<link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css' integrity='sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO' crossorigin='anonymous'>\n")
        file.write("<script src='https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js' integrity='sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy' crossorigin='anonymous'></script>\n")
        # font awesome
        file.write("<link rel='stylesheet' href='https://use.fontawesome.com/releases/v5.3.1/css/all.css' integrity='sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU' crossorigin='anonymous'>\n")
        # datatable
        file.write("<link rel='stylesheet' href='https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css'>")
        file.write("<script src='https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js'></script>")
        file.write("<script>$(document).ready(function() {$('#example').DataTable();} );</script>")
        file.write("</head>\n")

        # html body
        #
        file.write("<body>\n")

        # header
        file.write("<nav class='navbar navbar-expand-lg navbar-dark bg-dark static-top'>")
        file.write("<div class='container'>")
        file.write("<a class='navbar-brand' href='index.html'><i class='fas fa-sitemap'></i> " + APP_NAME + " <small>... " + APP_DESC + "</small></a>")
        file.write("<button class='navbar-toggler' type='button' data-toggle='collapse' data-target=''#navbarResponsive' aria-controls='navbarResponsive' aria-expanded='false' aria-label='Toggle navigation'>")
        file.write("<span class='navbar-toggler-icon'></span>")
        file.write("</button>")
        file.write("<div class='collapse navbar-collapse' id='navbarResponsive'>")
        file.write("<ul class='navbar-nav ml-auto'>")
        # home
        file.write("<li class='nav-item active'>")
        file.write("<a class='nav-link' href='index.html'><i class='fas fa-home'></i> Home")
        file.write("<span class='sr-only'>(current)</span>")
        file.write("</a>")
        file.write("</li>")
        # github
        file.write("<li class='nav-item'>")
        file.write("<a class='nav-link' href='" + APP_URL + "'><i class='fab fa-github-square'></i> GitHub</a>")
        file.write("</li>")
        # issues
        file.write("<li class='nav-item'>")
        file.write("<a class='nav-link' href='" + APP_URL + "/issues'><i class='fas fa-bug'></i> Issues</a>")
        file.write("</li>")
        file.write("</ul>")
        file.write("</div>")
        file.write("</div>")
        file.write("</nav>")

        # content
        #
        # bootstrap content container
        file.write("<main role='main' class='container'>")

        file.write("<br><h4>Source: <span class='badge badge-secondary'>"+current_path+"</span> contains <span class='badge badge-secondary'>" + str(len(cur_sub_directories)) + "</span> directories and <span class='badge badge-secondary'>" + str(len(cur_file_name)) + "</span> file(s)</h4>\n")

        '''
        # breadcrumb
        <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="#">Home</a></li>
        <li class="breadcrumb-item active" aria-current="page">Library</li>
        </ol>
        </nav>
        '''

        # adding a backlink to upper dir for all subdir indexes
        global child_dir
        if child_dir is True:
            file.write("<a href='../index.html'><button type='button' class='btn btn-secondary'>Back</button></a><br><br>")

        file.write("<div id='content'>\n")

        #  table head
        #
        file.write("<table id='example' class='display' style='width:100%'>\n")
        file.write("<thead>")
        file.write("<th>Icon</th>")
        file.write("<th>Name</th>")
        file.write("<th>Type</th>")
        file.write("<th>Size</th>")
        file.write("</thead>\n")

        # table body
        #
        file.write("<tbody>\n")

        # create table row for each single sub-directories (as links)
        if cur_sub_directories:  # if the list contains items
            for x in xrange(len(cur_sub_directories)):
                file.write("<tr>")
                file.write("<td><i class='fas fa-folder'></i></td>")  # typ
                file.write("<td><a href='" + cur_sub_directories[x] + "/index.html'>" + cur_sub_directories[x] + "</a></td>")
                file.write("<td>Directory</td>")  # typ
                file.write("<td>" + str(cur_sub_directories_sizes[x]) + "</td>")  # size
                file.write("</tr>\n")

        # create table row for each single file
        if cur_file_name:  # if the list contains items
            for x in xrange(len(cur_file_name)):
                # define font awesome icon for current filetype
                icon_code = self.get_file_type_icon(cur_file_typs[x])

                file.write("<tr>")
                file.write("<td>" + icon_code + "</td>")  # icon
                file.write("<td>" + cur_file_name[x] + "</td>")  # name of file
                file.write("<td>" + cur_file_typs[x] + "</td>")  # name of file
                file.write("<td>" + str(cur_file_sizes[x]) + "</td>")  # size
                file.write("</tr>\n")

        file.write("</tbody>\n")
        file.write("</table>\n")
        file.write("</div>\n")

        # Footer
        #
        file.write("<footer class='page-footer font-small blue pt-4'>")
        file.write("<div class='footer-copyright text-center py-3'>by <a href='" + APP_URL + "'><i class='fas fa-sitemap'></i> " + APP_NAME + "</a> - " + APP_DESC + " - Version: (" + VERSION + ")</div>")
        file.write("</footer>")
        file.write("</html>\n")

        # close output file
        file.close()

        # update log
        self.append_text_to_ui_log(" ... done.\n")

        # change child_dir to true (backlinks only on child-pages)
        child_dir = True

        # start new index creation process for all other sub-dirs
        for x in cur_sub_directories:
            new_current_path = current_path + x + "/"  # new source_path
            new_target_path = target_path + x + "/"  # new target path
            os.mkdir(new_target_path)  # create new target path

            # start indexing for new current dir
            self.make_single_index(new_current_path, new_target_path)

        # Finished all tasks
        print("Finished index generation for: " + current_path)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
app = wx.App()
DirectoryIndexer(None, title=APP_NAME)
app.MainLoop()
