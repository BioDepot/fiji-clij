import os
import glob
import sys
import functools
import jsonpickle
from collections import OrderedDict
from Orange.widgets import widget, gui, settings
import Orange.data
from Orange.data.io import FileFormat
from DockerClient import DockerClient
from BwBase import OWBwBWidget, ConnectionDict, BwbGuiElements, getIconName, getJsonName
from PyQt5 import QtWidgets, QtGui

class OWsequenceGen(OWBwBWidget):
    name = "sequenceGen"
    description = "alpine bash with wget curl gzip bzip2"
    priority = 1
    icon = getIconName(__file__,"genSeq.png")
    want_main_area = False
    docker_image_name = "biodepot/seq-gen"
    docker_image_tag = "alpine-3.7__081418"
    inputs = [("Trigger",str,"handleInputsTrigger"),("pattern",str,"handleInputspattern"),("min",str,"handleInputsmin"),("max",str,"handleInputsmax")]
    outputs = [("output_seq",str)]
    pset=functools.partial(settings.Setting,schema_only=True)
    runMode=pset(0)
    exportGraphics=pset(False)
    runTriggers=pset([])
    triggerReady=pset({})
    inputConnectionsStore=pset({})
    optionsChecked=pset({})
    pattern=pset("%d")
    min=pset(None)
    max=pset(None)
    def __init__(self):
        super().__init__(self.docker_image_name, self.docker_image_tag)
        with open(getJsonName(__file__,"sequenceGen")) as f:
            self.data=jsonpickle.decode(f.read())
            f.close()
        self.initVolumes()
        self.inputConnections = ConnectionDict(self.inputConnectionsStore)
        self.drawGUI()
    def handleInputsTrigger(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("Trigger", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputspattern(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("pattern", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsmin(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("min", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleInputsmax(self, value, *args):
        if args and len(args) > 0: 
            self.handleInputs("max", value, args[0][0], test=args[0][3])
        else:
            self.handleInputs("inputFile", value, None, False)
    def handleOutputs(self):
        outputValue=None
        if hasattr(self,"output_seq"):
            outputValue=getattr(self,"output_seq")
        self.send("output_seq", outputValue)
