
local GuideBuilder = {}

function GuideBuilder:CreateCategory(data)
    if not data.name then return nil end
    
    local category = {
        name = data.name,
        description = data.description or '',
        order = data.order or 0,
        permissions = data.permissions or {},
        pages = {}
    }
    
    TriggerServerEvent('guidebook:saveCategory', category)
    return category
end

function GuideBuilder:CreatePage(data)
    if not data.title or not data.categoryId then return nil end
    
    local page = {
        category_id = data.categoryId,
        title = data.title,
        content = data.content or '',
        key = data.key or GeneratePageKey(data.title),
        order = data.order or 0,
        permissions = data.permissions or {}
    }
    
    TriggerServerEvent('guidebook:savePage', page)
    return page
end

function GuideBuilder:CreateHelpPoint(data)
    if not data.name or not data.coords then return nil end
    
    local point = {
        name = data.name,
        key = data.key or GeneratePointKey(data.name),
        coords = json.encode(data.coords),
        type = data.type or 'marker',
        page_key = data.pageKey,
        can_navigate = data.canNavigate or false,
        permissions = data.permissions or {}
    }
    
    TriggerServerEvent('guidebook:createPoint', point)
    return point
end

return GuideBuilder