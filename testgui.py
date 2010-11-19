import EasyDialogs
import os

filename = EasyDialogs.AskFileForOpen(
    message='Select a Python source file',
    defaultLocation=os.getcwd(),
    wanted=unicode,
    )

print 'Selected:', filename