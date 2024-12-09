
local isEditing = false

function OpenEditor(data)
    isEditing = true
    SendNUIMessage({
        type = 'openEditor',
        data = data
    })
    SetNuiFocus(true, true)
end

function CloseEditor()
    isEditing = false
    SendNUIMessage({
        type = 'closeEditor'
    })
    SetNuiFocus(false, false)
end

RegisterNUICallback('saveContent', function(data, cb)
    if not isEditing then return end
    TriggerServerEvent('guidebook:saveContent', data)
    isEditing = false
    cb('ok')
end)

RegisterNUICallback('closeEditor', function(data, cb)
    CloseEditor()
    cb('ok')
end)