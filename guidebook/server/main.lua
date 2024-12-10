local Framework = nil
local MySQL = require('@oxmysql/lib/MySQL') -- Ensure this path is correct
local Categories = {}
local Pages = {}

-- Utility Functions
local function IsPlayerAdmin(player)
    if not player then return false end
    
    if Config.Framework == 1 then -- ESX
        return player.getGroup() == 'admin' or player.getGroup() == 'superadmin'
    elseif Config.Framework == 2 then -- QBCore
        return player.PlayerData.admin
    end
    return false
end

local function LogToDiscord(message)
    if SConfig.LogWebhook == '' then return end
    
    PerformHttpRequest(SConfig.LogWebhook, function(err, text, headers) end, 'POST', json.encode({
        username = 'Guidebook',
        content = message
    }), { ['Content-Type'] = 'application/json' })
end

local function GetPlayer(source)
    if Config.Framework == 1 then -- ESX
        return Framework.GetPlayerFromId(source)
    elseif Config.Framework == 2 then -- QBCore
        return Framework.Functions.GetPlayer(source)
    end
    return nil
end

local function HasAdminPermission(source)
    local player = GetPlayer(source)
    return IsPlayerAdmin(player)
end

-- Database Functions
local function InitializeDatabase()
    MySQL.ready(function()
        MySQL.Async.execute([[
            CREATE TABLE IF NOT EXISTS `guidebook_categories` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `name` varchar(50) NOT NULL,
                `description` text,
                `order` int(11) DEFAULT 0,
                `permissions` text,
                PRIMARY KEY (`id`)
            );

            CREATE TABLE IF NOT EXISTS `guidebook_pages` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `category_id` int(11) NOT NULL,
                `title` varchar(100) NOT NULL,
                `content` text NOT NULL,
                `key` varchar(50) NOT NULL,
                `order` int(11) DEFAULT 0,
                `permissions` text,
                PRIMARY KEY (`id`),
                FOREIGN KEY (`category_id`) REFERENCES `guidebook_categories`(`id`)
            );

            CREATE TABLE IF NOT EXISTS `guidebook_points` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `name` varchar(50) NOT NULL,
                `key` varchar(50) NOT NULL,
                `coords` varchar(50) NOT NULL,
                `type` varchar(20) NOT NULL,
                `page_key` varchar(50),
                `can_navigate` tinyint(1) DEFAULT 0,
                `permissions` text,
                `blip_sprite` int(11) DEFAULT 1,
                `blip_color` int(11) DEFAULT 0,
                `blip_scale` float DEFAULT 1.0,
                PRIMARY KEY (`id`)
            );
        ]])
    end)
end

-- Data Loading Functions
local function LoadCategories()
    local result = MySQL.Sync.fetchAll('SELECT * FROM guidebook_categories ORDER BY `order` ASC')
    for i=1, #result do
        result[i].permissions = json.decode(result[i].permissions or '[]')
    end
    return result
end

local function LoadPages()
    local result = MySQL.Sync.fetchAll('SELECT * FROM guidebook_pages ORDER BY `order` ASC')
    for i=1, #result do
        result[i].permissions = json.decode(result[i].permissions or '[]')
    end
    return result
end

-- Point Management
local function ValidatePoint(point)
    if not point.name or not point.coords then
        return false, 'Invalid point data'
    end
    if point.type == 'blip' and not point.blipSprite then
        return false, 'Invalid blip configuration'
    end
    return true
end

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

-- Event Handlers
RegisterNetEvent('guidebook:fetchCategories')
AddEventHandler('guidebook:fetchCategories', function()
    local source = source
    TriggerClientEvent('guidebook:receiveCategories', source, LoadCategories())
end)

RegisterNetEvent('guidebook:fetchPages')
AddEventHandler('guidebook:fetchPages', function()
    local source = source
    TriggerClientEvent('guidebook:receivePages', source, LoadPages())
end)

RegisterNetEvent('guidebook:createCategory')
AddEventHandler('guidebook:createCategory', function(data)
    local source = source
    if not HasAdminPermission(source) then return end
    
    MySQL.Async.execute('INSERT INTO guidebook_categories (name, description, `order`, permissions) VALUES (?, ?, ?, ?)',
        {data.name, data.description, data.order, json.encode(data.permissions)})
    
    TriggerClientEvent('guidebook:updateCategories', -1)
    LogToDiscord(string.format('Category created by %s: %s', GetPlayerName(source), data.name))
end)

-- Point Events
RegisterNetEvent('guidebook:createPoint')
AddEventHandler('guidebook:createPoint', function(point)
    local source = source
    if not HasAdminPermission(source) then return end
    
    local isValid, error = ValidatePoint(point)
    if not isValid then
        TriggerClientEvent('guidebook:showNotification', source, error)
        return
    end

    MySQL.Async.execute([[
        INSERT INTO guidebook_points 
        (name, `key`, coords, type, page_key, can_navigate, permissions) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ]], {
        point.name,
        point.key,
        json.encode(point.coords),
        point.type,
        point.page_key,
        point.can_navigate,
        json.encode(point.permissions)
    })

    TriggerClientEvent('guidebook:updatePoints', -1)
    LogToDiscord(string.format('Help point created by %s: %s', GetPlayerName(source), point.name))
end)

-- Page Events
RegisterNetEvent('guidebook:savePage')
AddEventHandler('guidebook:savePage', function(page)
    local source = source
    if not HasAdminPermission(source) then return end

    MySQL.Async.execute('INSERT INTO guidebook_pages (category_id, title, content, `key`, `order`, permissions) VALUES (?, ?, ?, ?, ?, ?)',
        {page.category_id, page.title, page.content, page.key, page.order, json.encode(page.permissions)})
    
    TriggerClientEvent('guidebook:updatePages', -1)
    LogToDiscord(string.format('Page created by %s: %s', GetPlayerName(source), page.title))
end)

-- Commands
RegisterCommand(Config.Commands.Admin, function(source, args)
    local xPlayer = GetPlayer(source)
    if IsPlayerAdmin(xPlayer) then
        TriggerClientEvent('guidebook:openAdmin', source)
    end
end)

RegisterCommand(Config.Commands.SendHelp, function(source, args)
    if not HasAdminPermission(source) then return end
    local targetId = tonumber(args[1])
    local pageKey = args[2]
    if targetId then
        TriggerClientEvent('guidebook:openGuidebook', targetId, pageKey)
    end
end)

-- Additional Events from commands.lua
RegisterServerEvent('guidebook:openForPlayer')
AddEventHandler('guidebook:openForPlayer', function(playerId, pageKey)
    TriggerClientEvent('guidebook:open', playerId, pageKey)
end)

RegisterServerEvent('guidebook:navigateToPoint')
AddEventHandler('guidebook:navigateToPoint', function(pointKey)
    local source = source
    local point = MySQL.Sync.fetchAll('SELECT * FROM guidebook_points WHERE `key` = @key', {['@key'] = pointKey})[1]
    if point and point.can_navigate then
        TriggerClientEvent('guidebook:setGPS', source, json.decode(point.coords))
    end
end)