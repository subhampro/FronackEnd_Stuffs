-- Hey there! 👋 Welcome to the fancy manifest file where we tell FiveM what's what

fx_version 'cerulean'  -- Living on the edge with the latest and greatest
game 'gta5'           -- In case you couldn't guess which game this is for 😉

author 'SubhaM'
description 'A fancy-pants guidebook that makes reading actually fun!'
version '1.0.0'     

-- The essentials
client_scripts {
    'client/main.lua',   -- Where the magic happens
    'config.lua'         -- Configuration settings
}

server_scripts {
    'server/server.lua'  -- Server-side sorcery
}

-- Web UI files
files {
    'ui/guidebook.html',      -- Our pretty interface
    'ui/guidebook-admin.html', -- Where the cool kids hang out
    'ui/mockdata.json',       -- Default content
    'locales/*.lua'           -- Translations
}

ui_page 'ui/guidebook.html'