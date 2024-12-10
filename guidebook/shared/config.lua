Config = {}

Config.Debug = true
Config.DebugLevel = {
    'CRITICAL',
    'SUCCESS',
    'ERROR',
}

Config.Framework = 2 -- 0: Auto, 1: ESX, 2: QBCore, 3: Other
Config.Locale = 'en'

Config.Commands = {
    Help = 'help',
    SendHelp = 'sendhelp',
    Admin = 'helpadmin',
    Navigate = 'pointgps',
}

Config.Keys = {
    OpenGuidebook = 'F9',
    HelpPointOpen = 'E',
}

Config.RegisterOpenKey = 'F9'
Config.DisablePageContentCopy = false
Config.DisableDataPermissions = false
Config.UseFrameworkNotify = true

Config.FrameworkTriggers = {
    resourceName = 'qb-core',
    load = 'QBCore:GetObject',
    notify = 'QBCore:Notify'
}

Config.IFrameInsertIntoPage = false

return Config