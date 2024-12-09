fx_version 'cerulean'
game 'gta5'

name 'Guidebook Script'
description 'Interactive server guidebook system'
author 'SubhaM'
version '1.0.0'

shared_scripts {
    '@es_extended/imports.lua',
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
    'server/utils.lua',       -- Load utilities first
    'server/database.lua',    -- Then database functions
    'server/categories.lua',  -- Load feature modules
    'server/pages.lua',
    'server/points.lua',
    'server/commands.lua',    
    'server/admin.lua',       
    'server/main.lua'         -- Load main script last
}

ui_page 'html/index.html'

files {
    'html/index.html',
    'html/admin.html',
    'html/css/*.css',
    'html/components/components.html',
    'html/js/*.js',
    'html/img/*.png'
}

dependencies {
    'oxmysql'
}