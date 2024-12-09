local function InitializeDatabase()
    MySQL.ready(function()
        -- Create tables if they don't exist
        MySQL.Async.execute([[
            CREATE TABLE IF NOT EXISTS `guidebook_categories` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `name` varchar(50) NOT NULL,
                `description` text,
                `order` int(11) DEFAULT 0,
                `permissions` text,
                PRIMARY KEY (`id`)
            );
        ]])

        MySQL.Async.execute([[
            CREATE TABLE IF NOT EXISTS `guidebook_pages` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `category_id` int(11) NOT NULL,
                `title` varchar(100) NOT NULL,
                `content` text NOT NULL,
                `key` varchar(50) NOT NULL,
                `order` int(11) DEFAULT 0,
                `permissions` text,
                PRIMARY KEY (`id`),
                FOREIGN KEY (`category_id`) REFERENCES `guidebook_categories`(`id`)
            );
        ]])

        MySQL.Async.execute([[
            CREATE TABLE IF NOT EXISTS `guidebook_points` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `name` varchar(50) NOT NULL,
                `key` varchar(50) NOT NULL,
                `coords` varchar(50) NOT NULL,
                `type` varchar(20) NOT NULL,
                `page_key` varchar(50),
                `can_navigate` tinyint(1) DEFAULT 0,
                `permissions` text,
                PRIMARY KEY (`id`)
            );
        ]])

        MySQL.Async.execute([[
            ALTER TABLE guidebook_points 
            ADD COLUMN IF NOT EXISTS blip_sprite int(11) DEFAULT 1,
            ADD COLUMN IF NOT EXISTS blip_color int(11) DEFAULT 0,
            ADD COLUMN IF NOT EXISTS blip_scale float DEFAULT 1.0
        ]])
    end)
end