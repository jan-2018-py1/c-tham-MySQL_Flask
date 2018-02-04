use 0wall;

select * from users
;
select * from messages
;
select * from comments
;

select m.id, concat(u.first_name,'  ',u.last_name) as name, m.message, m.created_at 
from messages m
join users u on m.user_id = u.id
order by m.created_at desc
;

select *
from messages m
join users u on m.user_id = u.id
;

select c.id, c.user_id, c.message_id, concat(u.first_name,'  ',u.last_name) as name, c.comment, c.created_at
from comments c
left join messages m on c.message_id = m.id
left join users u on c.user_id = u.id
;

select *
from comments c
left join messages m on c.message_id = m.id
left join users u on c.user_id = u.id
;

select created_at - updated_at, created_at, date_format(created_at,'%Y-%m-%d %h:%m:%s') -  '2018-02-03 01:07:51' from messages
;