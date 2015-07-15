#! /usr/bin/osascript

on run(arguments)
	set myDocumentFolder to POSIX path of (first item of arguments)

	tell application "Finder"
		close every window
		activate
		make new Finder window
		set toolbar visible of the front Finder window to false
		set statusbar visible of the front Finder window to false
		set the current view of front Finder window to icon view
		set the target of the front Finder window to (POSIX file myDocumentFolder)
		set screenResolution to bounds of window of desktop
	end tell

	set screenWidth to item 3 of screenResolution
	set screenHeight to item 4 of screenResolution

	tell application "System Events" to tell process "Dock"
		set dock_dimensions to size in list 1
		set dock_height to item 2 of dock_dimensions
	end tell

	tell application "Finder"
		activate
		set frontmost to true
		set bounds of the front Finder window to {screenWidth / 2, 24, screenWidth, screenHeight - dock_height}
	end tell 
end run
