#!/usr/bin/env python
import sys
import os
import time
import plistlib
import shlex
import subprocess


def printUsage():
    """Prints command line usage for the script"""
    print("""Usage: convertSnippets.py /path/to/directory/containing/snippets/ /path/to/uncrustify.cfg 
             The snippets directory should include a file named SystemCodeSnippets.codesnippets.
             This script requires uncrustify available at: https://github.com/bengardner/uncrustify
             If in doubt try /convertSnippets.py ./snippets ./uncrustifyTemplates/sbi.cfg""")

def cleanSnippetsCode(snippets, outdir, uncrustifyConfigPath):
    """Dumps snippets into the outdir, runs uncrustify over them, and reloads them into the snippets"""
    for snippet in snippets:
        snippetID = snippet['IDECodeSnippetIdentifier']                                                                                                                                  
        tempCodeFile = outDir + snippetID + ".m"
        if (os.path.exists(tempCodeFile)):
            os.remove(tempCodeFile)
        fileHandle = open(tempCodeFile, 'w')
        code = snippet['IDECodeSnippetContents']
        print("code = \n" + code + "\n for file path " + tempCodeFile + "\n")
        fileHandle.writelines(code)
        fileHandle.close()
        commandLine = "uncrustify -c " + uncrustifyConfigPath + " --no-backup " + tempCodeFile
        args = shlex.split(commandLine)
        p = subprocess.call(args)
        time.sleep(.1)
        fileHandle = open(tempCodeFile, 'r')
        newCode = fileHandle.read()
        newCode = newCode.replace("< # ", "<#")
        newCode = newCode.replace(" # >", "#>")
        
        if(len(newCode) > 0):
            snippet['IDECodeSnippetContents'] = newCode
            print("uncrustified code = \n" + newCode + "\n")
        else:
            print("uncrustified code is empty; leaving it alone")
        fileHandle.close()
        os.remove(tempCodeFile)

def makeUserSnippets(snippets):
    """Makes each snippet into a user snippet and makes it the first prority for completion in Xcode"""
    for snippet in snippets:
        snippet['IDECodeSnippetUserSnippet'] = True
        snippet['IDECodeSnippetRelativePriority'] = 0

def dumpSnippetsPlist(snippets, outdir):
    """Dumps individual snippets as plists into outdir"""
    for snippet in snippets:
        snippetID = snippet['IDECodeSnippetIdentifier']
        snippetFileOut = outDir + snippetID + ".codesnippet"
        plistlib.writePlist(snippet, snippetFileOut)
        
def printWhatsNext():
    """Prints a helpful little howto for the rest of the process"""
    print("""
There should now be a series of .codesnippet files in the out directory.
You can copy them to ~/Library/Developer/Xcode/UserData/CodeSnippets.
You can probably safely replace the file located at (dev tools path)/Library/Xcode/PrivatePlugIns/IDECodeSnippetLibrary.ideplugin/Contents/Resources/SystemCodeSnippets.codesnippets with an empty one.
I would back that up first, just in case you want it back.  Reinstalling Xcode will also put it back, so you might find that it also reappears on occasion.
""")

if __name__ == '__main__':
    if (len(sys.argv) <= 2):
        printUsage()
        sys.exit()

    baseDir = sys.argv[1]
    baseDir = os.path.abspath(baseDir)
    if not (os.path.exists(baseDir) and os.path.isdir(baseDir)):
        printUsage()
        sys.exit(baseDir + " is not a directory.")
    
    outDir = os.path.join(baseDir, "pythonOut", "")
    if not (os.path.exists(outDir)):
        os.makedirs(outDir)
    if not (os.path.isdir(outDir)):
        printUsage()
        sys.exit(outdir + " already exists, but isn't a directory.  This script dumps its output there by default.")

    crustifyConfig = sys.argv[2]
    crustifyConfig = os.path.abspath(crustifyConfig)
    
    if not (os.path.exists(crustifyConfig) and not os.path.isdir(crustifyConfig)):                                                                                                   
        printUsage()
        sys.exit(crustifyConfig + " is not a config file.")
    
    snippetsDir = os.path.join(baseDir, "SystemCodeSnippets.codesnippets")
    print(snippetsDir)
    snippets = plistlib.readPlist(snippetsDir)

    cleanSnippetsCode(snippets, outDir, crustifyConfig)
    makeUserSnippets(snippets)
    dumpSnippetsPlist(snippets, outDir)
    printWhatsNext()

