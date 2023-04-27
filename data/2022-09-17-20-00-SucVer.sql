/*
 Navicat Premium Data Transfer

 Source Server         : test
 Source Server Type    : MySQL
 Source Server Version : 50529
 Source Host           : localhost:3306
 Source Schema         : test

 Target Server Type    : MySQL
 Target Server Version : 50529
 File Encoding         : 65001

 Date: 17/09/2022 20:01:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for data_for_websites
-- ----------------------------
DROP TABLE IF EXISTS `data_for_websites`;
CREATE TABLE `data_for_websites`  (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `day` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `start_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `finish_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `event` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `level` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `acc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 175 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of data_for_websites
-- ----------------------------
INSERT INTO `data_for_websites` VALUES (147, '2022-09-24', '22:09', '22:09', '红色之旅', '0', 'admin');
INSERT INTO `data_for_websites` VALUES (146, '2022-09-23', '22:09', '22:09', '上学', '0', 'admin');
INSERT INTO `data_for_websites` VALUES (171, '2022-09-17', '19:09', '19:09', '实例', '0', 'zsc');
INSERT INTO `data_for_websites` VALUES (170, '2022-09-17', '19:09', '19:09', '实例', '0', 'zsc');
INSERT INTO `data_for_websites` VALUES (158, '2022-09-17', '19:09', '19:09', '上学', '0', 'None');
INSERT INTO `data_for_websites` VALUES (155, '2022-09-17', '17:09', '17:09', '上学', '0', 'None');
INSERT INTO `data_for_websites` VALUES (142, '2022-09-10', '22:09', '23:09', '上学', '0', 'admin');
INSERT INTO `data_for_websites` VALUES (148, '2022-09-24', '22:09', '22:09', '红色之旅', '0', 'admin');
INSERT INTO `data_for_websites` VALUES (172, '2022-09-17', '19:09', '19:09', '实例', '0', 'zsc');
INSERT INTO `data_for_websites` VALUES (173, '2022-09-17', '19:09', '19:09', '实例', '0', 'zsc');
INSERT INTO `data_for_websites` VALUES (174, '2022-09-17', '19:09', '19:09', '实例', '0', 'zsc');

-- ----------------------------
-- Table structure for share_user
-- ----------------------------
DROP TABLE IF EXISTS `share_user`;
CREATE TABLE `share_user`  (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `share_user` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `acc_user` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `event` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 109 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of share_user
-- ----------------------------

-- ----------------------------
-- Table structure for type
-- ----------------------------
DROP TABLE IF EXISTS `type`;
CREATE TABLE `type`  (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `level` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `acc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of type
-- ----------------------------
INSERT INTO `type` VALUES (4, '排练', '3', NULL);
INSERT INTO `type` VALUES (6, '排练', '1', 'None');
INSERT INTO `type` VALUES (7, '放假', '1', 'admin');
INSERT INTO `type` VALUES (8, '排练', '1', 'zsc');

-- ----------------------------
-- Table structure for userlist
-- ----------------------------
DROP TABLE IF EXISTS `userlist`;
CREATE TABLE `userlist`  (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of userlist
-- ----------------------------
INSERT INTO `userlist` VALUES (1, 'admin', 'admin1234');
INSERT INTO `userlist` VALUES (2, 'zsc', '1226');

SET FOREIGN_KEY_CHECKS = 1;
