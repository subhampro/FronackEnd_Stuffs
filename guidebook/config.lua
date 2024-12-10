Config = {}

Config.Framework = 'auto' -- 'auto', 'esx', 'qbcore'

Config.Debug = false

Config.Themes = {
    default = {
        primary = '#2c3e50',
        secondary = '#34495e',
        accent = '#3498db',
        text = '#ecf0f1'
    },
    dark = {
        primary = '#1a1a1a',
        secondary = '#2d2d2d',
        accent = '#bb86fc',
        text = '#ffffff'
    },
    light = {
        primary = '#ffffff',
        secondary = '#f5f5f5',
        accent = '#007bff',
        text = '#333333'
    },
    neon = {
        primary = '#0a0a0a',
        secondary = '#1a1a1a',
        accent = '#00ff00',
        text = '#ffffff'
    },
    sunset = {
        primary = '#ff7e5f',
        secondary = '#feb47b',
        accent = '#ff5e62',
        text = '#ffffff'
    },
    forest = {
        primary = '#2d5a27',
        secondary = '#1e4d2b',
        accent = '#a7c957',
        text = '#ffffff'
    }
    -- Add more themes...
}

Config.DefaultPermissions = {
    admin = {
        edit = true,
        delete = true,
        manage_points = true
    },
    user = {
        view = true,
        edit = false,
        delete = false
    }
}

Config.HelpPointDefaults = {
    blipSprite = 280,
    blipColor = 2,
    markerType = 1,
    markerSize = {x = 1.5, y = 1.5, z = 1.0}
}

Config.DiscordWebhook = '' -- Add your Discord webhook URL

Config.Debug = {
    level = 1, -- 0: None, 1: Basic, 2: Verbose
    logToFile = true,
    logPath = 'logs/guidebook.log'
}

Config.Permissions = {
    JobGrades = {
        ['police'] = {
            edit = 3,
            delete = 4
        },
        ['admin'] = {
            edit = 0,
            delete = 0
        }
    }
}