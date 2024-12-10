
function SendDiscordLog(action, data)
    if not Config.DiscordWebhook then return end
    
    local embedData = {
        {
            ["title"] = "Guidebook Action: " .. action,
            ["description"] = FormatLogMessage(data),
            ["color"] = 3447003,
            ["footer"] = {
                ["text"] = "FiveM Guidebook | " .. os.date("%Y-%m-%d %H:%M:%S")
            }
        }
    }

    PerformHttpRequest(Config.DiscordWebhook, function(err, text, headers) end, 'POST', 
        json.encode({username = "Guidebook", embeds = embedData}), 
        { ['Content-Type'] = 'application/json' })
end

function FormatLogMessage(data)
    if Config.Debug.level > 0 then
        print(json.encode(data, {indent = true}))
    end
    return json.encode(data)
end