##### SQL examples are tested in MySQL 8.0.29

### Example: window functions

We have a table with data about sales for a year in three cities

![table sales](https://github.com/ViktorKorolko/data-branch/blob/mysql/img/sales.jpg)

Task: query find average revenue for three months for city Madrid:
  ```
  SELECT year, nmonth, revenue, 
  ROUND(AVG(revenue) OVER w) AS avg3month 
  FROM sales.sales
  WHERE town='Madrid'
  WINDOW w AS (
     order by nmonth
     rows between 1 preceding and 1 following)
  ORDER BY nmonth;
  ```
  Result:
  
  ![Result](https://github.com/ViktorKorolko/data-branch/blob/mysql/img/avg3month.jpg)
  
  Task: make a raiting by months for all cities, where rank a revenue (1st - max revenue, 12th - min revenue)
  ```
  WITH tmp AS 
   (select year, nmonth, town, revenue,
   rank() over w as place
   from sales.sales
   window w as (
      partition by town order by revenue desc
      rows between unbounded preceding and unbounded following)
      order by nmonth, revenue
   )
SELECT year, nmonth,
SUM(case when town = 'Madrid' then place end) AS Madrid,
SUM(case when town = 'Barcelona' then place end) AS Barcelona,
SUM(case when town = 'Kordova' then place end) AS Kordova
FROM tmp
GROUP BY nmonth 
ORDER BY nmonth;
  ```
  Result:
  
  ![](https://github.com/ViktorKorolko/data-branch/blob/mysql/img/rankcities.jpg)
