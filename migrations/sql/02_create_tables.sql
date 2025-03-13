
-- ファイルタイプマスターテーブル (documents スキーマ)
CREATE TABLE `documents`.`file_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `extension` varchar(50) NOT NULL COMMENT 'ファイルの拡張子',
  `description` varchar(255) NOT NULL COMMENT '拡張子の説明',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_extension` (`extension`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ファイルの拡張子に関する情報';

-- タグマスターテーブル (documents スキーマ)
CREATE TABLE `documents`.`tags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT 'タグ名',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='タグに関するマスター';

-- ファイル情報テーブル (documents スキーマ)
CREATE TABLE `documents`.`files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) NOT NULL COMMENT 'ファイル名',
  `display_name` varchar(255) NOT NULL COMMENT '表示名',
  `url` varchar(1000) NOT NULL COMMENT 'URL',
  `file_type_id` int NOT NULL COMMENT 'ファイル形式',
  `file_size` bigint NOT NULL COMMENT 'ファイルサイズ(バイト)',
  `is_template` tinyint(1) NOT NULL DEFAULT '0' COMMENT '定型文書か否か',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `created_by` int NOT NULL COMMENT '作成者ID',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `updated_by` int NOT NULL COMMENT '更新者ID',
  `deleted_at` datetime DEFAULT NULL COMMENT '削除日時（ソフトデリート用）',
  PRIMARY KEY (`id`),
  KEY `idx_file_type` (`file_type_id`),
  KEY `idx_created_by` (`created_by`),
  KEY `idx_updated_by` (`updated_by`),
  KEY `idx_deleted_at` (`deleted_at`),
  CONSTRAINT `fk_files_file_type` FOREIGN KEY (`file_type_id`) REFERENCES `documents`.`file_types` (`id`),
  CONSTRAINT `fk_files_created_by` FOREIGN KEY (`created_by`) REFERENCES `auth`.`manager_users` (`id`),
  CONSTRAINT `fk_files_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `auth`.`manager_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ファイルの情報を格納する';

-- ファイルとタグの中間テーブル (documents スキーマ)
CREATE TABLE `documents`.`file_tags` (
  `file_id` int NOT NULL COMMENT 'fileのid',
  `tag_id` int NOT NULL COMMENT 'タグid',
  PRIMARY KEY (`file_id`,`tag_id`),
  KEY `idx_tag_id` (`tag_id`),
  CONSTRAINT `fk_file_tags_file_id` FOREIGN KEY (`file_id`) REFERENCES `documents`.`files` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_file_tags_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `documents`.`tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ファイルについているタグの情報';

-- auth スキーマに管理者ユーザーテーブルを作成
CREATE TABLE `auth`.`manager_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL COMMENT 'ユーザー名',
  `password_hash` varchar(255) NOT NULL COMMENT 'ハッシュ化パスワード',
  `role_name` varchar(100) NOT NULL COMMENT '役務名',
  `last_login` datetime DEFAULT NULL COMMENT '最終ログイン日時',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管理者ユーザーの管理テーブル';
