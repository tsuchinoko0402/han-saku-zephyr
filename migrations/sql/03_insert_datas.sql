
-- サンプルデータ投入（オプション）
INSERT INTO `documents`.`file_types` (`extension`, `description`) VALUES
('pdf', 'PDF形式'),
('docx', 'Microsoft Word文書'),
('xlsx', 'Microsoft Excel表計算'),
('pptx', 'Microsoft PowerPointプレゼンテーション');

INSERT INTO `documents`.`tags` (`name`) VALUES
('BVS'),
('CS'),
('BS'),
('VS'),
('RS'),
('指導者');

-- 初期管理者ユーザーの追加（本番環境ではパスワードを変更してください）
-- パスワードは「admin123」のハッシュ例です。本番環境では必ず変更してください。
INSERT INTO `auth`.`manager_users` (`username`, `password_hash`, `role_name`) VALUES
('admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', '管理者');
