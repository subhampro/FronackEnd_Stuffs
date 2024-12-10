fx_version 'cerulean'
game 'gta5'

name 'Guidebook Script'
description 'Interactive server guidebook system'
author 'SubhaM'
version '1.0.0'

shared_scripts {
    -- '@es_extended/imports.lua',  -- Uncomment this line for ESX framework
    '@qb-core/shared/locale.lua',
    'shared/config.lua',
    'shared/sconfig.lua',
    'locales/*.lua'
}

client_scripts {
    'client/*.lua'
}

server_scripts {
    '@oxmysql/lib/MySQL.lua',
    'shared/sconfig.lua',
    'server/*.lua'
}

ui_page 'html/index.html'

files {
    'html/index.html',
    'html/css/*.css',
    'html/js/*.js',
}

dependencies {
    'qb-core',  -- Remove this line and uncomment below for ESX
    -- 'es_extended',
    'oxmysql'
}