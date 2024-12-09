local Framework = nil
local PlayerData = {}
local helpPoints = {}

-- Framework Detection and Initialization
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

-- Commands Registration
RegisterCommand(Config.Commands.Help, function()
    OpenGuidebook()
end)

RegisterCommand(Config.Commands.Navigate, function(source, args)
    if args[1] then
        NavigateToPoint(args[1])
    end
end)

-- Help Points Management
RegisterNetEvent('guidebook:updateHelpPoints')
AddEventHandler('guidebook:updateHelpPoints', function(points)
    helpPoints = points
    CreateHelpPointBlips()
end)

-- UI Callbacks
RegisterNUICallback('closeguidebook', function(data, cb)
    SetNuiFocus(false, false)
    cb('ok')
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