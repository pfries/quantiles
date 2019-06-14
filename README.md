## Compute quantiles over frequency tables

This is useful when you have a rollup of queries and search counts, and want to
compute different quantiles for the data.

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

You can run this through a histogram grapher such as [ termgraph ](https://github.com/mkaz/termgraph).

```sh
python quantiles.py quantiles -q 3 sample_frequency_table.csv | termgraph
```

```text
1: ▇ 718.00
2: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 6227.00
3: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 18786.00
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

```
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

#### Accept input in pipe

It can be useful to preprocess your data before computing quantiles:

```sh
grep -v edu sample_frequency_table.csv | python quantiles.py quantiles
```
