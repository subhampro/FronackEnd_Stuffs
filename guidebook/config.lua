Config = {}

Config.Debug = false
Config.DebugLevel = {
    'CRITICAL',
    'SUCCESS',
    'ERROR',
}

Config.Framework = 0 -- 0: Auto, 1: ESX, 2: QBCore, 3: Other
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
Config.UseFrameworkNotify = false

Config.FrameworkTriggers = {
    resourceName = '',
    load = '',
    notify = '',
}

Config.IFrameInsertIntoPage = false