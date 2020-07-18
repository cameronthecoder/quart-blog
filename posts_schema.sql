CREATE TABLE `posts` (
  `id` mediumint NOT NULL AUTO_INCREMENT,
  `title` varchar(150) NOT NULL,
  `image_url` varchar(80) NOT NULL,
  `slug` varchar(80) NOT NULL,
  `body` text NOT NULL,
  `draft` tinyint(1) DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
);