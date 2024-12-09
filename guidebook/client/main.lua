local Framework = nil
local PlayerData = {}
local helpPoints = {}
local blips = {}
local isEditing = false

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

-- Blip Functions
function CreateBlip(point)
    local blip = AddBlipForCoord(point.coords.x, point.coords.y, point.coords.z)
    SetBlipSprite(blip, point.blipSprite or 1)
    SetBlipColour(blip, point.blipColor or 0)
    SetBlipScale(blip, point.blipScale or 1.0)
    SetBlipAsShortRange(blip, true)
    BeginTextCommandSetBlipName("STRING")
    AddTextComponentString(point.name)
    EndTextCommandSetBlipName(blip)
    
    blips[point.id] = blip
    return blip
end

function RemoveBlip(pointId)
    if blips[pointId] then
        RemoveBlip(blips[pointId])
        blips[pointId] = nil
    end
end

-- Editor Functions
function OpenEditor(data)
    isEditing = true
    SendNUIMessage({
        type = 'openEditor',
        data = data
    })
    SetNuiFocus(true, true)
end

RegisterNUICallback('saveContent', function(data, cb)
    if not isEditing then return end
    TriggerServerEvent('guidebook:saveContent', data)
    isEditing = false
    cb('ok')
end)

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
    if isEditing then
        isEditing = false
    end
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

function DrawHelpPoint(point)
    if point.type == '3dtext' then
        Draw3DText(point.coords.x, point.coords.y, point.coords.z, point.name)
    elseif point.type == 'marker' then
        DrawMarker(1, point.coords.x, point.coords.y, point.coords.z - 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 255, 255, 255, 100)
    end
    -- Update blip if needed
    if point.type == 'blip' and not blips[point.id] then
        CreateBlip(point)
    end
end

-- Cleanup Function
function CleanupResources()
    for pointId, blip in pairs(blips) do
        RemoveBlip(blip)
    end
    blips = {}
    helpPoints = {}
    isEditing = false
end

-- Register Events
RegisterNetEvent('guidebook:pointUpdated')
AddEventHandler('guidebook:pointUpdated', function(pointData)
    if blips[pointData.id] then
        RemoveBlip(pointData.id)
    end
    if pointData.type == 'blip' then
        CreateBlip(pointData)
    end
end)

RegisterNetEvent('guidebook:pointDeleted')
AddEventHandler('guidebook:pointDeleted', function(pointId)
    RemoveBlip(pointId)
    helpPoints[pointId] = nil
end)

AddEventHandler('onResourceStop', function(resourceName)
    if GetCurrentResourceName() == resourceName then
        CleanupResources()
    end
end)