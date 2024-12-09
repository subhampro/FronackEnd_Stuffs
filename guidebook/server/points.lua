local function HasAdminPermission(source)
    local player = GetPlayer(source)
    return IsPlayerAdmin(player)
end

local function ValidatePoint(point)
    if not point.name or not point.coords then
        return false, 'Invalid point data'
    end
    if point.type == 'blip' and not point.blipSprite then
        return false, 'Invalid blip configuration'
    end
    return true
end

RegisterNetEvent('guidebook:createPoint')
AddEventHandler('guidebook:createPoint', function(point)
    local source = source
    if not HasAdminPermission(source) then return end
    
    local isValid, error = ValidatePoint(point)
    if not isValid then
        TriggerClientEvent('guidebook:showNotification', source, error)
        return
    end

    MySQL.Async.execute([[
        INSERT INTO guidebook_points 
        (name, `key`, coords, type, page_key, can_navigate, permissions) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ]], {
        point.name,
        point.key,
        json.encode(point.coords),
        point.type,
        point.page_key,
        point.can_navigate,
        json.encode(point.permissions)
    })

    TriggerClientEvent('guidebook:updatePoints', -1)
    LogToDiscord(string.format('Help point created by %s: %s', GetPlayerName(source), point.name))
end)

RegisterNetEvent('guidebook:deletePoint')
AddEventHandler('guidebook:deletePoint', function(pointId)
    local source = source
    if not HasAdminPermission(source) then return end

    MySQL.Async.execute('DELETE FROM guidebook_points WHERE id = ?', {pointId})
    TriggerClientEvent('guidebook:updatePoints', -1)
end)