
Translations = {}

function LoadTranslations(locale)
    if not Locales[locale] then
        print('^1[ERROR] Invalid locale: ' .. locale)
        return false
    end
    
    Translations = Locales[locale]
    return true
end

function T(key, ...)
    if not Translations[key] then
        return 'Missing translation: ' .. key
    end
    
    return string.format(Translations[key], ...)
end