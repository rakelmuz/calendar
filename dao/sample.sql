/*criação da base de dados
create database calendar;

/*criar tabela
CREATE TABLE `evento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `allDay` char(1) NOT NULL DEFAULT 'Y',
  PRIMARY KEY (`id`)
);

