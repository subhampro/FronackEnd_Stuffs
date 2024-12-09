local function DrawHelpPoint(point)
    local coords = json.decode(point.coords)
    
    if point.type == 'blip' then
        if not point.blip then
            point.blip = AddBlipForCoord(coords.x, coords.y, coords.z)
            SetBlipSprite(point.blip, point.blipSprite or 1)
            SetBlipColour(point.blip, point.blipColor or 0)
            SetBlipScale(point.blip, point.blipScale or 1.0)
            SetBlipAsShortRange(point.blip, true)
            BeginTextCommandSetBlipName("STRING")
            AddTextComponentString(point.name)
            EndTextCommandSetBlipName(point.blip)
        end
        return
    end
    
    local distance = #(GetEntityCoords(PlayerPedId()) - vector3(coords.x, coords.y, coords.z))
    
    if distance < Config.DrawDistance then
        if point.type == 'marker' then
            DrawMarker(1, coords.x, coords.y, coords.z, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                1.0, 1.0, 1.0, 255, 255, 255, 100, false, true, 2, false, nil, nil, false)
        elseif point.type == '3dtext' then
            Draw3DText(coords.x, coords.y, coords.z, point.name)
        end

        if distance < 2.0 then
            ShowHelpNotification(Locales[Config.Locale]['press_to_open'])
            if IsControlJustReleased(0, 38) then -- E key
                OpenGuidebook(point.page_key)
            end
        end
    end
end

CreateThread(function()
    while true do
        Wait(0)
        for _, point in pairs(helpPoints) do
            DrawHelpPoint(point)
        end
    end
end)