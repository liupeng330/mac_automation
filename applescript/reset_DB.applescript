tell application "RealTimes"
    activate
end tell

tell application "System Events"
    
    tell process "RealTimes"
        tell menu item "Preferences..." of menu 1 of menu bar item 2 of menu bar 1
            click
        end tell
        
        -- Navigate to Preferences
        tell button "Update" of toolbar 1 of window "Preferences"
            click
        end tell
        
        tell button "Reset RealTimes" of group 1 of window "Preferences"
            click
        end tell
        
        tell button "OK" of sheet 1 of window "Preferences"
            click
        end tell
    end tell
end tell