local helpDisplay = false
local adminDisplay = false

RegisterCommand("help", function()
    SetDisplay("help", not helpDisplay)
end, false)

RegisterCommand("helpadmin", function()
    SetDisplay("admin", not adminDisplay)
end, false)

function SetDisplay(menuType, bool)
    if menuType == "help" then
        helpDisplay = bool
    else
        adminDisplay = bool
    end
    
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
