
local function DebugLog(level, message)
    if not Config.Debug then return end
    
    for _, allowedLevel in ipairs(Config.DebugLevel) do
        if level == allowedLevel then
            print(string.format('[Guidebook] [%s] %s', level, message))
            return
        end
    end
end

function DebugPoint(point)
    DebugLog('DEBUG', string.format('Point: %s, Type: %s, Coords: %s', 
        point.name, point.type, point.coords))
end