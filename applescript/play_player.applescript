tell application "RealTimes"
	activate
end tell
delay 1
tell application "System Events"
	tell process "RealTimes"
		tell menu item "Play" of menu 1 of menu bar item "Playback" of menu bar 1
			click
		end tell
	end tell
end tell