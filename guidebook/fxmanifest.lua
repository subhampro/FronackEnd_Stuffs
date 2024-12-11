-- Hey there! 👋 Welcome to the fancy manifest file where we tell FiveM what's what

fx_version 'cerulean'  -- Living on the edge with the latest and greatest
game 'gta5'           -- In case you couldn't guess which game this is for 😉

-- Who's responsible for this masterpiece?
author 'SubhaM'
description 'A fancy-pants guidebook that makes reading actually fun!'
version '1.0.0'     -- Starting small but dreaming big

-- All the cool stuff we need
client_scripts {
    'client/main.lua',   -- The brains of the operation
    'config.lua'         -- Your friendly neighborhood config file
}

server_scripts {
    'server/server.lua'  -- The puppet master pulling the strings
}

files {
    'ui/guidebook.html',  
    'ui/guidebook-admin.html', -- Where the cool kids hang out    -- The pretty face of our operation
    'ui/mockdata.json',       -- Our trusty data backup
    'locales/*.lua'           -- Making the world a better place, one translation at a time
}

ui_page 'ui/guidebook.html'   -- First impressions matter!

-- If something breaks, it's not a bug, it's a feature! 😅