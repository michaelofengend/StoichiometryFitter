#!/usr/bin/env python
# -*- coding: US-ASCII -*-
#
# generated by wxGlade 0.6.8 on Thu Mar  6 15:07:47 2014
#

# TODO Output quant from minerals and delta.
# TODO Subphase reporter.
# TODO Add and compute errorbars

import wx
from numpy import *
import os
import ReportResults
from collections import OrderedDict
import MyPython

# begin wxGlade: dependencies
import gettext
# end wxGlade

import PhysicsBasics as pb
from MyPython import *
import CountsToQuant
import PhaseFit

wx.SystemOptions.SetOption('mac.listctrl.always_use_generic', '1')

# begin wxGlade: extracode
ID_SAVEINPUTS = 1000
from wx.lib.mixins.listctrl import TextEditMixin

class EditableTextListCtrl(wx.ListCtrl, TextEditMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        TextEditMixin.__init__(self)
# end wxGlade

    EditableColumns = None
    def SetEditableColumns(self, ColNums=None):
        self.EditableColumns = ColNums

    # This opens when the user edits an item in the ListCtrl.
    def OpenEditor(self, col, row):
        # IF this is not an editable ListCtrl, then EditableColumns == None.  Nothing to do here in this case.  Defer
        #  to super.
        if self.EditableColumns == None:
            print 'Warning: It appears you are using an EditableTextListCtrl where there are no editable columns.'
            return

        # The only editable entry is column 1 (counts for a given element.)
        if col in self.EditableColumns:
            super(EditableTextListCtrl, self).OpenEditor(col, row)




class MyMenuBar(wx.MenuBar):
    def __init__(self, *args, **kwds):
        # Content of this block not found. Did you rename this class?
        pass

    def __set_properties(self):
        # Content of this block not found. Did you rename this class?
        pass

    def __do_layout(self):
        # Content of this block not found. Did you rename this class?
        pass

# end of class MyMenuBar
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        # Menu Bar
        self.MainMenu = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_OPEN, _("&Open Inputs..."), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(ID_SAVEINPUTS, _("Save &Inputs..."), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_SAVE, _("&Save Results..."), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_ABOUT, _("&About"), "", wx.ITEM_NORMAL)
        self.MainMenu.Append(wxglade_tmp_menu, _("File"))
        self.SetMenuBar(self.MainMenu)
        # Menu Bar end
        self.panel_4 = wx.Panel(self, wx.ID_ANY)
        self.ElementsListCtrl = EditableTextListCtrl(self.panel_4, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_EDIT_LABELS | wx.LC_SINGLE_SEL | wx.SUNKEN_BORDER | wx.FULL_REPAINT_ON_RESIZE)
        self.rdioInputType = wx.RadioBox(self.panel_4, wx.ID_ANY, _("Input Type"), choices=[_("Counts"), _("At %"), _("Wt %"), _("Ox Wt %")], majorDimension=0, style=wx.RA_SPECIFY_ROWS)
        self.btnReset = wx.Button(self.panel_4, wx.ID_ANY, _("Reset"))
        self.panel_5 = wx.Panel(self, wx.ID_ANY)
        self.PhasesListCtrl = wx.ListCtrl(self.panel_5, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.panel_2 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.chkArbAbsCorrection = wx.CheckBox(self.panel_1, wx.ID_ANY, "")
        self.comboArbAbsCorrection = wx.ComboBox(self.panel_1, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.sizer_5_copy_staticbox = wx.StaticBox(self.panel_1, wx.ID_ANY, _("Arbitrary absorption"))
        self.chkAbsCorr = wx.CheckBox(self.panel_1, wx.ID_ANY, "")
        self.txtAbsCorr = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, _("g/cm3 * nm"))
        self.sizer_3_staticbox = wx.StaticBox(self.panel_1, wx.ID_ANY, _("TEM Thickness Correction"))
        self.chkKfacs = wx.CheckBox(self.panel_1, wx.ID_ANY, "")
        self.comboKfacs = wx.ComboBox(self.panel_1, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.sizer_4_staticbox = wx.StaticBox(self.panel_1, wx.ID_ANY, _("Apply k-factors for:"))
        self.chkOByStoichiometry = wx.CheckBox(self.panel_1, wx.ID_ANY, "")
        self.comboStoich = wx.ComboBox(self.panel_1, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.sizer_5_staticbox = wx.StaticBox(self.panel_1, wx.ID_ANY, _("Oxygen by stoichiometry?"))
        self.btnGo = wx.Button(self.panel_1, wx.ID_ANY, _("Go!"))
        self.panel_3 = wx.Panel(self.panel_1, wx.ID_ANY)
        self.txtOutput = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSaveInputs, id=ID_SAVEINPUTS)
        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_RADIOBOX, self.OnInputType, self.rdioInputType)
        self.Bind(wx.EVT_BUTTON, self.OnReset, self.btnReset)
        self.Bind(wx.EVT_CHECKBOX, self.OnStoichSelect, self.chkArbAbsCorrection)
        self.Bind(wx.EVT_COMBOBOX, self.OnDetectorSelect, self.comboArbAbsCorrection)
        self.Bind(wx.EVT_CHECKBOX, self.OnStoichSelect, self.chkOByStoichiometry)
        self.Bind(wx.EVT_COMBOBOX, self.OnStoichSelect, self.comboStoich)
        self.Bind(wx.EVT_BUTTON, self.OnGo, self.btnGo)
        # end wxGlade

        # First verify that we are running in the home directory (i.e. we should be in the directory containing
        # StoichiometryFitter.py
        #import pdb
        #pdb.set_trace()
        if not os.path.isfile(os.path.join(os.getcwd(), 'StoichiometryFitter.py')):
            MyPython.ReportError('Please ensure the running directory is the directory containing StoichiometryFitter'
                                 '.py')

        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)

        # Make sure the window never gets too small to see the controls.
        self.SetMinSize((650, 500))

        # Set up the initial conditions for the frame.
        self.InitControls()

        # Catch the frame closing event so we can ask if we want to save.
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Layout()

    def OnClose(self, evt):
        """OnClose(self, evt): Ask the user if he wants to save before closing.  Not yet implemented."""
        # it = self.ElementsListCtrl.GetItem(0,1)
        # print it.GetText()
        self.Destroy()

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(_("Stoichiometry Fitter"))
        self.SetSize((1118, 703))
        self.ElementsListCtrl.SetMinSize((200, 100))
        self.rdioInputType.SetMinSize((200,120))
        self.rdioInputType.SetSelection(0)
        self.btnReset.SetMinSize((200,20))
        self.panel_4.SetMinSize((200, -1))
        self.PhasesListCtrl.SetMinSize((300, 300))
        self.panel_5.SetMinSize((305,300))
        self.chkArbAbsCorrection.SetValue(1)
        self.chkKfacs.Enable(False)
        self.chkOByStoichiometry.SetValue(1)
        self.panel_1.SetMinSize((250, -1))
        self.txtOutput.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.FlexGridSizer(1, 1, 0, 0)
        sizer_2 = wx.FlexGridSizer(1, 4, 0, 0)
        grid_sizer_1 = wx.FlexGridSizer(6, 1, 0, 0)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_5_staticbox.Lower()
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.HORIZONTAL)
        self.sizer_4_staticbox.Lower()
        sizer_4 = wx.StaticBoxSizer(self.sizer_4_staticbox, wx.HORIZONTAL)
        self.sizer_3_staticbox.Lower()
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.HORIZONTAL)
        self.sizer_5_copy_staticbox.Lower()
        sizer_5_copy = wx.StaticBoxSizer(self.sizer_5_copy_staticbox, wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.FlexGridSizer(2, 1, 0, 0)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9.Add(self.ElementsListCtrl, 0, wx.ALL | wx.EXPAND, 2)
        sizer_6.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_10.Add(self.rdioInputType, 0, wx.EXPAND, 0)
        sizer_6.Add(sizer_10, 0, wx.EXPAND, 0)
        sizer_8.Add(self.btnReset, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 2)
        sizer_6.Add(sizer_8, 0, wx.EXPAND, 0)
        self.panel_4.SetSizer(sizer_6)
        sizer_6.AddGrowableRow(0)
        sizer_2.Add(self.panel_4, 0, wx.EXPAND, 0)
        sizer_11.Add(self.PhasesListCtrl, 0, wx.ALL | wx.EXPAND, 2)
        self.panel_5.SetSizer(sizer_11)
        sizer_2.Add(self.panel_5, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.panel_2, 1, wx.EXPAND, 0)
        sizer_5_copy.Add(self.chkArbAbsCorrection, 0, 0, 0)
        sizer_5_copy.Add(self.comboArbAbsCorrection, 0, wx.ALL | wx.EXPAND, 2)
        grid_sizer_1.Add(sizer_5_copy, 1, wx.EXPAND, 0)
        sizer_3.Add(self.chkAbsCorr, 0, 0, 0)
        sizer_3.Add(self.txtAbsCorr, 0, wx.EXPAND, 0)
        sizer_3.Add(self.label_1, 0, 0, 0)
        grid_sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_4.Add(self.chkKfacs, 0, 0, 0)
        sizer_4.Add(self.comboKfacs, 0, wx.ALL | wx.EXPAND, 2)
        grid_sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_5.Add(self.chkOByStoichiometry, 0, 0, 0)
        sizer_5.Add(self.comboStoich, 0, wx.ALL | wx.EXPAND, 2)
        grid_sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_7.Add(self.btnGo, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 2)
        grid_sizer_1.Add(sizer_7, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.panel_3, 1, wx.EXPAND, 0)
        self.panel_1.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableRow(0)
        grid_sizer_1.AddGrowableRow(5)
        grid_sizer_1.AddGrowableCol(0)
        sizer_2.Add(self.panel_1, 0, wx.EXPAND, 0)
        sizer_2.Add(self.txtOutput, 1, wx.ALL | wx.EXPAND, 2)
        sizer_2.AddGrowableRow(0)
        sizer_2.AddGrowableCol(3)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.AddGrowableRow(0)
        sizer_1.AddGrowableCol(0)
        self.Layout()
        # end wxGlade

    def LoadStoichiometryFile(self):
        # Load the stoichiometry list.  It's two column.  First is the element name.  Second is the atom's charge.
        # The converter removes ensures we have floats.
        try:
            self.Stoich = genfromtxt('ConfigData/Stoich ' + self.comboStoich.StringSelection + '.csv', dtype=None,
                                     comments='#', delimiter=',', skip_header=1, converters={1: lambda s: float(s)})
        except:
            ReportError('Could not read stoichiometry file.')

    def InitControls(self):
        """InitControls(self):
        Fills in the Elements list, sets up checkboxes, and fills in the phases list.
        """

        """ PHASES LIST CONTROL"""
        # Initialize the Phases list control.
        self.PhasesListCtrl.InsertColumn(0, 'Phase')

        # Load the list of phases.  It's two column.  First is the human name for the phase.  Second is the formula in the format 'Si1 O2' for SiO2.
        # The converter removes whitespace from the formula column so we can have variable column widths.
        self.Phases = genfromtxt('ConfigData/Phases.csv', dtype=None, comments='#', delimiter=',',
                                 converters={1: lambda s: str(s).lstrip()})

        # Now loop through each one, and add it to the phases list box.
        i = 0
        for Phase, Formula in self.Phases:
            self.PhasesListCtrl.InsertStringItem(i, Phase)
            i += 1

        # Make sure the column is wide enough to show everything.
        self.PhasesListCtrl.SetColumnWidth(0, 300)

        """ POPULATE KFACS PULLDOWN """
        for file in os.listdir('ConfigData'):
            if file.startswith('kfacs') and file.endswith('.csv'):
                kfacsname = file.split('kfacs ')[1].split('.csv')[0]
                self.comboKfacs.Append(kfacsname)
        self.comboKfacs.Select(0)
        # For counts we will want the kfactors.
        self.chkKfacs.SetValue(True)

        """ POPULATE ARBITRARY ABSORPTION PULLDOWN """
        for file in os.listdir('ConfigData'):
            if file.startswith('Absorption ') and file.endswith('.csv'):
                kfacsname = file.split('Absorption ')[1].split('.csv')[0]
                self.comboArbAbsCorrection.Append(kfacsname)
        self.comboArbAbsCorrection.Select(0)
        # The user will have to select if he wants an absorption correction.
        self.chkArbAbsCorrection.SetValue(False)

        """ POPULATE THE INPUT SOURCE """
        # Start with counts as the selected item.
        self.rdioInputType.SetSelection(0)

        """ POPULATE THE STOICHIOMETRY FITTER """
        for file in os.listdir('ConfigData'):
            if file.startswith('stoich') and file.endswith('.csv'):
                stoichname = file.split('stoich ')[1].split('.csv')[0]
                self.comboStoich.Append(stoichname)
        self.comboStoich.Select(0)
        # Default to using O by stoichiometry.
        self.chkOByStoichiometry.SetValue(True)

        self.LoadStoichiometryFile()

        """ ELEMENTS LIST CONTROL"""
        #Initialize the Elements list control.  Add a row for every element.
        self.ElementsListCtrl.InsertColumn(0, 'Element')
        self.ElementsListCtrl.SetColumnWidth(0, 60)
        self.ElementsListCtrl.InsertColumn(1, 'Counts')
        self.ElementsListCtrl.SetColumnWidth(1, 60)
        self.ElementsListCtrl.InsertColumn(2, 'Charge') # Used for stoichiometry calculation.
        self.ElementsListCtrl.SetColumnWidth(2, 60)
        for Z in range(1, pb.MAXELEMENT + 1):
            self.ElementsListCtrl.InsertStringItem(Z - 1, pb.ElementalSymbols[Z])
            self.ElementsListCtrl.SetStringItem(Z - 1, 1, '0')
        # The stoichometry column is separately populated by this function...
        self.OnStoichSelect(None)


    def OnReset(self, event):  # wxGlade: MyFrame.<event_handler>
        """OnReset(self, event):
            Set all the elements back to zero so the user can type in a new sample.
        """

        # Sometimes the person doesn't hit enter after editing a value in the ElementsListControl.  In this case,
        # we need to end his edit or the value doesn't get saved.
        self.ElementsListCtrl.CloseEditor(None)

        for Z in range(1, pb.MAXELEMENT + 1):
            self.ElementsListCtrl.SetStringItem(Z - 1, 1, '0')
        event.Skip()

    def OnGo(self, event):  # wxGlade: MyFrame.<event_handler>
        # Sometimes the person doesn't hit enter after editing a value in the ElementsListControl.  In this case,
        # we need to end his edit or the value doesn't get saved.
        self.ElementsListCtrl.CloseEditor(None)

        # Extract the counts vector out of the ElementsListControl.
        # Z-1 since H=1 is the first atom, and the list is zero based.
        self.Counts = zeros(pb.MAXELEMENT)
        for Z in range(1, pb.MAXELEMENT + 1):
            self.Counts[Z-1] = float(self.ElementsListCtrl.GetItem(Z - 1,1).GetText())

        # Make the input human readable and output it for reference.
        InputDat = OrderedDict(zip(pb.ElementalSymbols[1:], self.Counts))
        ReportStr = ReportResults.FormatInputResults(InputDat, self.rdioInputType.StringSelection)
        # Report it by printing to console and put it in the output text box.
        print ReportStr
        self.txtOutput.SetValue(ReportStr)
        
        # Find out if there is a k-factor file to use.
        if self.chkKfacs.IsChecked():
            kfacsfile = self.comboKfacs.StringSelection
        else:
            kfacsfile = None

        # Find out if there is an absorption correction to use.
        if self.chkArbAbsCorrection.IsChecked():
            DetectorFile = self.comboArbAbsCorrection.StringSelection
        else:
            DetectorFile = None

        # Find out if there is an absorption correction to do.
        AbsorptionCorrection = 0
        if self.chkAbsCorr.IsChecked():
            try:
                AbsorptionCorrection = float(self.txtAbsCorr.GetString(0,-1))
            except:
                wx.MessageBox('Absorption Correction is not a valid number.', 'Please correct input:')
                return

        # Find out if we are using oxygen by stoichiometry
        if self.chkOByStoichiometry.IsChecked():
            # Stoich is a list of tuples.  We want an array of atom charges from the 1 index of the tuples.  So unzip
            # the list into two tuples,
            # choose the tuple which corresponds to the charges not the atom names and feed it to numpy to make a vector.
            OByStoich = array(zip(*self.Stoich)[1])
        else:
            OByStoich = None

        # Stuff the user entered data into a black box and get out At%, Wt% results.
        Quant = CountsToQuant.GetAbundancesFromCounts(self.Counts, kfacsfile=kfacsfile,
                                                      ArbitraryAbsorptionCorrection= DetectorFile, InputType=self.rdioInputType\
                                                      .StringSelection, AbsorptionCorrection=0, OByStoichiometry=OByStoich)

        # Make it human readable.
        ReportStr = ReportResults.FormatQuantResults(Quant)

        # Report it by printing to console and put it in the output text box.
        print ReportStr
        self.txtOutput.AppendText(ReportStr)

        """ FIT PHASES """
        SelectedPhases = GetSelectedItemsFromListCtrl(self.PhasesListCtrl)

        if SelectedPhases == None:
            NoFitStr = '\n\nCould not fit phases since none were selected for the fit.'.format()
            print NoFitStr
            self.txtOutput.AppendText(NoFitStr)
        else:
            # Generate a list of phases with just the ones the user selected to fit.
            PhasesToFit = [PhasesToFit for PhasesToFit in self.Phases if PhasesToFit[0] in SelectedPhases]

            # Do a linear least squares fit for the best set of phases to represent this composition.
            FitResult, Residual = PhaseFit.FitPhases(Quant, PhasesToFit)

            # Report it to console and output text box.
            ReportStr = ReportResults.FormatPhaseResults(FitResult, Residual)
            print ReportStr
            self.txtOutput.AppendText(ReportStr)

        event.Skip()

    def UpdateInputType(self, InputType=None):
        # If InputType=None, then this is being called because the user changed the input type.
        # If it is 'Counts', 'At%' or 'Wt%' then we are being asked to update the type ourselves.
        if InputType == 'Counts':
            self.rdioInputType.SetSelection(0)
            self.chkOByStoichiometry.Enable()
        elif InputType == 'At%':
            self.rdioInputType.SetSelection(1)
            self.chkOByStoichiometry.Enable()
        elif InputType == 'Wt%':
            self.rdioInputType.SetSelection(2)
            self.chkOByStoichiometry.Enable()
        elif InputType == 'OxWt%':
            self.rdioInputType.SetSelection(3)

        # We use kfacs and arbitrary absorption correction (optionally) for counts.  At% and Wt% don't, ever.
        if self.rdioInputType.GetSelection() == 0:
            self.chkKfacs.SetValue(True)  # By default we'll use kfacs.
            # For now, the chkKfacs is permanently disabled.  If we ever provide an SEM
            # algorithm, or something then it should be a radio box.
            self.chkKfacs.Disable()
            self.comboKfacs.Enable()
        else:
            self.chkKfacs.SetValue(False)  # Uncheck it.
            self.chkKfacs.Disable()  # And also disable it so the user can't check it.  (Breaks our algorithms.)
            self.comboKfacs.Disable()

        # Get the column which is labeled Counts or At % or Wt %.
        col = self.ElementsListCtrl.GetColumn(1)
        # Depending on which radio is checked, choose the right text.
        if self.rdioInputType.GetSelection() == 0:
            col.SetText('Counts')
            self.chkOByStoichiometry.Enable()
        elif self.rdioInputType.GetSelection() == 1:
            col.SetText('At %')
            self.chkOByStoichiometry.Enable()
        elif self.rdioInputType.GetSelection() == 2:
            col.SetText('Wt %')
            self.chkOByStoichiometry.Enable()
        else:
            col.SetText('Ox Wt %')
            # For oxide wt % the user must use stoichiometry.
            self.chkOByStoichiometry.Disable()
            self.chkOByStoichiometry.SetValue(True)
            self.OnStoichSelect(None) # And update the list box.

        # And stuff that modified column back into the ListBox.
        self.ElementsListCtrl.SetColumn(1, col)

    def OnInputType(self, event):  # wxGlade: MyFrame.<event_handler>
        self.UpdateInputType()
        event.Skip()
        
    def OnStoichSelect(self, event):  # wxGlade: MyFrame.<event_handler>
        # It doesn't matter what the user did.  If they changed any stoichometry settings, we do it all from scratch.
        self.LoadStoichiometryFile()

        # If we are not using oxygen by stoichometry, then mark out the stoichiometry column.
        if self.chkOByStoichiometry.IsChecked() == False:
            for Z in range(1, pb.MAXELEMENT + 1):
                self.ElementsListCtrl.SetStringItem(Z-1, 2, 'n/a')
            # Make sure the user can only edit the counts column.
            self.ElementsListCtrl.SetEditableColumns((1, ))
        else:
            # If we are using it then we populate it from the self.Stoich variable read by LoadStoichiometryFile
            # Since that was a csv, we have a list of tuples like [('H', 1), ('He', 2), ...]  So index to the right tuple
            # [Z-1] and then into the tuple [Z-1][1]
            for Z in range(1, pb.MAXELEMENT + 1):
                self.ElementsListCtrl.SetStringItem(Z-1, 2, str(self.Stoich[Z-1][1]))
            # The user can edit the counts column and the stoichiometry column.
            self.ElementsListCtrl.SetEditableColumns((1,2))

        if event != None:
            event.Skip()

    def OnOpen(self, event):  # wxGlade: MyFrame.<event_handler>
        dlg = wx.FileDialog(self, 'Open counts/At%/Wt% input file', '','','Comma space delimited (*.csv)|*'
                                                                          '.csv|Any file (*.*)|*.*', wx.FD_OPEN |
                                                                          wx.FD_FILE_MUST_EXIST)

        if dlg.ShowModal() == wx.ID_CANCEL:
            return

        InputDat = genfromtxt(dlg.GetPath(), dtype=float, delimiter=',', usecols=(1), autostrip=True, comments='#',
                              names=True)

        HowlBadFile = lambda s: wx.MessageBox("Input file does not match the expected format.\n"
                                              "It should be a CSV with the header:\n"
                                              "Element,Counts\n"
                                              "Where Counts can be replaced by At%, Wt% or OxWt%.\n"
                                              "It should have a line for each element from H to Uuo.""",
                                              "Invalid file format: "+s,
                                              style=wx.OK)

        # Verify the quality of the input data.  It should have as many rows as we have rows in the input listbox.
        if len(InputDat) != self.ElementsListCtrl.GetItemCount():
            HowlBadFile('Incorrect number of lines')
            return

        # If the input type is valid, this will be set True.  Otherwise, we bail by default.
        InputTypeValid = False

        if InputDat.dtype.names[0][:2] in ['Co', 'At', 'Wt', 'Ox']:
            # Note that the file reader filters out the % symbol, so we have to add that in.  Kind of stupid...
            if InputDat.dtype.names[0] == 'Counts':
                # Set the input type radio to Counts
                self.UpdateInputType(InputDat.dtype.names[0])
            if InputDat.dtype.names[0] == 'OxWt':
                self.UpdateInputType('OxWt%')
            else:
                self.UpdateInputType(InputDat.dtype.names[0][:2] + '%')
        else:
            HowlBadFile('Incorrect header')
            return

        # Now populate it with the numbers from the input file.
        for Z in range(1, pb.MAXELEMENT + 1):
            self.ElementsListCtrl.SetStringItem(Z-1, 1, str(InputDat[Z-1][0]))
        return

    def OnSaveInputs(self, event):  # wxGlade: MyFrame.<event_handler>
        dlg = wx.FileDialog(self, 'Save inputs', '', '', 'CSV file (*.csv)|*'
                                                         '.csv|Any file (*.*)|*.*', wx.FD_SAVE)

        if dlg.ShowModal() == wx.ID_CANCEL:
            return

        if self.rdioInputType.GetSelection() == 0:
            SavStr = 'Element,Counts\n'
        elif self.rdioInputType.GetSelection() == 1:
            SavStr = 'Element,At%\n'
        elif self.rdioInputType.GetSelection() == 2:
            SavStr = 'Element,Wt%\n'
        elif self.rdioInputType.GetSelection() == 3:
            SavStr = 'Element,OxWt%\n'
        else:
            raise

        for Z in range(1, pb.MAXELEMENT + 1):
            ElName = pb.ElementalSymbols[Z]
            SavStr += '%s,%f\n' % (ElName, float(self.ElementsListCtrl.GetItem(Z-1,1).GetText()))

        with open(dlg.GetPath(), 'w') as fid:
            fid.write(SavStr)
        return

    def OnSave(self, event):  # wxGlade: MyFrame.<event_handler>
        dlg = wx.FileDialog(self, 'Save report', '', '', 'Text file (*.txt)|*'
                                                                            '.txt|Any file (*.*)|*.*', wx.FD_SAVE)

        if dlg.ShowModal() == wx.ID_CANCEL:
            return

        fid = open(dlg.GetPath(), 'w')
        fid.write(self.txtOutput.GetString(0, -1))
        fid.close()

        return

    def OnAbout(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'OnAbout' not implemented!"
        event.Skip()
    def OnDetectorSelect(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'OnDetectorSelect' not implemented!"
        event.Skip()

    # CURRENT END OF CLASS
 # end of class MyFrame

if __name__ == "__main__":
    gettext.install("app")  # replace with the appropriate catalog name

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, wx.ID_ANY, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()