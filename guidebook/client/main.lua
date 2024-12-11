local display = false

-- Debug function
local function Debug(msg)
    print('^3[Guidebook Debug]^7 ' .. msg)
end

RegisterCommand('closeui', function()
    Debug('Attempting to close UI...')
    display = false
    SetNuiFocus(false, false)
    SendNUIMessage({
        type = "ui",
        status = false
    })
    Debug('UI closed and focus reset')
end, false)

RegisterCommand('help', function()
    Debug('Help command triggered')
    SetDisplay(not display)
    Debug('Display state: ' .. tostring(display))
end, false)

RegisterNUICallback('close', function(data, cb)
    Debug('Close callback received from UI')
    display = false
    SetNuiFocus(false, false)
    SendNUIMessage({
        type = "ui",
        status = false
    })
    Debug('UI closed via close button')
    cb('ok')
end)

RegisterNUICallback('uiReady', function(data, cb)
    Debug('UI Ready callback received')
    cb('ok')
end)

function SetDisplay(bool)
    display = bool
    SetNuiFocus(bool, bool)
    SendNUIMessage({
        type = "ui",
        status = bool
    })
    Debug('Display set to: ' .. tostring(bool))
end

CreateThread(function()
    Wait(1000)
    TriggerEvent('chat:addSuggestion', '/help', 'Open the guidebook')
    TriggerEvent('chat:addSuggestion', '/closeui', 'Force close UI if stuck')
    Debug('Resource started and commands registered')
end)