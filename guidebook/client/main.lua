local Framework = nil
local PlayerData = {}
local helpPoints = {}

-- Debug Functions
local function DebugLog(level, message)
    if not Config.Debug then return end
    
    for _, allowedLevel in ipairs(Config.DebugLevel) do
        if level == allowedLevel then
            print(string.format('[Guidebook] [%s] %s', level, message))
            return
        end
    end
end

function DebugPoint(point)
    DebugLog('DEBUG', string.format('Point: %s, Type: %s, Coords: %s', 
        point.name, point.type, point.coords))
end

-- UI Functions
local function ShowUI(data)
    SetNuiFocus(true, true)
    SendNUIMessage({
        type = "show",
        data = data
    })
end

local function HideUI()
    SetNuiFocus(false, false)
    SendNUIMessage({
        type = "hide"
    })
end

RegisterNUICallback('close', function(data, cb)
    HideUI()
    cb('ok')
end)

-- Main Thread
CreateThread(function()
    while true do
        Wait(0)
        for _, point in pairs(helpPoints) do
            DrawHelpPoint(point)
        end
    end
end)

-- Framework Init
CreateThread(function()
    if Config.Framework == 1 or (Config.Framework == 0 and GetResourceState('es_extended') == 'started') then
        while Framework == nil do
            Framework = exports['es_extended']:getSharedObject()
            Wait(0)
        end
        PlayerData = Framework.GetPlayerData()
    elseif Config.Framework == 2 or (Config.Framework == 0 and GetResourceState('qb-core') == 'started') then
        Framework = exports['qb-core']:GetCoreObject()
        PlayerData = Framework.Functions.GetPlayerData()
    end
end)

-- Functions for handling help points, blips, and UI interactions
function OpenGuidebook(pageKey)
    local data = {
        type = 'openGuidebook',
        page = pageKey
    }
    SendNUIMessage(data)
    SetNuiFocus(true, true)
end

function CreateHelpPointBlips()
    -- Implementation
end

function NavigateToPoint(pointKey)
    for _, point in pairs(helpPoints) do
        if point.key == pointKey and point.can_navigate then
            local coords = json.decode(point.coords)
            SetNewWaypoint(coords.x, coords.y)
            ShowNotification(Locales[Config.Locale]['point_marked'])
            return
        end
    end
    ShowNotification(Locales[Config.Locale]['point_not_found'])
end

function ShowNotification(message)
    if Config.UseFrameworkNotify then
        if Framework.Name == 'esx' then
            TriggerEvent('esx:showNotification', message)
        else
            TriggerEvent('QBCore:Notify', message)
        end
    else
        SetNotificationTextEntry('STRING')
        AddTextComponentString(message)
        DrawNotification(false, false)
    end
end

-- Commands
RegisterCommand(Config.Commands.Help, function()
    TriggerEvent('guidebook:open')
end)

RegisterCommand(Config.Commands.Admin, function()
    if IsPlayerAdmin() then
        TriggerEvent('guidebook:openAdmin')
    else
        ShowNotification(Locales[Config.Locale]['no_permission'])
    end
end)

RegisterCommand(Config.Commands.Navigate, function(source, args)
    if #args < 1 then return end
    local pointKey = args[1]
    TriggerEvent('guidebook:navigateToPoint', pointKey)
end)

RegisterCommand(Config.Commands.SendHelp, function(source, args)
    if not IsPlayerAdmin() then return end
    
    local targetId = tonumber(args[1])
    local pageKey = args[2]
    
    if not targetId then return end
    TriggerServerEvent('guidebook:sendHelp', targetId, pageKey)
end)

-- Events
RegisterNetEvent('guidebook:updateHelpPoints')
AddEventHandler('guidebook:updateHelpPoints', function(points)
    helpPoints = points
    CreateHelpPointBlips()
end)

RegisterNetEvent('guidebook:showUI')
AddEventHandler('guidebook:showUI', function(data)
    ShowUI(data)
end)