tell application "RealTimes"
	activate
end tell

tell application "System Events"
	tell process "RealTimes"
		tell menu item "Original Size" of menu 1 of menu bar item "Playback" of menu bar 1
			click
		end tell
	end tell
end tell