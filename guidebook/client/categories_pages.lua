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

-- Open the guidebook with a specific page
function OpenGuidebook(pageKey)
    local data = {
        type = 'openGuidebook',
        page = pageKey
    }
    SendNUIMessage(data)
    SetNuiFocus(true, true)
end

-- Command to open the guidebook
RegisterCommand('help', function()
    OpenGuidebook()
end)