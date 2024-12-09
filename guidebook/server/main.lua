local Framework = nil
local MySQL = require('mysql-async')

-- Framework Detection
CreateThread(function()
    if Config.Framework == 1 or (Config.Framework == 0 and GetResourceState('es_extended') == 'started') then
        Framework = exports['es_extended']:getSharedObject()
    elseif Config.Framework == 2 or (Config.Framework == 0 and GetResourceState('qb-core') == 'started') then
        Framework = exports['qb-core']:GetCoreObject()
    end
end)

-- Database Initialization
MySQL.ready(function()
    InitializeDatabase()
end)

-- Commands
RegisterCommand(Config.Commands.Admin, function(source, args)
    local xPlayer = GetPlayer(source)
    if IsPlayerAdmin(xPlayer) then
        TriggerClientEvent('guidebook:openAdmin', source)
    end
end)

RegisterCommand(Config.Commands.SendHelp, function(source, args)
    local xPlayer = GetPlayer(source)
    if IsPlayerAdmin(xPlayer) and args[1] then
        local targetId = tonumber(args[1])
        local pageKey = args[2]
        SendHelpToPlayer(targetId, pageKey)
    end
end)

-- Events and Functions
RegisterServerEvent('guidebook:fetchData')
AddEventHandler('guidebook:fetchData', function()
    local source = source
    local xPlayer = GetPlayer(source)
    FetchPlayerData(source, xPlayer)
end)

RegisterNetEvent('guidebook:sendHelp')
AddEventHandler('guidebook:sendHelp', function(targetId, pageKey)
    local source = source
    if not HasAdminPermission(source) then return end
    TriggerClientEvent('guidebook:openGuidebook', targetId, pageKey)
end)

RegisterServerEvent('guidebook:saveCategory')
AddEventHandler('guidebook:saveCategory', function(category)
    MySQL.Async.execute('INSERT INTO guidebook_categories (name, description, `order`, permissions) VALUES (@name, @description, @order, @permissions)', {
        ['@name'] = category.name,
        ['@description'] = category.description,
        ['@order'] = category.order,
        ['@permissions'] = json.encode(category.permissions)
    })
end)

RegisterServerEvent('guidebook:savePage')
AddEventHandler('guidebook:savePage', function(page)
    MySQL.Async.execute('INSERT INTO guidebook_pages (category_id, title, content, `key`, `order`, permissions) VALUES (@category_id, @title, @content, @key, @order, @permissions)', {
        ['@category_id'] = page.category_id,
        ['@title'] = page.title,
        ['@content'] = page.content,
        ['@key'] = page.key,
        ['@order'] = page.order,
        ['@permissions'] = json.encode(page.permissions)
    })
end)

RegisterServerEvent('guidebook:saveContent')
AddEventHandler('guidebook:saveContent', function(data)
    MySQL.Async.execute('UPDATE guidebook_pages SET content = @content WHERE id = @id', {
        ['@content'] = data.content,
        ['@id'] = data.id
    })
end)

RegisterServerEvent('guidebook:createPoint')
AddEventHandler('guidebook:createPoint', function(point)
    MySQL.Async.execute('INSERT INTO guidebook_points (name, `key`, coords, type, page_key, can_navigate, permissions) VALUES (@name, @key, @coords, @type, @page_key, @can_navigate, @permissions)', {
        ['@name'] = point.name,
        ['@key'] = point.key,
        ['@coords'] = json.encode(point.coords),
        ['@type'] = point.type,
        ['@page_key'] = point.page_key,
        ['@can_navigate'] = point.can_navigate,
        ['@permissions'] = json.encode(point.permissions)
    })
end)

RegisterServerEvent('guidebook:deletePoint')
AddEventHandler('guidebook:deletePoint', function(pointId)
    MySQL.Async.execute('DELETE FROM guidebook_points WHERE id = @id', {
        ['@id'] = pointId
    })
end)