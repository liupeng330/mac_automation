tell application "System Events" to tell process "Dock"
    set dock_dimensions to size in list 1
    set dock_height to item 2 of dock_dimensions
end tell