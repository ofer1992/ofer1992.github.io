Title: Supermarket Prices
Date: 2025-10-10 12:24
Category: Programming
Status: draft

Lately with AI agents are all the craze, and indeed their behavior is quite impressive. The nice thing is that you can give them access to stuff through REST APIs or terminal tools or files and they manage to use them and combine them with other things. Anyway, I was thinking, what if we give an agent access to supermarket prices, what could it do? could it build a shopping list? could it find a recipe and tell you which ingredients to buy?

Now, in Israel by law all large enough grocery stores must supply price info for all their locations online, updated every couple of hours. While the intention is great, the execution is not so. Every chain has its own publishing system or method, they mostly rely on xmls and there's no easy programmatic way to access stuff. I know its possible though, because the app CHP does just that, aggregates all the info to one nice interface. Even though its free, it doesn't offer an api and even after reverse engineering an api on top of it, it is not expressive enough to be useful for an agent. Also, having some free publicly accessible API seems like a useful thing, and maybe a fun project.

After some snooping around I also found https://www.kaggle.com/datasets/erlichsefi/israeli-supermarkets-2024, which is "A versioned daily dump of the data published by the Israeli supermarkets chain". They already do all the scraping and convert the xmls to csvs. At least for now we can use it to save some time.

So, what does the data look like? for each chain we have a

- `[name].json`: logs the scraping process for the kaggle dataset creation
- `price_full_file_[name].csv`: full price snapshot for all products in all locations
- `price_file_[name].csv`: price changes since last update
- `promo_full_file_[name].csv`: full promo snapshot in all locations
- `promo_file_[name].csv`: promo changes since last update
- `store_file_[name].csv`: list of locations for chain

Let's look at `price_full_file_super_yuda.csv`. A typical sample looks like (showing some of the columns)

|       | priceupdatedate     |    itemcode | itemname             | manufactureritemdescription | unitqty   | quantity | unitofmeasure | bisweighted | qtyinpackage | itemprice | unitofmeasureprice | itemid |
| ----: | :------------------ | ----------: | :------------------- | :-------------------------- | :-------- | -------: | :------------ | ----------: | -----------: | --------: | -----------------: | -----: |
| 49996 | 2025-07-29 20:00:18 |    7.29e+12 | לחם מחמצת לבן        | לחם מחמצת לבן               | יחידה     |        0 | יחידה         |         nan |          nan |      21.9 |                  0 | 216346 |
| 74083 | 2025-09-07 08:18:45 |    7.29e+12 | תמר צהוב             | תמר צהוב                    | קילוגרמים |        1 | ק"ג           |           1 |          nan |      29.9 |               29.9 | 212648 |
| 13725 | nan                 | 7.29011e+12 | צבר חומוס צנובר 400  | צבר חומוס צנובר 400         | nan       |      nan | nan           |         nan |          nan |       nan |                nan | 176704 |
| 71788 | 2025-03-06 13:05:14 | 8.02499e+12 | סמוזי שיבולת שועל תפ | סמוזי שיבולת שועל תפ        | גרמים     |      100 | 100 גרם       |         nan |          nan |       7.5 |                7.5 | 215969 |
| 47217 | 2025-05-05 06:54:47 | 7.29001e+12 | מרסס מסיר כתמים "אוק | מרסס מסיר כתמים "אוק        | nan       |      nan | nan           |         nan |          nan |      22.9 |                nan | 186712 |
Some observations:
- itemid or itemcode are the product identifier
- we have some columns for quantities but they are a bit confusing, and we can expect some inconsitencies in the units specification for example
- some rows even have a missing price, so what's the point of having them?

We also have some missing info, for example which store is the price in? I removed these columns because they are null. Why are they null? well, I guess to save space, the dataset has a ffill convention for some of the columns. Let's look at the column breakdown.

| Column                      | Data Type | % Complete |
| --------------------------- | --------- | ---------- |
| itemid                      | int64     | 100.0%     |
| itemcode                    | float64   | 99.99%     |
| itemname                    | object    | 97.7%      |
| manufactureritemdescription | object    | 97.7%      |
| itemprice                   | float64   | 79.2%      |
| unitofmeasureprice          | float64   | 72.6%      |
| quantity                    | float64   | 64.6%      |
| priceupdatedate             | object    | 62.7%      |
| unitofmeasure               | object    | 35.4%      |
| unitqty                     | object    | 34.6%      |
| bisweighted                 | float64   | 2.3%       |
| allowdiscount               | float64   | 2.2%       |
| manufacturername            | object    | 0.55%      |
| found_folder                | object    | 0.04%      |
| file_name                   | object    | 0.04%      |
| chainid                     | float64   | 0.04%      |
| subchainid                  | float64   | 0.04%      |
| storeid                     | float64   | 0.04%      |
| bikoretno                   | float64   | 0.04%      |
| itemtype                    | float64   | 0.04%      |
| manufacturecountry          | object    | 0.04%      |
| qtyinpackage                | object    | 0.04%      |
| itemstatus                  | float64   | 0.04%      |
- **Total Entries:** 134,940  
- **Total Columns:** 23  

If we model the data relationally we arrive at something like 
![[Screenshot 2025-10-10 at 13.30.28.png]]