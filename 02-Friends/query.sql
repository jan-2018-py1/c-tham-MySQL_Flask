use 0friendsdb
;

select * from friends
;

INSERT INTO `0friendsdb`.`friends` (`first_name`, `last_name`, `age`, `friend_since`, `created_at`, `updated_at`) VALUES ('Jay', 'Patel', '19', '2015-01-15', now(), now());
INSERT INTO `0friendsdb`.`friends` (`first_name`, `last_name`, `age`, `friend_since`, `created_at`, `updated_at`) VALUES ('Brendan', 'Stanton', '17', '2015-06-19', now(), now());
INSERT INTO `0friendsdb`.`friends` (`first_name`, `last_name`, `age`, `friend_since`, `created_at`, `updated_at`) VALUES ('Eli', 'Byers', '20', '2016-08-12', now(), now());
INSERT INTO `0friendsdb`.`friends` (`first_name`, `last_name`, `age`, `friend_since`, `created_at`, `updated_at`) VALUES ('Anna', 'Propas', '30', '1987-05-03', now(), now());

select * from friends
;