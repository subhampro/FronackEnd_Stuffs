
RegisterCommand(Config.Commands.Help, function()
    TriggerEvent('guidebook:open')
end)

RegisterCommand(Config.Commands.Admin, function()
    if IsPlayerAdmin() then
        TriggerEvent('guidebook:openAdmin') 
    else
        ShowNotification(Locales[Config.Locale]['no_permission'])
    end
end)

RegisterCommand(Config.Commands.Navigate, function(source, args)
    if #args < 1 then return end
    local pointKey = args[1]
    TriggerEvent('guidebook:navigateToPoint', pointKey)
end)

RegisterCommand(Config.Commands.SendHelp, function(source, args)
    if not IsPlayerAdmin() then return end
    
    local targetId = tonumber(args[1])
    local pageKey = args[2]
    
    if not targetId then return end
    TriggerServerEvent('guidebook:sendHelp', targetId, pageKey)
end)