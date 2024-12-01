-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 02, 2024 at 03:08 AM
-- Server version: 8.0.39
-- PHP Version: 8.1.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wordpres_test`
--

-- --------------------------------------------------------

--
-- Table structure for table `licenses`
--

CREATE TABLE `licenses` (
  `id` int NOT NULL,
  `license_key` varchar(64) NOT NULL,
  `machine_id` varchar(64) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `activated_at` datetime DEFAULT NULL,
  `expires_at` datetime DEFAULT NULL,
  `status` enum('unused','active','expired') DEFAULT 'unused'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `usage_stats`
--

CREATE TABLE `usage_stats` (
  `id` int NOT NULL,
  `user_id` varchar(32) NOT NULL,
  `event_type` varchar(50) NOT NULL,
  `system_info` varchar(255) DEFAULT NULL,
  `version` varchar(20) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `isp` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `usage_stats`
--

INSERT INTO `usage_stats` (`id`, `user_id`, `event_type`, `system_info`, `version`, `created_at`, `ip_address`, `country`, `region`, `city`, `isp`) VALUES
(4, '81b8e21070bfd0eb96f206dbeda983dd', 'startup', 'Windows 11', '1.0.0', '2024-12-02 02:22:12', NULL, NULL, NULL, NULL, NULL),
(5, '81b8e21070bfd0eb96f206dbeda983dd', 'start', 'Windows 11', '1.0.0', '2024-12-02 02:22:12', NULL, NULL, NULL, NULL, NULL),
(6, '81b8e21070bfd0eb96f206dbeda983dd', 'startup', 'Windows 11', '1.0.0', '2024-12-02 02:36:52', '202.8.112.89', 'India', 'West Bengal', 'Kolkata', NULL),
(7, '81b8e21070bfd0eb96f206dbeda983dd', 'start', 'Windows 11', '1.0.0', '2024-12-02 02:36:53', '202.8.112.89', 'India', 'West Bengal', 'Kolkata', NULL),
(8, '81b8e21070bfd0eb96f206dbeda983dd', 'startup', 'Windows 11', '1.0.0', '2024-12-02 02:49:38', '202.8.112.89', 'India', 'West Bengal', 'Kolkata', NULL),
(9, '81b8e21070bfd0eb96f206dbeda983dd', 'start', 'Windows 11', '1.0.0', '2024-12-02 02:49:39', '202.8.112.89', 'India', 'West Bengal', 'Kolkata', NULL),
(10, '81b8e21070bfd0eb96f206dbeda983dd', 'startup', 'Windows 11', '1.0.0', '2024-12-02 02:51:03', '202.8.112.89', 'India', 'West Bengal', 'Kolkata', NULL),
(11, '81b8e21070bfd0eb96f206dbeda983dd', 'start', 'Windows 11', '1.0.0', '2024-12-02 02:51:04', '202.8.112.89', 'India', 'West Bengal', 'Kolkata', NULL),
(12, '81b8e21070bfd0eb96f206dbeda983dd', 'startup', 'Windows 11', '1.0.0', '2024-12-02 02:54:05', '202.8.112.89', 'India', 'West Bengal', 'Kolkata', NULL),
(13, '81b8e21070bfd0eb96f206dbeda983dd', 'start', 'Windows 11', '1.0.0', '2024-12-02 02:54:06', '202.8.112.89', 'India', 'West Bengal', 'Kolkata', NULL),
(14, '81b8e21070bfd0eb96f206dbeda983dd', 'startup', 'Windows 11', '1.0.0', '2024-12-02 02:57:05', '202.8.112.89', 'India', 'West Bengal', 'Kolkata', NULL),
(15, '81b8e21070bfd0eb96f206dbeda983dd', 'start', 'Windows 11', '1.0.0', '2024-12-02 02:57:05', '202.8.112.89', 'India', 'West Bengal', 'Kolkata', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `user_id` varchar(32) NOT NULL,
  `first_seen` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  `total_uses` int DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `user_id`, `first_seen`, `last_seen`, `total_uses`) VALUES
(4, '81b8e21070bfd0eb96f206dbeda983dd', '2024-12-02 02:22:12', '2024-12-02 02:57:05', 12);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `licenses`
--
ALTER TABLE `licenses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `license_key` (`license_key`),
  ADD KEY `license_key_2` (`license_key`),
  ADD KEY `machine_id` (`machine_id`);

--
-- Indexes for table `usage_stats`
--
ALTER TABLE `usage_stats`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `created_at` (`created_at`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `last_seen` (`last_seen`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `licenses`
--
ALTER TABLE `licenses`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `usage_stats`
--
ALTER TABLE `usage_stats`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
