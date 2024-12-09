local Framework = nil

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