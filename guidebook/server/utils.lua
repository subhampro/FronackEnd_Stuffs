
local Utils = {}

-- Permission checking
function Utils.HasPermission(source, permissions)
    if not permissions or #permissions == 0 then return true end
    
    local player = GetPlayer(source)
    if not player then return false end
    
    for _, perm in ipairs(permissions) do
        if Config.Framework == 1 then -- ESX
            if player.job.name == perm.job and player.job.grade >= perm.grade then
                return true
            end
        elseif Config.Framework == 2 then -- QBCore
            if player.PlayerData.job.name == perm.job and player.PlayerData.job.grade.level >= perm.grade then
                return true
            end
        end
    end
    return false
end

-- Debug logging
function Utils.DebugLog(level, message)
    if not Config.Debug then return end
    
    for _, allowedLevel in ipairs(Config.DebugLevel) do
        if level == allowedLevel then
            print(string.format('[Guidebook] [%s] %s', level, message))
            LogToDiscord(message)
            return
        end
    end
end

return Utils