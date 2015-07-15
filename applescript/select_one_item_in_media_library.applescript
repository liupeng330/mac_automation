on run argv
	set watch_folder_item to item 1 of argv

	tell application "RealTimes"
		activate
	end tell

	tell application "System Events"
		
		tell process "RealTimes"
			tell menu item "Preferences..." of menu 1 of menu bar item 2 of menu bar 1
				click
			end tell
			
			-- Navigate to Preferences
			tell button "Media Library" of toolbar 1 of window "Preferences"
				click
			end tell
			
			tell table 1 of scroll area 1 of group 1 of group 1 of window "Preferences"
				repeat with thisRow in rows
					set rowValue to value of static text 1 of UI element 1 of thisRow
					if rowValue is watch_folder_item then
						tell checkbox 1 of UI element 1 of thisRow
							if not (its value as boolean) then click
						end tell
					end if
				end repeat
			end tell
			
			tell window "Preferences"
				click button 1
			end tell

		end tell
		
	end tell
end run