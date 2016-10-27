DROP DATABASE IF EXISTS maicheren;
CREATE DATABASE IF NOT EXISTS maicheren
  DEFAULT CHARACTER SET UTF8
  COLLATE UTF8_general_ci;
USE maicheren;

#品牌表：静态表
CREATE TABLE `brands` (
  `id`   INT UNSIGNED NOT NULL,
  `name` VARCHAR(64)  NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = innodb
  DEFAULT CHARSET = utf8
  AUTO_INCREMENT = 1;

#管理员添加商品的时候，必须先添加一条sku，或者根据已有sku来添加商品
CREATE TABLE `sku` (
  `id`           INT UNSIGNED                                                          NOT NULL,
  `brand_id`     INT                                                                   NOT NULL, #选定品牌id
  `color`        ENUM ('black', 'red', 'silver', 'brown', 'blue')                      NOT NULL,
  `type`         ENUM ('two', 'three', 'suv'), #轿车类型
  `seats`        ENUM ('2', '5', '7'), #座位数
  `displacement` ENUM ('1.5L', '1.8L', '2.0L', '2.5L', '1.5T', '1.8T', '2.0T', '2.2T') NOT NULL, #排量
  `price`        INT                                                                   NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = innodb
  DEFAULT CHARSET = utf8
  AUTO_INCREMENT = 1;

#管理员添加库存的时候，必须先选定库存商品所属sku
CREATE TABLE `stock` (
  `id`     INT UNSIGNED       NOT NULL,
  `sku_id` INT                NOT NULL,
  `vin`    VARCHAR(64) UNIQUE NOT NULL, #车架号
  `status` ENUM ('selling', 'sold', 'unavailable'), #selling：在库，sold：已售，unavailable：缺货
  PRIMARY KEY (`id`)
)
  ENGINE = innodb
  DEFAULT CHARSET = utf8
  AUTO_INCREMENT = 1;