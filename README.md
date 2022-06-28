# ClickHouse
 We have a table named ads_data with infirmation about 
 
 Table structure:
 |Column names|Description|
 |------------|:----------|
 |date|event date|
 |time|event time|
 |event|type of event (cleck or view)|
 |platform|platform on which the advertising event took place|
 |ad_id|advertisement id|
 |client_union_id|advertiser id|
 |campaign_union_id|advertising campaign|
 |ad_cost_type|type of ad with pay-per-clicks (CPC) or per-impressions (CPM)|
 |ad_cost|the cost of an ad in rubles, for CPC ads - per click,<br/>for CPM - the price per 1000 impressions|
 |has_video|video availability (0 or 1)|
 |target_audience_count|the size of the audience (quantity of people)|
 
 
 ### Example 1
  Calculate count all events, views, clicks, uniq advertisments and campaign by days.
 
 ```
 select date, countIf(event='view') as count_views,
       countIf(event='click') as count_clicks,
       uniqExact(ad_id) as count_ad,
       uniqExact(campaign_union_id) as count_campaign
from ads_data
group by date;
```

### Example 2
How many percent of clicks for each platform?
```
select platform,
       round(count_view/(
                   select countIf(event='view') from ads_data)
                   *100,0)
       as percent_views
from
(select platform, countIf(event='view') as count_view
from ads_data
group by platform);
```

### Example 3
How much have we earned for each day? (we take a money for CPC and CPM)
```
select date, round(sum(day_cost),0) as day_earn from
       (select date,
               case
                   when ad_cost_type = 'CPM' then count_cv * ad_cost / 1000
                   else count_cv * ad_cost
                   end day_cost
        from (select date, ad_id, event, ad_cost_type, count(ad_cost_type) as count_cv, ad_cost
              from ads_data
              group by date, ad_id, event, ad_cost_type, ad_cost
              having (event='click' and ad_cost_type='CPC') or (event='view' and ad_cost_type='CPM'))
       )
group by date order by date;
```
