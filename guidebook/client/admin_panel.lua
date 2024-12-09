local isAdminPanelOpen = false
local Categories = {}
local Pages = {}

-- Fetch categories from the server
RegisterNetEvent('guidebook:receiveCategories')
AddEventHandler('guidebook:receiveCategories', function(categories)
    Categories = categories
end)

-- Fetch pages from the server
RegisterNetEvent('guidebook:receivePages')
AddEventHandler('guidebook:receivePages', function(pages)
    Pages = pages
end)

-- Open the admin panel
function OpenAdminPanel()
    isAdminPanelOpen = true
    local data = {
        type = 'openAdminPanel'
    }
    SendNUIMessage(data)
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