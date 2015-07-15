on run argv
    set env to item 1 of argv
    tell application "RealTimes"
        activate
    end tell

    tell application "System Events"
        tell window "RealPlayer Cloud - Debug Control" of process "RealTimes"
            click radio button env of radio group 0 of group "Cloud Environment"
            click radio button "On" of radio group 0 of group "Debug Level"
            click button "OK"
        end tell
    end tell
end run