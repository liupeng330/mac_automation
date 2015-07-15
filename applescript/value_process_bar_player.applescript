tell application "System Events"
    tell process "RealTimes"
        get value of slider 1 of group 1 of window ""
    end tell
end tell