
local themes = {
    dark = {
        background = '#1a1a1a',
        text = '#ffffff',
        border = '#333333',
        inputBackground = '#2a2a2a',
        accent = '#4a90e2',
        error = '#ff4444',
        success = '#4caf50'
    },
    light = {
        background = '#ffffff',
        text = '#000000',
        border = '#dddddd',
        inputBackground = '#f5f5f5',
        accent = '#2196f3',
        error = '#f44336',
        success = '#4caf50'
    },
    twilight = {
        background = '#2c2f33',
        text = '#99aab5',
        border = '#23272a',
        inputBackground = '#36393f',
        accent = '#7289da',
    }
}

function SetTheme(themeName)
    local theme = themes[themeName]
    if theme then
        SendNUIMessage({
            type = 'setTheme',
            theme = theme
        })
    end
end

-- Command to set the theme
RegisterCommand('settheme', function(source, args)
    local themeName = args[1]
    SetTheme(themeName)
end)