--SELECT
SELECT 1 + 1;

SELECT * FROM film;
SELECT title, description FROM film WHERE description LIKE '%Epic%';

SELECT title, release_year, description FROM film WHERE release_year >= 1996 ORDER BY release_year;
SELECT title, release_year, description FROM film WHERE release_year  BETWEEN 2000 AND 2006 ORDER BY release_year asc;

-- BETWEEN
SELECT * from track where genre_id between 1 and 3 order by media_type_id;
-- LIMIT
SELECT * from track where genre_id between 1 and 3 order by media_type_id LIMIT 10;
-- RANGE
SELECT * from track where genre_id in (1,3 ,5) order by media_type_id;

-- UPDATE
update film set replacement_cost=13.99 where film_id=2;
select * from film where film_id =2;

-- DELETE
DELETE FROM film WHERE film_id = 3;





-- JOIN
select  * from film
join film_actor on film_actor.film_id = film.film_id;

-- WITH NULL VALUES
select  * from actor
FULL join film_actor  on film_actor.actor_id = actor.actor_id;


select  * from actor
FULL join film_actor on film_actor.actor_id = actor.actor_id
where film_actor.actor_id isnull;
--GROUP BY
select  * from actor
FULL join film_actor  on film_actor.actor_id = actor.actor_id;

select e.first_name, e.last_name , concat(reports_to.first_name, ' ', reports_to.last_name) as reports_to
from employee as e
full join employee as reports_to on e.employee_id=reports_to.reports_to;

-- all actors with film descriptions
select actor.actor_id, first_name, last_name , film_actor.film_id, film.title , film.release_year , film.description
from actor
join film_actor  on film_actor.actor_id = actor.actor_id
join film  on film.film_id= film_actor.film_id;

-- AGGREGATION
-- number fo films by actor
with actor_fc as (
	select actor.actor_id, COUNT(film_id) as number_movies
	from actor
	FULL join film_actor  on film_actor.actor_id = actor.actor_id
	group by  actor.actor_id
)
select actor.actor_id, first_name, last_name, number_movies
from actor_fc
join actor on actor_fc.actor_id=actor.actor_id
order by number_movies desc;


-- MIN MAX
select title, max(birth_date)  from employee group by title ;
select MIN(birth_date) from employee ;

-- SUBQUERY
select * from track  where genre_id in (
 select genre_id from genre where name in ('Rock', 'Jazz', 'Latin', 'Drama')
);
