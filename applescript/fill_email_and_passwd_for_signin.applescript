on run(arguments)
    set email to (first item of arguments)
    set passwd to (second item of arguments)
    tell application "RealTimes"
        activate
    end tell

    tell application "System Events"
        tell process "RealTimes"
            try
                set value of text field of group 6 of UI element 0 of scroll area 0 of window 1 to email
                delay 2
                set value of text field of group 7 of UI element 0 of scroll area 0 of window 1 to passwd
                delay 2
                click button 0 of UI element 0 of scroll area 0 of window 1
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
    end tell
end run