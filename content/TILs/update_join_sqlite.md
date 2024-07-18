Title: Update with join in sqlite
Date: 2024-03-31 16:10
Category: Dailies
Status: published

I converted a csv containing customer information to a sqlite table, and it needed breaking down to several tables. Specifically, some columns where really about the employer, so it was better to normalize the employers in the table out and bring these columns along.

To normalize the `Employer` column I used `sqlite-utils`, a cool library that makes working with sqlite nicer. [Extracting](https://sqlite-utils.datasette.io/en/stable/cli.html#extracting-columns-into-a-separate-table) can be done with
```bash
sqlite-utils extract my.db customers Employer
```
which create a new table with unique values etc.

How can we bring `Employer_State` along? I used a relatively new (2020) sqlite feature called *UPDATE FROM* which allows you to update table values based on a different table.

```sqlite
UPDATE employers
SET STATE = customers.EMPLOYER_STATE
FROM customers
WHERE employers.id = customers.employers_id
  AND conditions...
```

Fairly straightforward. We update the `employers` table's column STATE with the column from customers. The WHERE clause is responsible for the join. You can also add other conditions to prevent updating some rows, or handle multiple values etc.