tell application "System Events"
	tell process "RealTimes"
		tell window ""
			get value of static text 0 of group 2
		end tell
	end tell
end tell