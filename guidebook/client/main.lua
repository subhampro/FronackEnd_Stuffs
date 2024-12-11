local display = false

-- Safety command to force close UI
RegisterCommand('closeui', function()
    display = false
    SetNuiFocus(false, false)
    SendNUIMessage({
        type = "ui",
        status = false
    })
end, false)

RegisterCommand('help', function()
    -- Check if UI is ready before toggling
    SendNUIMessage({
        type = "checkUI"
    })
    Wait(100) -- Small wait to ensure UI responds
    SetDisplay(not display)
end, false)

RegisterNUICallback('close', function(data, cb)
    SetDisplay(false)
    cb('ok')
end)

RegisterNUICallback('uiReady', function(data, cb)
    cb('ok')
end)

function SetDisplay(bool)
    display = bool
    SetNuiFocus(bool, bool)
    SendNUIMessage({
        type = "ui",
        status = bool
    })
end

CreateThread(function()
    Wait(1000)
    TriggerEvent('chat:addSuggestion', '/help', 'Open the guidebook')
    TriggerEvent('chat:addSuggestion', '/closeui', 'Force close UI if stuck')
end)