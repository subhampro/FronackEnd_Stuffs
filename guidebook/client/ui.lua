
local function ShowUI(data)
    SetNuiFocus(true, true)
    SendNUIMessage({
        type = "show",
        data = data
    })
end

local function HideUI()
    SetNuiFocus(false, false)
    SendNUIMessage({
        type = "hide"
    })
end

RegisterNUICallback('close', function(data, cb)
    HideUI()
    cb('ok')
end)

-- Handle UI messages from server
RegisterNetEvent('guidebook:showUI')
AddEventHandler('guidebook:showUI', function(data)
    ShowUI(data)
end)