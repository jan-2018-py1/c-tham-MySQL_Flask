use 0emailsdb
;

select * from emails
;

INSERT INTO `0emailsdb`.`emails` (`email`, `created_at`, `updated_at`) VALUES ('michael@condingdojo.com', now(), now());
INSERT INTO `0emailsdb`.`emails` (`email`, `created_at`, `updated_at`) VALUES ('dexter@codingdojo.com', now(), now());
INSERT INTO `0emailsdb`.`emails` (`email`, `created_at`, `updated_at`) VALUES ('eylem@codingdojo.com', now(), now());


select * from emails
;