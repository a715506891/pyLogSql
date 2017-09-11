CREATE TABLE `tablename` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `a` INT(11) NOT NULL DEFAULT 0,
  `b` CHAR(11) NOT NULL DEFAULT '' COMMENT 'aa',
  PRIMARY KEY (`id`)
) ENGINE=INNODB AUTO_INCREMENT=1 #自增id开始值
 DEFAULT CHARSET=utf8 COMMENT='bbb'(SELECT id AS a,b FROM tablename1  ORDER BY RAND());
UPDATE tablename1 a INNER JOIN tablename b ON s.id=a.id SET a.b=s.b;
DROP TABLE tablename;
