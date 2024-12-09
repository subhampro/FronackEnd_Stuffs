fx_version 'cerulean'
game 'gta5'

name 'Guidebook Script'
description 'Interactive server guidebook system'
author 'Your Name'
version '1.0.0'

shared_scripts {
    '@es_extended/imports.lua',
    '@qb-core/shared/locale.lua',
    'config.lua',
    'locales/*.lua'
}

client_scripts {
    'client/*.lua'
}

server_scripts {
    '@oxmysql/lib/MySQL.lua',
    'sconfig.lua',
    'server/*.lua'
}

ui_page 'html/index.html'

files {
    'html/index.html',
    'html/css/*.css',
    'html/components.html',
    'html/js/*.js',
    'html/img/*.png'
}

dependencies {
    'oxmysql',
    'es_extended'
}