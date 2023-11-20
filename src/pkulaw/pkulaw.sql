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
`law_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '法条详情id',
`title` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '法条法规标题',
  `is_crawled` int DEFAULT NULL COMMENT '是否采集',
PRIMARY KEY (`law_info`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='北大法宝 法规详情id表';


INSERT INTO pkulaw.account_table (username,password,phone,is_login,user_type,last_login_time) VALUES
('王建','DA2023da','15837466531',NULL,2,NULL),
('王大喜','wang2010','15658097781',NULL,2,NULL),
('张岩','da300033','18106516970',NULL,2,NULL),
('田浩','myhexintianhao','13124103006',NULL,2,NULL),
('张岩','da300033','18106516970',NULL,2,NULL),
('李翔','DA2023da','13588106946',NULL,2,NULL),
('萧炎','DA2023da','18850078996',NULL,2,NULL),
('吴丹丹','DA2023da','18910572403',NULL,2,NULL),
('王生','kul0714KUL','18666668362',NULL,2,NULL),
('杨惠泽','12345678','18234132630',NULL,2,NULL);
INSERT INTO pkulaw.account_table (username,password,phone,is_login,user_type,last_login_time) VALUES
('洪阳','ths123456','15757176746',NULL,2,NULL),
('张媛','qwa12345','17324607307',NULL,2,NULL),
('陈子扬','DA2023da','18106564013',NULL,2,NULL),
('张浙永','DA2023da','15858269033',NULL,2,NULL),
('张浙永','DA2023da','15858269033',NULL,2,NULL),
('张钶','DA2023da','17717088701',NULL,2,NULL),
('郑腾','DA2023da','15315725634',NULL,2,NULL),
('刘小璇','DA2023da','19168070268',NULL,2,NULL),
('梁旭东','DA2023da','13858871954',NULL,2,NULL),
('肖一丁','DA2023da','18758351880',NULL,2,NULL);
INSERT INTO pkulaw.account_table (username,password,phone,is_login,user_type,last_login_time) VALUES
('王启宁','DA2023da','18507046505',NULL,2,NULL),
('郭硕','DA2023da','18667931984',NULL,2,NULL),
('石南','DA2023da','15267047759',NULL,2,NULL),
('江凯睿','DA2023da','15370480224',NULL,2,NULL),
('陈丁同','DA2023da','181110673509',NULL,2,NULL),
('李高伟','DA2023da','15993219810',NULL,2,NULL),
('蒋锦春','DA2023da','18868107903',NULL,2,NULL),
('马骥','DA2023da','13777833633',NULL,2,NULL),
('ZL','zl910204','13738266127',NULL,2,NULL),
('吴梓唯','DA2023da','18983353651',NULL,2,NULL);
INSERT INTO pkulaw.account_table (username,password,phone,is_login,user_type,last_login_time) VALUES
('景思聪','DA2023da','15189821626',NULL,2,NULL),
('徐杨远翔','DA2023da','18811132057',NULL,2,NULL),
('顾树明','DA1234da','18851835805',NULL,2,NULL);