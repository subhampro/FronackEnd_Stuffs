local QBCore = exports['qb-core']:GetCoreObject()
local ESX = nil

-- Framework Detection
if GetResourceState('es_extended') ~= 'missing' then
    ESX = exports['es_extended']:getSharedObject()
end

-- Database initialization
MySQL.ready(function()
    MySQL.Async.execute([[
        CREATE TABLE IF NOT EXISTS guidebook_categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            description TEXT,
            permission_level INT DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS guidebook_pages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category_id INT,
            title VARCHAR(100) NOT NULL,
            content TEXT,
            permission_level INT DEFAULT 0,
            FOREIGN KEY (category_id) REFERENCES guidebook_categories(id)
        );

        CREATE TABLE IF NOT EXISTS guidebook_help_points (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            x FLOAT,
            y FLOAT,
            z FLOAT,
            page_id INT,
            blip_sprite INT,
            blip_color INT,
            FOREIGN KEY (page_id) REFERENCES guidebook_pages(id)
        );
    ]])
end)

-- Server events and command handlers
RegisterCommand('help', function(source)
    TriggerClientEvent('guidebook:openUI', source)
end)

RegisterCommand('helpadmin', function(source)
    if IsPlayerAdmin(source) then
        TriggerClientEvent('guidebook:openAdminUI', source)
    end
end)

-- Category Management
RegisterNetEvent('guidebook:createCategory')
AddEventHandler('guidebook:createCategory', function(data)
    if not IsPlayerAdmin(source) then return end
    MySQL.Async.insert('INSERT INTO guidebook_categories (name, description, permission_level) VALUES (?, ?, ?)', {data.name, data.description, data.permission_level})
end)

RegisterNetEvent('guidebook:editCategory')
AddEventHandler('guidebook:editCategory', function(data)
    if not HasPermission(source, 'edit') then return end
    MySQL.Async.execute('UPDATE guidebook_categories SET name = ?, description = ?, permission_level = ? WHERE id = ?',
        {data.name, data.description, data.permission_level, data.id})
end)

RegisterNetEvent('guidebook:deleteCategory')
AddEventHandler('guidebook:deleteCategory', function(id)
    if not HasPermission(source, 'delete') then return end
    MySQL.Async.execute('DELETE FROM guidebook_categories WHERE id = ?', {id})
end)

-- Page Management
RegisterNetEvent('guidebook:createPage')
AddEventHandler('guidebook:createPage', function(data)
    if not IsPlayerAdmin(source) then return end
    MySQL.Async.insert('INSERT INTO guidebook_pages (category_id, title, content, permission_level) VALUES (?, ?, ?, ?)', {data.category_id, data.title, data.content, data.permission_level})
end)

RegisterNetEvent('guidebook:editPage')
AddEventHandler('guidebook:editPage', function(data)
    if not HasPermission(source, 'edit') then 
        TriggerClientEvent('guidebook:notification', source, Locales[Config.Locale]['no_permission'])
        return 
    end
    
    MySQL.Async.execute('UPDATE guidebook_pages SET title = ?, content = ?, permission_level = ? WHERE id = ?',
        {data.title, data.content, data.permission_level, data.id},
        function(rowsChanged)
            SendDiscordLog('page_edit', data)
        end)
end)

-- Help Points
RegisterNetEvent('guidebook:createHelpPoint')
AddEventHandler('guidebook:createHelpPoint', function(data)
    if not IsPlayerAdmin(source) then return end
    MySQL.Async.insert('INSERT INTO guidebook_help_points (name, x, y, z, page_id, blip_sprite, blip_color) VALUES (?, ?, ?, ?, ?, ?, ?)', {data.name, data.x, data.y, data.z, data.page_id, data.blip_sprite, data.blip_color})
end)

RegisterNetEvent('guidebook:editHelpPoint')
AddEventHandler('guidebook:editHelpPoint', function(data)
    if not HasPermission(source, 'manage_points') then return end
    
    MySQL.Async.execute('UPDATE guidebook_help_points SET name = ?, blip_sprite = ?, blip_color = ? WHERE id = ?',
        {data.name, data.blip_sprite, data.blip_color, data.id},
        function(rowsChanged)
            SendDiscordLog('help_point_edit', data)
            SyncHelpPoints()
        end)
end)

function SyncHelpPoints()
    MySQL.Async.fetchAll('SELECT * FROM guidebook_help_points', {}, function(points)
        TriggerClientEvent('guidebook:syncHelpPoints', -1, points)
    end)
end

-- Command Implementation
RegisterCommand('sendhelp', function(source, args)
    local targetId = tonumber(args[1])
    local pageKey = args[2]
    if targetId and pageKey then
        TriggerClientEvent('guidebook:openUI', targetId, pageKey)
    end
end)

-- Permission checking
function HasPermission(source, action)
    local player = GetPlayer(source)
    if not player then return false end
    
    local job = player.job
    local jobGrade = player.job.grade

    if Config.Permissions.JobGrades[job.name] then
        return jobGrade >= Config.Permissions.JobGrades[job.name][action]
    end
    return false
end

function GetPlayer(source)
    if Config.Framework == 'esx' then
        return ESX.GetPlayerFromId(source)
    elseif Config.Framework == 'qbcore' then
        return QBCore.Functions.GetPlayer(source)
    end
    return nil
end

-- Discord Webhook Logging
function LogToDiscord(action, data)
    if Config.DiscordWebhook then
        -- Implementation here
    end
end

-- More server-side logic...