
-- First, check if last_check column exists, if not add it
SET @dbname = 'wordpres_test';
SET @tablename = 'users';
SET @columnname = 'last_check';
SET @preparedStatement = (SELECT IF(
  (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE
      TABLE_SCHEMA = @dbname
      AND TABLE_NAME = @tablename
      AND COLUMN_NAME = @columnname
  ) > 0,
  'SELECT "Column already exists."',
  CONCAT('ALTER TABLE ', @tablename, ' ADD COLUMN ', @columnname, ' datetime DEFAULT NULL AFTER last_seen;')
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Update licenses table structure if needed
CREATE TABLE IF NOT EXISTS `licenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `license_key` varchar(64) DEFAULT NULL,
  `machine_id` varchar(64) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `activated_at` datetime DEFAULT NULL,
  `expires_at` datetime DEFAULT NULL,
  `status` enum('unused','active','expired') DEFAULT 'unused',
  PRIMARY KEY (`id`),
  UNIQUE KEY `license_key` (`license_key`),
  KEY `machine_id` (`machine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Update users table if needed
ALTER TABLE `users` 
MODIFY COLUMN `first_seen` datetime DEFAULT CURRENT_TIMESTAMP,
MODIFY COLUMN `last_seen` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
MODIFY COLUMN `total_uses` int DEFAULT '1';

-- Add indexes if they don't exist
ALTER TABLE `users` 
ADD INDEX IF NOT EXISTS `idx_last_seen` (`last_seen`),
ADD INDEX IF NOT EXISTS `idx_first_seen` (`first_seen`);