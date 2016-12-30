-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        5.0.96-community-nt - MySQL Community Edition (GPL)
-- 服务器操作系统:                      Win32
-- HeidiSQL 版本:                  8.2.0.4675
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- 导出  表 db_news.tongbu_device 结构
CREATE TABLE IF NOT EXISTS `tongbu_device` (
  `id` int(11) NOT NULL auto_increment,
  `device_name` varchar(50) default '0',
  `device_id` varchar(50) default NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- 正在导出表  db_news.tongbu_device 的数据：~6 rows (大约)
/*!40000 ALTER TABLE `tongbu_device` DISABLE KEYS */;
INSERT INTO `tongbu_device` (`id`, `device_name`, `device_id`) VALUES
	(1, 'iphone6plus', '64'),
	(2, 'iphone6', '32'),
	(3, 'iphone5', '16'),
	(4, 'iphone4', '5'),
	(5, 'newipad', '8'),
	(6, 'ipad', '2');
/*!40000 ALTER TABLE `tongbu_device` ENABLE KEYS */;


-- 导出  表 db_news.tongbu_wallpaper_category 结构
CREATE TABLE IF NOT EXISTS `tongbu_wallpaper_category` (
  `id` int(11) NOT NULL auto_increment,
  `category` varchar(50) default '0',
  `type_id` varchar(50) default '0',
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- 正在导出表  db_news.tongbu_wallpaper_category 的数据：~23 rows (大约)
/*!40000 ALTER TABLE `tongbu_wallpaper_category` DISABLE KEYS */;
INSERT INTO `tongbu_wallpaper_category` (`id`, `category`, `type_id`) VALUES
	(1, '美女', '3'),
	(2, '小清新', '18'),
	(3, '风景', '1'),
	(4, '静物', '102'),
	(5, '天生一对', '17'),
	(6, '节日', '19'),
	(7, '抽象', '103'),
	(8, '名车', '5'),
	(9, '潮流', '7'),
	(10, '创意', '4'),
	(11, '动漫', '2'),
	(12, '植物', '12'),
	(13, '萌宠', '6'),
	(14, '体育', '15'),
	(15, '科技', '13'),
	(16, '爱情', '9'),
	(17, '帅哥', '11'),
	(18, '影视', '8'),
	(19, '军事', '14'),
	(20, '游戏', '10'),
	(21, '文字控', '20'),
	(22, '主屏控', '21'),
	(23, '其他', '16');
/*!40000 ALTER TABLE `tongbu_wallpaper_category` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
