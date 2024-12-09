
local helpPoints = {}
local blips = {}

-- Fetch help points from the server
RegisterNetEvent('guidebook:receivePoints')
AddEventHandler('guidebook:receivePoints', function(points)
    helpPoints = points
    for _, point in pairs(points) do
        CreateHelpPoint(point)
    end
end)

-- Create a help point
function CreateHelpPoint(point)
    if point.type == '3dtext' then
        Draw3DText(point.coords.x, point.coords.y, point.coords.z, point.name)
    elseif point.type == 'marker' then
        DrawMarker(1, point.coords.x, point.coords.y, point.coords.z - 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 255, 255, 255, 100)
    end
    if point.type == 'blip' and not blips[point.id] then
        CreateBlip(point)
    end
end

-- Create a blip
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
end

-- Command to navigate to a help point
RegisterCommand('pointgps', function(source, args)
    local pointKey = args[1]
    TriggerServerEvent('guidebook:navigateToPoint', pointKey)
end)