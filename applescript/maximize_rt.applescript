tell application "Finder"
	set screenResolution to bounds of window of desktop
end tell

set screenWidth to item 3 of screenResolution
set screenHeight to item 4 of screenResolution

tell application "System Events" to tell process "Dock"
	set dock_dimensions to size in list 1
	set dock_height to item 2 of dock_dimensions
end tell

tell application "System Events" to tell process "RealTimes"
	activate
	set position of window 1 to {0, 24}
	set size of window 1 to {screenWidth, screenHeight - dock_height - 24}
end tell