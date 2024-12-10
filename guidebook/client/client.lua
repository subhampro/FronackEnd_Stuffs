local QBCore = exports['qb-core']:GetCoreObject()
local ESX = nil
local helpPoints = {}
local isUIOpen = false

-- Initialize help points
RegisterNetEvent('guidebook:syncHelpPoints')
AddEventHandler('guidebook:syncHelpPoints', function(points)
    helpPoints = points
    CreateHelpPointBlips()
end)

-- UI Functions
function OpenGuidebook(pageId)
    if not isUIOpen then
        SetNuiFocus(true, true)
        SendNUIMessage({
            type = "openGuidebook",
            pageId = pageId
        })
        isUIOpen = true
    end
end

-- Help Point Management
function CreateHelpPointBlips()
    for _, point in pairs(helpPoints) do
        local blip = AddBlipForCoord(point.x, point.y, point.z)
        SetBlipSprite(blip, point.blip_sprite)
        SetBlipColour(blip, point.blip_color)
        SetBlipScale(blip, 0.8)
        SetBlipAsShortRange(blip, true)
        BeginTextCommandSetBlipName("STRING")
        AddTextComponentString(point.name)
        EndTextCommandSetBlipName(blip)
    end
end

-- Help Point Display
Citizen.CreateThread(function()
    while true do
        Citizen.Wait(0)
        local playerCoords = GetEntityCoords(PlayerPedId())
        
        for _, point in pairs(helpPoints) do
            DrawMarker(Config.HelpPointDefaults.markerType,
                point.x, point.y, point.z - 1.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                Config.HelpPointDefaults.markerSize.x,
                Config.HelpPointDefaults.markerSize.y,
                Config.HelpPointDefaults.markerSize.z,
                255, 255, 255, 100,
                false, true, 2, nil, nil, false)

            local distance = #(playerCoords - vector3(point.x, point.y, point.z))
            if distance < 2.0 then
                Draw3DText(point.x, point.y, point.z, point.name)
                if IsControlJustReleased(0, 38) then -- E key
                    OpenGuidebook(point.page_id)
                end
            end
        end
    end
end)

-- 3D Text Rendering
function Draw3DText(x, y, z, text)
    local onScreen, _x, _y = World3dToScreen2d(x, y, z)
    if onScreen then
        SetTextScale(0.35, 0.35)
        SetTextFont(4)
        SetTextProportional(1)
        SetTextColour(255, 255, 255, 255)
        SetTextEntry("STRING")
        SetTextCentre(1)
        AddTextComponentString(text)
        DrawText(_x, _y)
    end
end

-- Commands and Events
RegisterCommand('pointgps', function(source, args)
    local pointKey = args[1]
    if helpPoints[pointKey] then
        SetNewWaypoint(helpPoints[pointKey].x, helpPoints[pointKey].y)
    end
end)

-- Admin UI Functions
function OpenAdminPanel()
    SetNuiFocus(true, true)
    SendNUIMessage({
        type = "openAdminPanel"
    })
end

-- Admin Panel Functions
RegisterNUICallback('createHelpPoint', function(data, cb)
    local coords = GetEntityCoords(PlayerPedId())
    data.x = coords.x
    data.y = coords.y
    data.z = coords.z
    TriggerServerEvent('guidebook:createHelpPoint', data)
    cb('ok')
end)

RegisterNUICallback('saveTheme', function(data, cb)
    TriggerServerEvent('guidebook:saveCustomTheme', data)
    cb('ok')
end)

-- NUI Callbacks
RegisterNUICallback('closeGuidebook', function()
    SetNuiFocus(false, false)
    isUIOpen = false
end)