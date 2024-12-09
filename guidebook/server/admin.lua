
local function HasAdminPermission(source)
    local player = GetPlayer(source)
    return IsPlayerAdmin(player)
end

RegisterNetEvent('guidebook:saveCategory')
AddEventHandler('guidebook:saveCategory', function(category)
    local source = source
    if not HasAdminPermission(source) then
        return
    end

    MySQL.Async.execute('INSERT INTO guidebook_categories (name, description, `order`, permissions) VALUES (?, ?, ?, ?)',
        {category.name, category.description, category.order, json.encode(category.permissions)})
    
    LogToDiscord(string.format('Category created by %s: %s', GetPlayerName(source), category.name))
end)

RegisterNetEvent('guidebook:savePage')
AddEventHandler('guidebook:savePage', function(page)
    local source = source
    if not HasAdminPermission(source) then
        return
    end

    MySQL.Async.execute('INSERT INTO guidebook_pages (category_id, title, content, `key`, `order`, permissions) VALUES (?, ?, ?, ?, ?, ?)',
        {page.category_id, page.title, page.content, page.key, page.order, json.encode(page.permissions)})
    
    LogToDiscord(string.format('Page created by %s: %s', GetPlayerName(source), page.title))
end)