
fx_version 'cerulean'
game 'gta5'

author 'Your Name'
description 'Interactive Guidebook System for FiveM'
version '1.0.0'

shared_scripts {
    '@ox_lib/init.lua',
    'config.lua'
}

client_scripts {
    'client/*.lua'
}

server_scripts {
    '@oxmysql/lib/MySQL.lua',
    'server/*.lua'
}

ui_page 'html/index.html'

files {
    'html/index.html',
    'html/styles.css',
    'html/app.js'
}

dependencies {
    'oxmysql',
    'ox_lib'
}