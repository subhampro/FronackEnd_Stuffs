RegisterServerEvent('guidebook:openForPlayer')
AddEventHandler('guidebook:openForPlayer', function(playerId, pageKey)
    TriggerClientEvent('guidebook:open', playerId, pageKey)
end)

RegisterServerEvent('guidebook:navigateToPoint')
AddEventHandler('guidebook:navigateToPoint', function(pointKey)
    local source = source
    local point = MySQL.Sync.fetchAll('SELECT * FROM guidebook_points WHERE `key` = @key', {['@key'] = pointKey})[1]
    if point and point.can_navigate then
        TriggerClientEvent('guidebook:setGPS', source, json.decode(point.coords))
    end
end)