# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2019/9/1 22:22'

import pymysql.cursors

class db(object):
    flag = True
    instant = None
    # flag = True
    def __new__(cls, *args, **kwargs):
        if cls.instant is None:
            cls.instant = super().__new__(cls)
        return cls.instant

    def __init__(self):
        if not db.flag:
            return
        db.flag = False
        sql1  = """
        CREATE TABLE if NOT EXISTS `class` (
  `class_name` varchar(50) COLLATE utf8_bin NOT NULL,
  `week_day` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `start_section` int(3) DEFAULT NULL,
  `section_num` int(3) DEFAULT NULL,
  `week_range` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `teacher` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `test_type` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `year` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `term` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`class_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
        """
        sql2 = """
        CREATE TABLE if NOT EXISTS `student_grade` (
  `class_name` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `class_type` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `grade` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `year` bigint(6) DEFAULT NULL,
  `term` tinyint(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
        """
        self.excute("drop table if exists class")
        self.excute(sql1)
        self.excute("drop table if exists student_grade")
        self.excute(sql2)


    def connect_db(self):
        # Connect to the database
        self.connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='123',
                                     db='spider',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

    def excute(self, sql):
        try:
            self.connect_db()
            with self.connection.cursor() as cursor:
                # Read a single record
                cursor.execute(sql)
                self.connection.commit()
                result = cursor.fetchone()
                self.connection.close()
                return result

        except Exception as e:
            self.connection.rollback()
            self.connection.close()
            return e



