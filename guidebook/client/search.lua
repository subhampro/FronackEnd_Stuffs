
local searchResults = {}

-- Search content
function SearchContent(query)
    if not query then return end
    TriggerServerEvent('guidebook:searchContent', query)
end

-- Receive search results from the server
RegisterNetEvent('guidebook:receiveSearchResults')
AddEventHandler('guidebook:receiveSearchResults', function(results)
    searchResults = results
    SendNUIMessage({
        type = 'showSearchResults',
        results = results
    })
end)

-- Command to search content
RegisterCommand('search', function(source, args)
    local query = table.concat(args, ' ')
    SearchContent(query)
end)