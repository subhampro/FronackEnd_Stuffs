-- Hey there! 👋 Welcome to the fancy manifest file where we tell FiveM what's what

fx_version 'cerulean'  -- Living on the edge with the latest and greatest
game 'gta5'           -- In case you couldn't guess which game this is for 😉

-- Who's responsible for this masterpiece?
author 'SubhaM'
description 'A fancy-pants guidebook that makes reading actually fun!'
version '1.0.0'     -- Starting small but dreaming big

-- All the cool client stuff (where the magic happens)
client_scripts {
    'client/main.lua',   -- The brains of the operation
}

-- Server-side wizardry (keep your secrets safe!)
server_scripts {
    'server/server.lua', -- The puppet master pulling the strings
    'config.lua',        -- Where all the "should I?" questions are answered
}

-- These files need to make it to the client (pretty please)
files {
    'ui/guidebook.html',      -- The pretty face of our operation
    'ui/guidebook-admin.html', -- Where the cool kids hang out
    'ui/mockdata.json',       -- Because everyone needs a backup plan
}

-- The star of the show
ui_page 'ui/guidebook.html'   -- First impressions matter!

-- Need friends to play with? Uncomment these!
-- dependencies {
--     'mysql-async',    -- Because raw SQL is scary
--     'es_extended'     -- The backbone of every proper server
-- }

-- If something breaks, it's not a bug, it's a feature! 😅