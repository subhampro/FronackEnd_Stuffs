local display = false

RegisterCommand('help', function()
    SetDisplay(not display)
end)

RegisterNUICallback('close', function(data, cb)
    SetDisplay(false)
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
end)