
-- Open a website
function OpenWebsite(url)
    SendNUIMessage({
        type = 'openWebsite',
        url = url
    })
    SetNuiFocus(true, true)
end

-- Command to open a website
RegisterCommand('openwebsite', function(source, args)
    local url = args[1]
    OpenWebsite(url)
end)