/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80035
 Source Host           : localhost:3306
 Source Schema         : exam

 Target Server Type    : MySQL
 Target Server Version : 80035
 File Encoding         : 65001

 Date: 03/01/2024 18:48:32
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for exam
-- ----------------------------
DROP TABLE IF EXISTS `exam`;
CREATE TABLE `exam`  (
  `examid` int NOT NULL AUTO_INCREMENT COMMENT '考试ID',
  `examname` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '考试名',
  `examtype` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '考试类型',
  `examstart` datetime NOT NULL COMMENT '考试开始时间',
  `examend` datetime NOT NULL COMMENT '考试结束时间',
  `time` int NOT NULL COMMENT '时间(分钟)',
  `scores` int NULL DEFAULT NULL COMMENT '得分',
  PRIMARY KEY (`examid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of exam
-- ----------------------------
INSERT INTO `exam` VALUES (1, '第一次期中考试', '英语', '2023-12-29 08:00:00', '2023-12-29 10:00:00', 120, NULL);
INSERT INTO `exam` VALUES (2, '第一次期中考试', '数学', '2023-12-29 08:00:00', '2023-12-29 10:00:00', 120, NULL);

-- ----------------------------
-- Table structure for exam_1
-- ----------------------------
DROP TABLE IF EXISTS `exam_1`;
CREATE TABLE `exam_1`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '试题id',
  `score` int NULL DEFAULT NULL COMMENT '试题分数',
  `title` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '题号',
  `info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '试题详情',
  `radio` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '单选',
  `check` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '多选',
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '填空',
  `answer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '答案',
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '试题类型',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '第一次英语期中考试' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of exam_1
-- ----------------------------
INSERT INTO `exam_1` VALUES (1, 4, '第1题', 'What is the opposite of the word \"hot\"?', '{\'A\': \'Cold\', \'B\': \'Warm\', \'C\': \'Cool\', \'D\': \'Hotter\'}', NULL, NULL, 'A', '单选题');
INSERT INTO `exam_1` VALUES (2, 4, '第2题', 'What does the abbreviation \"DIY\" stand for?', '{\'A\': \'Digital In You\', \'B\': \'Do It Yourself\', \'C\': \'Download It Yourself\', \'D\': \'Divide It Yourself\'}', NULL, NULL, 'B', '单选题');
INSERT INTO `exam_1` VALUES (3, 4, '第3题', 'Which word is an antonym of the word \"happy\"?', '{\'A\': \'Sad\', \'B\': \'Angry\', \'C\': \'Excited\', \'D\': \'Tired\'}', NULL, NULL, 'A', '单选题');
INSERT INTO `exam_1` VALUES (4, 4, '第4题', 'Which of the following words is a preposition?', '{\'A\': \'Dog\', \'B\': \'Under\', \'C\': \'Sleep\', \'D\': \'Tree\'}', NULL, NULL, 'A', '单选题');
INSERT INTO `exam_1` VALUES (5, 4, '第5题', 'What is the plural form of the word \"child\"?', '{\'A\': \'Child\', \'B\': \'Childrens\', \'C\': \'Childs\', \'D\': \'Children\'}', NULL, NULL, 'D', '单选题');
INSERT INTO `exam_1` VALUES (6, 4, '第6题', 'What is the verb in the sentence \"I am running in the park\"?', '{\'A\': \'I\', \'B\': \'Am\', \'C\': \'Running\', \'D\': \'Park\'}', NULL, NULL, 'C', '单选题');
INSERT INTO `exam_1` VALUES (7, 4, '第7题', 'Which of the following words is a synonym of the word \"happy\"?', '{\'A\': \'Sad\', \'B\': \'Angry\', \'C\': \'Joyful\', \'D\': \'Tired\'}', NULL, NULL, 'C', '单选题');
INSERT INTO `exam_1` VALUES (8, 4, '第8题', 'What is the adverb in the sentence \"She sings beautifully\"?', '{\'A\': \'She\', \'B\': \'Sings\', \'C\': \'Beautifully\', \'D\': \'None of the above\'}', NULL, NULL, 'C', '单选题');
INSERT INTO `exam_1` VALUES (9, 4, '第9题', 'Which of the following words is a conjunction?', '{\'A\': \'Dog\', \'B\': \'And\', \'C\': \'Run\', \'D\': \'Tree\'}', NULL, NULL, 'B', '单选题');
INSERT INTO `exam_1` VALUES (10, 4, '第10题', 'What color is the apple', '{\'A\': \'Red\', \'B\': \'Yellow\', \'C\': \'Black\', \'D\': \'Blue\'}', NULL, NULL, 'A', '单选题');
INSERT INTO `exam_1` VALUES (11, 4, '第11题', 'What is the capital city of France?', '{\'A\': \'Paris\', \'B\': \'London\', \'C\': \'Toronto\', \'D\': \'Sydney\'}', NULL, NULL, 'A', '单选题');
INSERT INTO `exam_1` VALUES (12, 4, '第12题', 'Which of the following is not a primary color?', '{\'A\': \'Red\', \'B\': \'Green\', \'C\': \'Blue\', \'D\': \'Yellow-Green\'}', NULL, NULL, 'D', '单选题');
INSERT INTO `exam_1` VALUES (13, 4, '第13题', 'What is the opposite of the word \"fast\"?', '{\'A\': \'Slow\', \'B\': \'Quick\', \'C\': \'Speedy\', \'D\': \'Rapid\'}', NULL, NULL, 'A', '单选题');
INSERT INTO `exam_1` VALUES (14, 4, '第14题', 'Which of the following words is a pronoun?', '{\'A\': \'Table\', \'B\': \'He\', \'C\': \'Run\', \'D\': \'Tree\'}', NULL, NULL, 'B', '单选题');
INSERT INTO `exam_1` VALUES (15, 4, '第15题', 'What is the comparative form of the word \"big\"?', '{\'A\': \'Bigger\', \'B\': \'Biggest\', \'C\': \'Bigly\', \'D\': \'Bigest\'}', NULL, NULL, 'A', '单选题');
INSERT INTO `exam_1` VALUES (16, 4, '第16题', 'What\'s the rainbow made of?', NULL, '{\'A\': \'Light\', \'B\': \'Water\', \'C\': \'Plants\', \'D\': \'Wood\'}', NULL, 'AB', '多选题');
INSERT INTO `exam_1` VALUES (17, 4, '第17题', 'Which of the following are programming languages?', NULL, '{\'A\': \'Java\', \'B\': \'Python\', \'C\': \'JavaScript\', \'D\': \'HTML\'}', NULL, 'ABC', '多选题');
INSERT INTO `exam_1` VALUES (18, 4, '第18题', 'Which of the following are types of renewable energy?', NULL, '{\'A\': \'Solar\', \'B\': \'Nuclear\', \'C\': \'Wind\', \'D\': \'Coal\'}', NULL, 'AC', '多选题');
INSERT INTO `exam_1` VALUES (19, 4, '第19题', 'Which of the following are mammals?', NULL, '{\'A\': \'Whale\', \'B\': \'Shark\', \'C\': \'Kangaroo\', \'D\': \'Eagle\'}', NULL, 'AC', '多选题');
INSERT INTO `exam_1` VALUES (20, 4, '第20题', 'Which of the following are countries in Europe?', NULL, '{\'A\': \'Canada\', \'B\': \'Mexico\', \'C\': \'Germany\', \'D\': \'Brazil\'}', NULL, 'CD', '多选题');
INSERT INTO `exam_1` VALUES (21, 4, '第21题', 'Which of the following are planets in our solar system?', NULL, '{\'A\': \'Jupiter\', \'B\': \'Mars\', \'C\': \'Pluto\', \'D\': \'Saturn\'}', NULL, 'ABD', '多选题');
INSERT INTO `exam_1` VALUES (22, 4, '第22题', 'Which of the following are tools used in gardening?', NULL, '{\'A\': \'Hammer\', \'B\': \'Shovel\', \'C\': \'Lawnmower\', \'D\': \'Drill\'}', NULL, 'BC', '多选题');
INSERT INTO `exam_1` VALUES (23, 4, '第23题', 'Which of the following are primary colors?', NULL, '{\'A\': \'Red\', \'B\': \'Orange\', \'C\': \'Yellow\', \'D\': \'Purple\'}', NULL, 'AC', '多选题');
INSERT INTO `exam_1` VALUES (24, 4, '第24题', 'Which of the following are parts of the human body?', NULL, '{\'A\': \'Liver\', \'B\': \'Leaf\', \'C\': \'Finger\', \'D\': \'Apple\'}', NULL, 'AC', '多选题');
INSERT INTO `exam_1` VALUES (25, 4, '第25题', 'Which of the following are programming paradigms?', NULL, '{\'A\': \'Object-Oriented\', \'B\': \'Functional\', \'C\': \'Imperative\', \'D\': \'Responsive\'}', NULL, 'ABC', '多选题');

-- ----------------------------
-- Table structure for userexam
-- ----------------------------
DROP TABLE IF EXISTS `userexam`;
CREATE TABLE `userexam`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `examid` int NOT NULL COMMENT '考试ID',
  `userid` int NOT NULL COMMENT '用户ID',
  `score` int NOT NULL DEFAULT 0 COMMENT '得分',
  `con` int NOT NULL DEFAULT 0 COMMENT '考试状态（0未考，1考完，2超时）',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户考试列表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of userexam
-- ----------------------------
INSERT INTO `userexam` VALUES (1, 1, 1, 96, 1);
INSERT INTO `userexam` VALUES (2, 1, 2, 0, 0);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `userid` int NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `password` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '姓名',
  `classname` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '所属班级',
  `email` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '电子邮箱',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '联系电话',
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '性别',
  PRIMARY KEY (`userid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', '000000', '老六', '网络224', '2569845847@qq.com', '15448484545', '男');
INSERT INTO `users` VALUES (2, 'barbatos', '123456', '老八', '网络225', '2645484844@qq.com', '121548445445', '女');

SET FOREIGN_KEY_CHECKS = 1;
