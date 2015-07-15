on run argv
    if (count argv) is 0 then
        set item_name to "MediaScan.JPG"
    else
        set item_name to (first item of argv)
        -- display dialog item_name
    end if
    
    tell application "RealTimes"
        activate
    end tell
    
    tell application "System Events"
        tell process "RealTimes"
            keystroke "f" using {command down}
            delay 0.5
            keystroke "f" using {command down}
            keystroke item_name
            keystroke return
            
        end tell
    end tell
end run