local display = false

CreateThread(function()
    Wait(500)
    SetDisplay(false) -- Force initial state
    Wait(500)
    SetDisplay(false) -- Force hide UI on resource start
    Wait(1000)
    TriggerEvent('chat:addSuggestion', '/help', 'Open the guidebook')
    TriggerEvent('chat:addSuggestion', '/closeui', 'Force close UI if stuck')
    Debug('Resource started and commands registered')
end)

-- Debug function
local function Debug(msg)
    print('^3[Guidebook Debug]^7 ' .. msg)
end

RegisterCommand('closeui', function()
    SetDisplay(false)
end, false)

RegisterCommand('help', function()
    Debug('Help command triggered')
    SetDisplay(not display)
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
    Wait(100) -- Add small delay to ensure NUI message is processed
end