
local isAdminPanelOpen = false

function OpenAdminPanel()
    isAdminPanelOpen = true
    SendNUIMessage({
        type = 'openAdminPanel'
    })
    SetNuiFocus(true, true)
end

function CloseAdminPanel()
    isAdminPanelOpen = false
    SendNUIMessage({
        type = 'closeAdminPanel'
    })
    SetNuiFocus(false, false)
end

RegisterNUICallback('closeAdminPanel', function(data, cb)
    CloseAdminPanel()
    cb('ok')
end)

RegisterCommand('helpadmin', function()
    OpenAdminPanel()
end)