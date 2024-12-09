
SConfig = {}

SConfig.LogWebhook = '' -- Discord webhook URL for logging

function LogToDiscord(message)
    if SConfig.LogWebhook == '' then return end
    
    PerformHttpRequest(SConfig.LogWebhook, function(err, text, headers) end, 'POST', json.encode({
        username = 'Guidebook',
        content = message
    }), { ['Content-Type'] = 'application/json' })
end