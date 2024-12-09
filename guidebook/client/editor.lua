
local isEditing = false

-- Open the editor
function OpenEditor(data)
    isEditing = true
    SendNUIMessage({
        type = 'openEditor',
        data = data
    })
    SetNuiFocus(true, true)
end

-- Close the editor
function CloseEditor()
    isEditing = false
    SendNUIMessage({
        type = 'closeEditor'
    })
    SetNuiFocus(false, false)
end

-- NUI callback for saving content
RegisterNUICallback('saveContent', function(data, cb)
    if not isEditing then return end
    TriggerServerEvent('guidebook:saveContent', data)
    isEditing = false
    cb('ok')
end)

-- NUI callback for closing the editor
RegisterNUICallback('closeEditor', function(data, cb)
    CloseEditor()
    cb('ok')
end)