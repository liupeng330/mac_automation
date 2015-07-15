tell application "RealTimes"
    activate
end tell

tell application "System Events"
    
    tell process "RealTimes"
        tell button 3 of group 2 of group 1 of group 1 of splitter group 1 of splitter group 1 of window 1
            click
        end tell
    end tell
end tell