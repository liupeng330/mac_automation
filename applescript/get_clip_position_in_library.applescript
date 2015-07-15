on run argv
    set clip_name to item 1 of argv
    tell application "RealTimes"
        activate
    end tell

    tell application "System Events"
        tell process "RealTimes"
            tell UI element 0 of scroll area 0 of group 0 of splitter group 0 of splitter group 0 of window 0
                tell (1st image whose title is clip_name)
                    set p to position
                    set s to size
                    
                    set x to ((item 1 of p) + (item 1 of s) / 2)
                    set y to ((item 2 of p) + (item 2 of s) / 2)
                    
                    set output to ("" & x & "," & y)
                    do shell script "echo " & quoted form of output
                end tell
            end tell
        end tell
    end tell
end run