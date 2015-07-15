tell application "RealTimes"
	activate
end tell
delay 1
tell application "System Events"
	tell process "RealTimes"
		tell group 1 of group 1 of group 1 of splitter group 1 of splitter group 1 of window 1
			tell button "Save"
				click
			end tell
		end tell
	end tell
	keystroke "u"
	delay 0.5
	key code 36
end tell