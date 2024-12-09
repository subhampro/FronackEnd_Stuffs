local Pages = {}

local function LoadPages()
    local result = MySQL.Sync.fetchAll('SELECT * FROM guidebook_pages ORDER BY `order` ASC')
    for i=1, #result do
        result[i].permissions = json.decode(result[i].permissions or '[]')
    end
    return result
end

RegisterNetEvent('guidebook:fetchPages')
AddEventHandler('guidebook:fetchPages', function()
    local source = source
    local pages = LoadPages()
    TriggerClientEvent('guidebook:receivePages', source, pages)
end)

RegisterNetEvent('guidebook:createPage')
AddEventHandler('guidebook:createPage', function(data)
    local source = source
    if not HasAdminPermission(source) then return end
    
    MySQL.Async.execute('INSERT INTO guidebook_pages (category_id, title, content, `key`, `order`, permissions) VALUES (?, ?, ?, ?, ?, ?)',
        {data.category_id, data.title, data.content, data.key, data.order, json.encode(data.permissions)})
    
    TriggerClientEvent('guidebook:updatePages', -1)
end)

RegisterNetEvent('guidebook:editPage')
AddEventHandler('guidebook:editPage', function(data)
    local source = source
    if not HasAdminPermission(source) then return end
    
    MySQL.Async.execute('UPDATE guidebook_pages SET category_id = ?, title = ?, content = ?, `key` = ?, `order` = ?, permissions = ? WHERE id = ?',
        {data.category_id, data.title, data.content, data.key, data.order, json.encode(data.permissions), data.id})
    
    TriggerClientEvent('guidebook:updatePages', -1)
end)

RegisterNetEvent('guidebook:deletePage')
AddEventHandler('guidebook:deletePage', function(pageId)
    local source = source
    if not HasAdminPermission(source) then return end
    
    MySQL.Async.execute('DELETE FROM guidebook_pages WHERE id = ?', {pageId})
    TriggerClientEvent('guidebook:updatePages', -1)
end)