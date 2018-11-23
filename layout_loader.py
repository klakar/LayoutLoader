# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LayoutLoader
                                 A QGIS plugin
 Load and modify layout templates
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-11-18
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Klas Karlsson
        email                : klaskarlsson@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
# The following two imports are probably a bit overkill...
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog and for copying the templates to local profile folder
from .layout_loader_dialog import LayoutLoaderDialog
import os.path
from qgis.core import QgsApplication, QgsProject
from distutils.dir_util import copy_tree
from random import randrange as rand


class LayoutLoader:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'LayoutLoader_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = LayoutLoaderDialog()
        # Set Layer Name line edit disabled at the start
        self.dlg.txtLayoutName.setEnabled(False)
        
        # Run the function to load templates into the dialog listWidget (probably not needed, it's called later)
        # self.loadTemplates()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Layout Loader')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'LayoutLoader')
        self.toolbar.setObjectName(u'LayoutLoader')
        
        # Connect signals from the dialog to functions in this file
        self.dlg.listWidget.itemClicked.connect(self.suggestLayoutName)
        self.dlg.btnAddMore.clicked.connect(self.addMoreTemplates)
        
        # Testing context menu
        self.dlg.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dlg.listWidget.customContextMenuRequested.connect(self.listMenu)
        
        
    # Load print layout templates from profile template folder to listWidget in plugin dialogue
    def loadTemplates(self):
    	  self.dlg.listWidget.clear()
    	  profile_dir = QgsApplication.qgisSettingsDirPath()
    	  templates_dir = os.path.join(profile_dir,'composer_templates')
    	  
    	  # Does the composer_templates folder exist? Otherwise create it.
    	  if os.path.isdir(templates_dir) == False:
    	      os.mkdir(templates_dir)
    	  
    	  # Search the templates folder and add files to templates list and sort it
    	  templates = [f.name for f in os.scandir(templates_dir) if f.is_file() ]
    	  templates.sort()
    	  
    	  # Get the project file name and if it exist the project title. Use for Title suggestion
    	  project_file_name = QFileInfo(QgsProject.instance().fileName()).baseName()
    	  project_title = QgsProject.instance().title()
    	  if project_title == '':
    	  	  project_title = project_file_name
    	  self.dlg.txtMapTitle.setText(project_title)
    	  
    	  # Add all the templates from the list to the listWidget
    	  for template in templates:
    	  	  filename, extension = os.path.splitext(template) 
    	  	  if extension == '.qpt':
    	  	  	  self.dlg.listWidget.addItem(filename)
    	  	  
    # List of templates context menu. This is how templates can be deleted
    def listMenu(self, position):
    	  self.dlg.txtLayoutName.setEnabled(False)
    	  indexes = self.dlg.listWidget.selectedIndexes()
    	  if indexes:
    	     menu = QMenu()
    	     menu.addAction(self.tr('Delete Template File'))
    	     # menu.addAction(self.tr('Future context menu option'))
         
    	     menu_choice = menu.exec_(self.dlg.listWidget.viewport().mapToGlobal(position))
    	  
    	     try:
    	     	  if menu_choice.text() == 'Delete Template File':
    	  	       template_name = self.dlg.listWidget.selectedItems()[0].text()
    	  	       template_path = os.path.join(QgsApplication.qgisSettingsDirPath(),'composer_templates',template_name + '.qpt')
    	  	       if os.path.exists(template_path):
    	  	  	       os.remove(template_path)
    	  	  	       self.loadTemplates()
    	  	  	       self.dlg.txtLayoutName.setText('{} - Deleted'.format(template_name))
    	  	  	  
    	  	  	  # if menu_choice.text() == 'Future context menu option':
    	  	  	  	  # do something
    	  	  	  	  
    	     except:
    	     	  pass
    	  
  	  
    # Add templates and resources from plugin to user profile (triggers on dialog button clicked signal)
    # Somehow a lot of QMessageBox's are generated.
    def addMoreTemplates(self):
    	  are_you_sure = self.tr('This will add Templates and resources like SVG files and script functions to your QGIS profile.\n\n')
    	  are_you_sure += self.tr('Do you want to OVERWRITE any existing files with the same filenames?')
    	  addMoreBox = QMessageBox()
    	  addMoreBox.setIcon(QMessageBox.Question)
    	  addMoreBox.setWindowTitle(self.tr('Add Templates from Plugin'))
    	  addMoreBox.setText(are_you_sure)
    	  more_information = self.tr('If you answer \'No\', no current files will be overwritten, but new files will be copied to their location.\n\n')
    	  more_information += self.tr('If you answer \'Yes\' any current files that you have manually modified, will be overwritten with the new ones from the plugin.\n')
    	  more_information += self.tr('This should be safe if you haven\'t modified any plugin templates and kept the original filename.\n\n')
    	  more_information += self.tr('If you \'Cancel\' No changes to your QGIS profile are made!\n\n')
    	  more_information += self.tr('Some template functions will require QGIS to be restarted before working properly.')
    	  addMoreBox.setDetailedText(more_information)
    	  addMoreBox.setStandardButtons(QMessageBox.Cancel|QMessageBox.No|QMessageBox.Yes)
    	  
    	  button_pressed = addMoreBox.exec_()
    	  
    	  # Paths to source files and qgis profile directory
    	  source_profile = os.path.join(self.plugin_dir, 'profile')
    	  profile_home = QgsApplication.qgisSettingsDirPath()

    	  # The acutal "copy" with or without overwrite (update)
    	  if button_pressed == QMessageBox.Yes:
    	  	  copy_tree(source_profile, profile_home)
    	  	  self.loadTemplates()
    	  elif button_pressed == QMessageBox.No:
    	  	  copy_tree(source_profile, profile_home, update=1)
    	  	  self.loadTemplates()
    	  
    	  
    # Use selected item from listWidget and any Map Title text to suggest new layout name (triggers on listWidget itemClicked signal)
    def suggestLayoutName(self):
    	  self.dlg.txtLayoutName.setEnabled(True)
    	  layout_name_string = self.dlg.listWidget.currentItem().text()
    	  if self.dlg.txtMapTitle != '':
    	  	  layout_name_string += ' ' + self.dlg.txtMapTitle.text()
    	  self.dlg.txtLayoutName.setText(layout_name_string)
    	     
    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('LayoutLoader', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/layout_loader/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Layout Loader'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Layout Loader'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    # Python function that do the main work of setting up the print layout
    # The code in the function can work stand alone if you use the commented variables and edit their values
    def layoutLoader(self, template_source, layout_name, title_text):
        """ Generate the layout """
        from qgis.core import (QgsProject,
                       QgsPrintLayout,
                       QgsReadWriteContext)
        from qgis.utils import iface
        from PyQt5.QtXml import QDomDocument

        #template_source = '/home/user/Document/Template.qpt'
        #layout_name = 'NewLayout'
        #title_text = 'New Title'
        
        # Create objects lm = layout manager, l = print layout
        lm = QgsProject.instance().layoutManager()
        l = QgsPrintLayout(QgsProject.instance())
        l.initializeDefaults()
        
        # Load template file and load it into the layout (l)
        template_file = open(template_source, 'r+', encoding='utf-8')
        template_content = template_file.read()
        template_file.close()
        document = QDomDocument()
        document.setContent(template_content)
        context = QgsReadWriteContext()
        l.loadFromTemplate(document, context)
        
        # Give the layout a name (must be unique)
        l.setName(layout_name)
        
        # Get current canvas extent and apply that to all maps (items) in layout
        # Replace any text "{{title}}" in any layout label with the dialog Title text
        canvas = iface.mapCanvas()
        for item in l.items():
            if item.type()==65639: # Map
                item.zoomToExtent(canvas.extent())
            if item.type()==65641: # Label
                item.setText(item.text().replace('{{title}}',title_text))
        
        # Add layout to layout manager
        l.refresh()
        lm.addLayout(l)
        
        # Open and show the layout in designer
        try:
           iface.openLayoutDesigner(l)
        except:
           oopsBox = QMessageBox()
           oopsBox.setIcon(QMessageBox.Warning)
           oopsBox.setText(self.tr('Ooops. Something went wrong. Trying to open the generated layout ({}) returned errors.'.format(l.name())))
           oopsBox.setWindowTitle(self.tr('Layout Loader'))
           oopsBox.exec_()
           
    # Does a layout already exist
    def layout_exists(self, layout_name):
    	  lm = QgsProject.instance().layoutManager()
    	  layouts = []
    	  for l in lm.layouts():
    	  	  layouts.append(l.name())
    	  if layout_name in layouts:
    	     return sum(layout_name in s for s in layouts)
    	  else:
    	     return 0


    def run(self):
        """Run method that performs all the real work"""
        # This loads the dialog with templates (again) TODO check when it's best to do this
        self.loadTemplates()
        
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed TODO: probably need something to happen when pressing "cancel" too.
        if result:
            # Get values from dialog list and text fields
            try:
               template_name = self.dlg.listWidget.currentItem().text()
            except:
            	template_name = ''
            layout_name = self.dlg.txtLayoutName.text()
            # Generate random layout name for blank names (REDUNDANT?)
            if layout_name == '':
               layout_name = 'Layout'
            
            # Add function to test the layout name so that it doesn't exist. If it does handle the exception
            
            map_title = self.dlg.txtMapTitle.text()
            profile_dir = QgsApplication.qgisSettingsDirPath()
            # create the template item selected full path (assuming extension is lower case)
            template_source = os.path.join(profile_dir,'composer_templates',template_name + '.qpt')
            
            # Call function to generate layout, renaming duplicate layout names
            layout_count = self.layout_exists(layout_name) # How many layouts with the same name exist already
            if layout_count >> 0:
               name = layout_name.split('_')
               if layout_count >> 1:
                  layout_name = '_'.join(name) + '_' + str(layout_count + 1)
               else:
               	layout_name += '_2'
            try:
               if os.path.exists(template_source):
                  self.layoutLoader(template_source, layout_name, map_title) # CALLING MAIN LAYOUT LOADING PROCESS
               else:
                  infoBox = QMessageBox()
                  infoBox.setIcon(QMessageBox.Information)
                  infoBox.setText(self.tr('You must select a valid template from the list.'))
                  infoBox.setWindowTitle(self.tr('Layout Loader'))
                  infoBox.exec_()
            except:
               oopsBox = QMessageBox()
               oopsBox.setIcon(QMessageBox.Warning)
               oopsBox.setText(self.tr('Ooops. Something went wrong opening ({}). But I don\'t know what?'.format(layout_name)))
               oopsBox.setWindowTitle(self.tr('Layout Loader'))
               oopsBox.setDetailedText('Map Title: {}\nTemplate Name: {}\nLayout Name: {}\nProfile Directory: {}\nTemplate Source: {}\nLayout Count: {}' % (map_title, template_name, layout_name, profile_dir, template_source, layout_count))
               oopsBox.exec_()
               
            # Clean up
            self.dlg.txtLayoutName.clear()
            self.dlg.txtLayoutName.setEnabled(False)
            self.dlg.txtMapTitle.clear()
            self.dlg.txtMapTitle.setFocus()
