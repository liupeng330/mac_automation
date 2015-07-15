tell application "System Events"
	tell process "RealTimes"
		tell window ""
			activate
			get size
		end tell
	end tell
end tell