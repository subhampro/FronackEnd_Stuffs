
fx_version 'cerulean'
game 'gta5'

author 'Your Name'
description 'Guidebook Resource'
version '1.0.0'

client_scripts {
    'client/main.lua',
    'client/editor.lua'
}

server_scripts {
    'server/main.lua',
    'server/database.lua',
    'config.lua',
    'sconfig.lua'
}

files {
    'ui/guidebook.html',
    'ui/mockdata.json',
    'locales/en.lua'
}

ui_page 'ui/guidebook.html'