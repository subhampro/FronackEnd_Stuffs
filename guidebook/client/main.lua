local Framework = nil
local PlayerData = {}
local helpPoints = {}
local blips = {}
local isEditing = false
local isAdminPanelOpen = false
local Categories = {}
local Pages = {}
local searchResults = {}

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

-- Add after Debug Functions
local function SafeNUIOperation(operation, fallback)
    local success, error = pcall(operation)
    if not success then
        print('^1[Guidebook Error]^7:', error)
        SetNuiFocus(false, false) -- Reset NUI focus
        if fallback then fallback() end
        return false
    end
    return true
end

-- Theme Management
local themes = {
    dark = {
        background = '#1a1a1a',
        text = '#ffffff',
        border = '#333333',
        inputBackground = '#2a2a2a',
        accent = '#4a90e2'
    },
    light = {
        background = '#ffffff',
        text = '#000000',
        border = '#dddddd',
        inputBackground = '#f5f5f5',
        accent = '#2196f3'
    },
    twilight = {
        background = '#2c2f33',
        text = '#99aab5',
        border = '#23272a',
        inputBackground = '#36393f',
        accent = '#7289da'
    },
    cyber = {
        background = '#0a192f',
        text = '#64ffda',
        border = '#112240',
        inputBackground = '#0a192f',
        accent = '#64ffda'
    },
    neon = {
        background = '#000000',
        text = '#ff00ff',
        border = '#00ff00',
        inputBackground = '#1a1a1a',
        accent = '#00ffff'
    },
    azure = {
        background = '#f0f8ff',
        text = '#000080',
        border = '#b0c4de',
        inputBackground = '#e6f3ff',
        accent = '#4169e1'
    }
}

function SetTheme(themeName)
    local theme = themes[themeName]
    if theme then
        SendNUIMessage({
            type = 'setTheme',
            theme = theme
        })
        SetResourceKvp('guidebook_theme', themeName)
    end
end

-- Point Management
local PointManager = {
    initialized = false
}

function PointManager:Initialize()
    if self.initialized then return end
    self:RegisterEvents()
    self:LoadPoints()
    self.initialized = true 
end

function PointManager:LoadPoints()
    TriggerServerEvent('guidebook:fetchPoints')
end

function PointManager:RegisterEvents()
    RegisterNetEvent('guidebook:receivePoints')
    AddEventHandler('guidebook:receivePoints', function(points)
        for _, point in pairs(points) do
            CreateHelpPoint(point)
        end
    end)
end

-- UI Functions
function ShowUI(data)
    SetNuiFocus(true, true)
    SendNUIMessage({
        type = "show",
        data = data
    })
end

function HideUI()
    SetNuiFocus(false, false)
    SendNUIMessage({
        type = "hide"
    })
end

function OpenGuidebook(pageKey)
    ShowUI({pageKey = pageKey})
    SendNUIMessage({
        type = 'openGuidebook',
        page = pageKey
    })
    SetNuiFocus(true, true)
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

function CloseEditor()
    isEditing = false
    SendNUIMessage({
        type = 'closeEditor'
    })
    SetNuiFocus(false, false)
end

-- Admin Panel Functions
function OpenAdminPanel()
    SafeNUIOperation(function()
        isAdminPanelOpen = true
        SendNUIMessage({
            type = 'openAdminPanel'
        })
        SetNuiFocus(true, true)
        print('^2[Guidebook]^7: Admin panel opened successfully')
    end, function()
        isAdminPanelOpen = false
        SetNuiFocus(false, false)
    end)
end

function CloseAdminPanel()
    isAdminPanelOpen = false
    SendNUIMessage({
        type = 'closeAdminPanel'
    })
    SetNuiFocus(false, false)
end

-- Help Point Functions
function CreateHelpPoint(data)
    if not data.coords then return end
    
    local point = {
        id = data.id,
        name = data.name,
        coords = json.decode(data.coords),
        type = data.type,
        blipSprite = data.blip_sprite,
        blipColor = data.blip_color,
        blipScale = data.blip_scale,
        canNavigate = data.can_navigate,
        pageKey = data.page_key,
        permissions = json.decode(data.permissions or '[]'),
    }

    if point.type == 'blip' then
        CreateBlip(point)
    elseif point.type == '3dtext' then
        Draw3DText(point.coords.x, point.coords.y, point.coords.z, point.name)
    elseif point.type == 'marker' then
        DrawMarker(1, point.coords.x, point.coords.y, point.coords.z - 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 255, 255, 255, 100)
    end
end

-- Website Functions
function OpenWebsite(url)
    SendNUIMessage({
        type = 'openWebsite',
        url = url
    })
    SetNuiFocus(true, true)
end

-- Search Functions
function SearchContent(query)
    if #query < 2 then 
        searchResults = {}
        return
    end
    TriggerServerEvent('guidebook:search', query)
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

-- Register All Events
RegisterNetEvent('guidebook:receiveSearchResults')
AddEventHandler('guidebook:receiveSearchResults', function(results)
    searchResults = results
    SendNUIMessage({
        type = 'showSearchResults',
        results = results
    })
end)

RegisterNetEvent('guidebook:receiveCategories')
AddEventHandler('guidebook:receiveCategories', function(categories)
    Categories = categories
end)

RegisterNetEvent('guidebook:receivePages')
AddEventHandler('guidebook:receivePages', function(pages)
    Pages = pages
end)

RegisterNetEvent('guidebook:pointUpdated')
AddEventHandler('guidebook:pointUpdated', function(pointData)
    if blips[pointData.id] then
        RemoveBlip(pointData.id)
    end
    CreateBlip(pointData)
end)

RegisterNetEvent('guidebook:receivePoints')
AddEventHandler('guidebook:receivePoints', function(points)
    for _, point in pairs(points) do
        CreateHelpPoint(point)
    end
end)

RegisterNetEvent('guidebook:openGuidebook')
AddEventHandler('guidebook:openGuidebook', function(pageKey)
    OpenGuidebook(pageKey)
end)

RegisterNetEvent('guidebook:openAdmin')
AddEventHandler('guidebook:openAdmin', function()
    OpenEditor()
end)

RegisterNetEvent('guidebook:searchResults')
AddEventHandler('guidebook:searchResults', function(results)
    searchResults = results
    SendNUIMessage({
        type = 'updateSearchResults',
        results = results
    })
end)

-- Register All Commands
RegisterCommand('openwebsite', function(source, args)
    local url = args[1]
    OpenWebsite(url)
end)

RegisterCommand('settheme', function(source, args)
    local themeName = args[1]
    SetTheme(themeName)
end)

RegisterCommand('search', function(source, args)
    local query = table.concat(args, ' ')
    SearchContent(query)
end)

RegisterCommand(Config.Commands.Help, function()
    OpenGuidebook()
end)

RegisterCommand(Config.Commands.Admin, function()
    OpenEditor()
end)

RegisterCommand(Config.Commands.SendHelp, function(source, args)
    local targetId = tonumber(args[1])
    local pageKey = args[2]
    TriggerServerEvent('guidebook:sendHelp', targetId, pageKey)
end)

RegisterCommand(Config.Commands.Navigate, function(source, args)
    local pointKey = args[1]
    TriggerServerEvent('guidebook:navigateToPoint', pointKey)
end)

RegisterCommand('helpadmin', function()
    OpenAdminPanel()
end)

-- Add after all other RegisterCommand functions
RegisterCommand('resetui', function()
    print('^3[Guidebook]^7: Attempting to reset UI state...')
    isEditing = false
    isAdminPanelOpen = false
    SetNuiFocus(false, false)
    SendNUIMessage({
        type = 'forceClose'
    })
    print('^2[Guidebook]^7: UI state reset complete')
end, false)

-- Register All NUI Callbacks
RegisterNUICallback('close', function(data, cb)
    HideUI()
    if isEditing then
        isEditing = false
    end
    cb('ok')
end)

RegisterNUICallback('saveContent', function(data, cb)
    if not isEditing then return end
    TriggerServerEvent('guidebook:saveContent', data)
    isEditing = false
    cb('ok')
end)

RegisterNUICallback('closeEditor', function(data, cb)
    CloseEditor()
    cb('ok')
end)

RegisterNUICallback('closeAdminPanel', function(data, cb)
    CloseAdminPanel()
    cb('ok')
end)

RegisterNUICallback('search', function(data, cb)
    SearchContent(data.query)
    cb('ok')
end)

RegisterNUICallback('setTheme', function(data, cb)
    SetTheme(data.theme)
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

    -- Load saved theme
    local savedTheme = GetResourceKvpString('guidebook_theme')
    if savedTheme then
        SetTheme(savedTheme)
    end
end)

-- Cleanup Function
function CleanupResources()
    for pointId, blip in pairs(blips) do
        RemoveBlip(blip)
    end
    blips = {}
    helpPoints = {}
    isEditing = false
end

-- Resource Cleanup
AddEventHandler('onResourceStop', function(resourceName)
    if GetCurrentResourceName() == resourceName then
        CleanupResources()
    end
end)

-- Initialize Point Manager
PointManager:Initialize()