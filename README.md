# flip_or_skip

High profile sneakers are difficult to purchase upon their retail release. If you miss out, your only chance to purchase the sneaker is via the resale market, where the resale value can be over 400% of their original retail value! I built a model that predicts if a sneaker will resell at a profit before its release.

Are they worth purchasing to resell? (Flip)
Or should we just avoid buying them? (Skip)

# Data Collection and Process:
I scraped data from StockX.com. I was able to scrape 765 Jordan sneakers and 922 Nike sneakers. Broke down the sneakers into 9 features, most of which were categorical. Fed the sneaker data into a Random Forest Classifier (RFC)  for Nike and Jordan respectively. Models give out a percentage of which class the shoe will belong to, flip or not flip (skip). I also utilized a Random Forest Regressor(RFR). Using the same features, these models also predict the actual resale value of a sneaker.

# Results:
My RFC for Nike and Jordan have AUC of 0.7529 and 0.7599 respectively. For Nike, my model scored an accuracy of 0.6667 with a precision of 0.7222. For Jordan, my model scored an accuracy of 0.7083 with a precision of 0.6857

However, my RFR had much more varying results. Due to the outliers in my data, my models were trained  with extreme ranges. These outliers included a sneaker reselling for +600 percent of retail (+\$11,000). Mean squared error for both Nike and Jordan models were too high.


