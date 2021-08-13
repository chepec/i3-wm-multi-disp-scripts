# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import necessaryFuncs as nf

proc_out = subprocess.run(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
wkList = json.loads(proc_out.stdout.decode('utf-8'))
# print(wkList) # the whole output of "i3-msg -t get_workspaces"

focWkName = nf.getFocusedWK(wkList)
# print(focWkName) # 1::dash:1 # where we currently are
allProjectNames = nf.getListOfProjects(wkList)
# print(allProjectNames) # ['dash', 'P03', 'thesis', 'firma']

if (len(allProjectNames) == 0) or (allProjectNames is None):
    sys.exit(1)

currentProjName = nf.getProjectFromWKName(focWkName)
# print(currentProjName) # dash # where we currently are

if currentProjName is None:
    nextProjIndex = 0
else:
    nextProjIndex = allProjectNames.index(currentProjName)
    if nextProjIndex == (len(allProjectNames) - 1):
        nextProjIndex = 0
    else:
        nextProjIndex = nextProjIndex + 1

nxtProjWks = nf.getWKNamesFromProj(wkList, allProjectNames[nextProjIndex])
# print(nxtProjWks) # ['13::P03:2', '15::P03:4', '14::P03:3', '12::P03:1'] # where we are going

visWks = nf.getVisibleWKs(wkList)
# print(visWks) # ['5::dash:2', '0::dash:1', '6::dash:3', '1::dash:1'] # where we currently are

wksToMakeVisible = list(set(nxtProjWks) - set(visWks))
# print(wksToMakeVisible) # ['15::P03:4', '12::P03:1', '14::P03:3', '13::P03:2'] # where we are going

focOutput = nf.getOutputForWK(wkList, focWkName)
# print(focOutput) # DP-2 # that's the monitor name
focOutputWks = nf.getWorkspacesOnOutput(wkList, focOutput)
# print(focOutputWks) # ['1::dash:1', '12::P03:1', '18::thesis:3', '22::firma:3'] # workspace on that monitor, I suppose
wkToBeFocused = list(set(focOutputWks).intersection(nxtProjWks))
# print(wkToBeFocused)	# ['12::P03:1']

parCommToRun = ['workspace ' + x for x in wksToMakeVisible]
# print(parCommToRun) # ['workspace 12::P03:1', 'workspace 15::P03:4', 'workspace 14::P03:3', 'workspace 13::P03:2']
if len(wkToBeFocused) > 0 and wksToMakeVisible[-1] != wkToBeFocused[0]:
    parCommToRun.append('workspace ' + wkToBeFocused[0])

commandToRun = ["i3-msg", '; '.join(parCommToRun)]

subprocess.call(commandToRun)

projToBeFocused = nf.getProjectFromWKName(wkToBeFocused[0])
# print(projToBeFocused) # P03
subprocess.run(["zenity", "--notification", "--text=<span size='x-large'>workspace:</span> <span size='x-large' foreground='yellow' background='black' bgalpha='25%' weight='bold'>" + projToBeFocused + "</span>"])
