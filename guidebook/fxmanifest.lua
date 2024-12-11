-- Welcome to our FXServer manifest! This is where all the important stuff gets registered

fx_version 'cerulean'
game 'gta5'

-- Made with ❤️ by SubhaM
author 'SubhaM'
description 'Guidebook Resource'
version '1.0.0'

-- Let's tell FXServer what files to load
client_scripts {
    'client/*.lua', -- All our client-side magic
}

server_scripts {
    'server/*.lua', -- Server-side goodness
    'config.lua',   -- Main settings
    'sconfig.lua'   -- Server-specific settings
}

-- These files need to be downloaded to the client
files {
    'ui/*.html',    -- Our pretty interface
    'ui/*.json',    -- Data storage
    'locales/*.lua' -- Language stuff
}

-- This is where our UI lives
ui_page 'ui/guidebook.html'