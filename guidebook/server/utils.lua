local function IsPlayerAdmin(player)
    if not player then return false end
    
    if Config.Framework == 1 then -- ESX
        return player.getGroup() == 'admin' or player.getGroup() == 'superadmin'
    elseif Config.Framework == 2 then -- QBCore
        return player.PlayerData.admin
    else
        -- Add custom admin check here
        return false
    end
end

local function LogToDiscord(message)
    if SConfig.LogWebhook == '' then return end
    
    PerformHttpRequest(SConfig.LogWebhook, function(err, text, headers) end, 'POST', json.encode({
        username = 'Guidebook',
        content = message
    }), { ['Content-Type'] = 'application/json' })
end

local function GetPlayer(source)
    if Config.Framework == 1 then -- ESX
        return Framework.GetPlayerFromId(source)
    elseif Config.Framework == 2 then -- QBCore
        return Framework.Functions.GetPlayer(source)
    end
    return nil
end