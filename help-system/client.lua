local display = false

RegisterCommand("help", function()
    SetDisplay("help", not display)
end, false)

RegisterCommand("helpadmin", function()
    SetDisplay("admin", not display)
end, false)

function SetDisplay(menuType, bool)
    display = bool
    SetNuiFocus(bool, bool)
    SendNUIMessage({
        type = menuType,
        display = bool
    })
end

RegisterNUICallback("closeMenu", function(data, cb)
    SetDisplay("help", false)
    SetDisplay("admin", false)
    cb('ok')
end)
