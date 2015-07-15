tell application "System Events"
    if exists (process "UserNotificationCenter") then
        tell process "UserNotificationCenter"
            if ((value of static text 1 of window 1 as string) contains "RealTimes") then
                click button "Ignore" of window 1
            end if
        end tell
    end if
end tell