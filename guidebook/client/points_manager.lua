
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
        blip = nil
    }
    
    if point.type == 'blip' then
        point.blip = AddBlipForCoord(point.coords.x, point.coords.y, point.coords.z)
        SetBlipSprite(point.blip, point.blipSprite)
        SetBlipColour(point.blip, point.blipColor)
        SetBlipScale(point.blip, point.blipScale)
        SetBlipAsShortRange(point.blip, true)
    end
    
    activePoints[point.id] = point
    return point
end

return PointManager