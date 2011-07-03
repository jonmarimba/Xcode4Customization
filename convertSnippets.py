#!/usr/bin/env python
import sys
import os
import plistlib
import shlex
import subprocess


def printUsage():
    """Prints command line usage for the script"""
    print("Usage: convertSnippets.py /path/to/directory/containing/snippets/ \nThis directory should include a file named SystemCodeSnippets.codesnippets")

def cleanSnippetsCode(snippets, outdir):
    """Dumps snippets into the outdir, runs uncrustify over them, and reloads them into the snippets"""
    for snippet in snippets:
        snippetID = snippet['IDECodeSnippetIdentifier']                                                                                                                                  
        codeFileOut = outDir + snippetID + ".m"
        if (os.path.exists(codeFileOut)):
            os.remove(codeFileOut)
        fileHandle = open(codeFileOut, 'w')
        code = snippet['IDECodeSnippetContents']
        fileHandle.writelines(code)
        fileHandle.close()
        commandLine = "uncrustify -c /Volumes/MacOSX/Users/jonathan/svnCheckouts/Xcode4Customization/uncrustifyTemplates/sbi.cfg --no-backup " + codeFileOut
        args = shlex.split(commandLine)
        p = subprocess.Popen(args)
        fileHandle = open(codeFileOut, 'r')
        newCode = fileHandle.read()
        #print("New code = \n" + newCode + " old code = \n" + code);
        if(len(newCode) > 0):
            snippet['IDECodeSnippetContents'] = newCode
        fileHandle.close()
        os.path.remove(codeFileOut)

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
        
if __name__ == '__main__':
    if (len(sys.argv) <= 1):
        printUsage()
        sys.exit()

    baseDir = sys.argv[1]
    baseDir = os.path.abspath(baseDir)
    if not (os.path.exists(baseDir) and os.path.isdir(baseDir)):
        printUsage()
        sys.exit(baseDir + " is not a directory.")

    
    outDir = os.path.join(baseDir, "pythonOut")
    print("outdir = " + outDir)
    if not (os.path.exists(outDir)):
        os.makedirs(outDir)
    elif not (os.path.isdir(outDir)):
        printUsage()
        sys.exit(outdir + " already exists, but isn't a directory.  This script dumps its output there by default.")

    snippetsDir = os.path.join(baseDir, "SystemCodeSnippets.codesnippets")
    snippets = plistlib.readPlist(snippetsDir)

    cleanSnippetsCode(snippets, outDir)
    makeUserSnippets(snippets)
    dumpSnippetsPlist(snippets, outDir)
