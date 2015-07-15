tell application "System Events"
    tell process "CoreServicesUIAgent"
        set theseWindows to every window whose subrole is "AXSystemDialog"
        repeat with thisWindow in theseWindows
            thisWindow
            click button "Open" of thisWindow
        end repeat
    end tell
end tell