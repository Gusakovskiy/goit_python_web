-- https://www.postgresql.org/docs/9.1/tutorial-window.html
-- https://www.postgresqltutorial.com/postgresql-window-function/
select
SUM(total) as total_per_country,
billing_country
from invoice i
group by billing_country
order by total_per_country desc;

/* But unlike regular aggregate functions, use of a window function does not cause rows
to become grouped into a single output row — the rows retain their separate identities.
Behind the scenes, the window function is able to access more than just the current row of the query result.
*/

SELECT total, billing_country,
SUM(total) OVER (PARTITION BY billing_country) as total_per_country
from invoice
order BY total_per_country;

-- with window naming
SELECT total, billing_country,
SUM(total) OVER w1 as total_per_country
from invoice
WINDOW w1 as (PARTITION BY billing_country)
order BY total_per_country;


-- with rank query
SELECT
billing_country,
total,
rank() OVER(PARTITION BY billing_country order by total)
from invoice;

-- create ids for all
SELECT
billing_country,
total,
ROW_NUMBER() OVER(PARTITION BY billing_country order by total) as _id_on_fly
from invoice;

with transaction_in_country as (SELECT
billing_country,
total,
SUM(total) OVER (PARTITION BY billing_country) as total_per_country,
SUM(total) OVER() as totaL_sum
from invoice
order BY total_per_country
)
select * from transaction_in_country;


with transaction_in_country as (SELECT
billing_country,
total,
SUM(total) OVER (PARTITION BY billing_country) as total_per_country,
SUM(total) OVER() as totaL_sum
from invoice
order BY total_per_country
)
select
(total/total_per_country * 100) as percent_in_country,
(total_per_country/totaL_sum * 100) as country_percent,
billing_country
from transaction_in_country

;
-- Last invoice of customer
select
invoice_id,
billing_country,
customer_id,
total,
invoice_date,
first_value(invoice_id) over (
	PARTITION by customer_id
	order by invoice_date desc
) as last_invoice_id
from invoice
where customer_id=2;



SELECT * from invoice;


