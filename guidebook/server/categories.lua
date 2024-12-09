local Categories = {}

local function LoadCategories()
    local result = MySQL.Sync.fetchAll('SELECT * FROM guidebook_categories ORDER BY `order` ASC')
    for i=1, #result do
        result[i].permissions = json.decode(result[i].permissions or '[]')
    end
    return result
end

RegisterNetEvent('guidebook:fetchCategories')
AddEventHandler('guidebook:fetchCategories', function()
    local source = source
    local categories = LoadCategories()
    TriggerClientEvent('guidebook:receiveCategories', source, categories)
end)

RegisterNetEvent('guidebook:createCategory')
AddEventHandler('guidebook:createCategory', function(data)
    local source = source
    if not HasAdminPermission(source) then return end
    
    MySQL.Async.execute('INSERT INTO guidebook_categories (name, description, `order`, permissions) VALUES (?, ?, ?, ?)',
        {data.name, data.description, data.order, json.encode(data.permissions)})
    
    TriggerClientEvent('guidebook:updateCategories', -1)
end)