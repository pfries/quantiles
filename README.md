## Compute quantiles over frequency tables

This is useful when you have a rollup of values and counts, and want to
compute different quantiles for the data. The results are rolling buckets where
each bucket represents q percent of the total. 

One use case for `quantiles` is when optimizing search relevance.  A good place
to start is by looking at the most popular queries. Unless you have a long,
flat distribution of queries, there are likely to be relatively few of them.
So, in the case of head/tail analysis, the top 100 queries may represent
half the total volume of all queries, while the other half is the long tail.
By tuning the performance of only 100 queries, you can improve the
performance of half of all searches performed. You can then move on to the
more diverse issues encountered in the long tail.

There is a sample frequency table `sample_frequency_table.csv` with the correct
format for computing quantiles. 

The sample is from the AOL query logs released in 2006 and have been cleaned up
but apologies if there are offensive queries still in the logs.

## Installation

Requires Python 3. Recommend you use a virtual environment.

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

`quantiles.py` expects a `csv` formated file with columns named `query` and
`instances`. A sample frequency table is included that looks like this:

```csv
query,instances,revenue
google,32163,990.87
yahoo,13646,985.81
ebay,13075,930.14
mapquest,8719,925.08
myspace,6877,894.72
my space,3008,889.66
map quest,2899,869.42
http,2840,864.36
weather,2676,859.30
```

Here are a list of some things you can do with this program.

#### Compute the deciles for a frequency table:

```sh
python quantiles.py quantiles -q 10 sample_frequency_table.csv
```

Which outputs:

```text
1	9
2	119
3	378
4	801
5	1403
6	2212
7	3220
8	4434
9	5833
10	7322
```

You can run this through a grapher such as [termgraph](https://github.com/mkaz/termgraph).

```sh
python quantiles.py quantiles -q 3 sample_frequency_table.csv | termgraph --format '{:.0f}
```

```text
1: ▇ 718
2: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 6227
3: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 18786
```

#### List all the queries in the head (top quantile):

```sh
python quantiles.py head sample_frequency_table.csv
```

By default this will split the frequency table in two, but you can specify the
number of quanties with the `--quantiles` (`-q`) flag. For example, to split the
table into `HEAD`, `MIDDLE`, `TAIL` and list the `HEAD` queries, use:

```sh
python quantiles.py head -q 3 sample_frequency_table.csv
```

#### List out the tail queries. To see a sample of the long tail (10th decile):

```sh
python quantiles.py tail -q 10 sample_frequency_table.csv | shuf -n 25
```

```text
stuff mag
philip way
reformista
nursing homes in texas
directmerchantsbank
home floor plans
sony digital camera
n64 expansion pak
mailcontrols
neo pets
canadian geese
aol.travel
guyana newspaper stabroke
fernbank museum of history
virginia dmv
personal ads
whiskey jug
rat pack las vegas
country inn & suites
not producing enough progesterone
progesterone cream
mock nfl draft
myspace videos
printing gift certificates
uncle sam outdoor garden statue
```

This can be useful is you want to generate a representative set of test
queries.

#### Compute revenue quantiles

The instances can be decimal values, so you can also compute the quantiles
based on revenue per query. The sample data includes some randomly generated
revenue data. To try this, rename the sample data column header to use the
`revenue` column as the `instances` column (using `awk`).

```sh
awk -F, 'BEGIN { print "query,instances" } { if (NR > 1) print $1","$3 }' sample_frequency_table.csv | python quantiles.py quantiles -q 10 | termgraph --format '{:.0f}'
```

```text

1 : ▏ 55
2 : ▏ 93
3 : ▇ 252
4 : ▇ 370
5 : ▇ 465
6 : ▇▇ 707
7 : ▇▇▇▇▇▇▇▇▇▇▇ 2836
8 : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 3896
9 : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 5065
10: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 11981
```

This shows that 55 queries generate 10% of all revenue. Pretty useful if you
want to concentrate your efforts for the reward.

#### Accept input on pipe

It can be useful to preprocess your data before computing quantiles:

```sh
grep -v edu sample_frequency_table.csv | python quantiles.py quantiles
```

