-- pkulaw.account_table definition

CREATE TABLE `account_table` (
  `id` int NOT NULL AUTO_INCREMENT,
`username` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户名',
`password` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户密码',
`phone` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_login` int DEFAULT NULL COMMENT '是否登录，cookie是否可用',
  `user_type` int NOT NULL COMMENT '用户类型 1:VIP账户，2:普通用户',
  `last_login_time` datetime DEFAULT NULL COMMENT '上次登录时间',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='北大法宝账号表';


-- pkulaw.cookie_table definition

CREATE TABLE `cookie_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cookie_type` int NOT NULL COMMENT 'cookie类型，游客cookie, m站登录cookie, www站登录cookie等',
  `cookie` text COLLATE utf8mb4_unicode_ci,
  `login_time` datetime DEFAULT NULL COMMENT '登录时间',
  `user_id` int DEFAULT NULL COMMENT '账号id',
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='账号cookie资源表';


-- pkulaw.law_info_table definition

CREATE TABLE `law_info_table` (
`law_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
`title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '标题',
`issue_department` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '制定机关',
`issue_date` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '公布日期',
`implement_date` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '实施日期',
`timeliness_dic` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '时效性',
`effectiveness_dic` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '效力位阶',
`category` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '法规类型',
  `content` longtext COLLATE utf8mb4_unicode_ci COMMENT '法规正文',
PRIMARY KEY (`law_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='法律详情信息表';


-- pkulaw.law_id_table definition

CREATE TABLE `law_id_table` (
`law_info` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '法条详情id',
`title` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '法条法规标题',
  `is_crawled` int DEFAULT NULL COMMENT '是否采集',
PRIMARY KEY (`law_info`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='北大法宝 法规详情id表';