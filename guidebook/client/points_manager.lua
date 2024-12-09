local PointManager = {}

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

PointManager:Initialize()