
local isAdminPanelOpen = false

-- Open the admin panel
function OpenAdminPanel()
    isAdminPanelOpen = true
    SendNUIMessage({
        type = 'openAdminPanel'
    })
    SetNuiFocus(true, true)
end

-- Close the admin panel
function CloseAdminPanel()
    isAdminPanelOpen = false
    SendNUIMessage({
        type = 'closeAdminPanel'
    })
    SetNuiFocus(false, false)
end

-- Command to open the admin panel
RegisterCommand('helpadmin', function()
    OpenAdminPanel()
end)

-- NUI callback for closing the admin panel
RegisterNUICallback('closeAdminPanel', function(data, cb)
    CloseAdminPanel()
    cb('ok')
end)