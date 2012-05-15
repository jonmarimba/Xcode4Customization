#!/bin/bash


BASEDIR=$(cd "$(dirname "$0")"; pwd)

#backup existing user code snippets
mkdir -p ~/Library/Developer/Xcode/UserData/CodeSnippets.bak
cp -r ~/Library/Developer/Xcode/UserData/CodeSnippets/* ~/Library/Developer/Xcode/UserData/CodeSnippets.bak/
rm -r ~/Library/Developer/Xcode/UserData/CodeSnippets/*

#remove the system code snippets
sudo rm /Applications/Xcode.app/Contents/PlugIns/IDECodeSnippetLibrary.ideplugin/Contents/Resources/SystemCodeSnippets.codesnippets 
sudo touch /Applications/Xcode.app/Contents/PlugIns/IDECodeSnippetLibrary.ideplugin/Contents/Resources/SystemCodeSnippets.codesnippets

#convert and uncrustify the snippets
python "$BASEDIR"/convertSnippets.py  "$BASEDIR"/snippets "$BASEDIR"/uncrustifyTemplates/sbi.cfg
cp -v "$BASEDIR"/snippets/pythonOut/*.codesnippet ~/Library/Developer/Xcode/UserData/CodeSnippets/  