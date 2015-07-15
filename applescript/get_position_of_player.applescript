tell application "System Events"
	tell process "RealTimes"
		tell window ""
			activate
			get position
		end tell
	end tell
end tell