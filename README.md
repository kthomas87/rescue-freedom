# Overview
  Goal:
  Help Rescue Freedom International make data driven decisions about how to optimize their resources to help end sexual slavery.

  How:
  Scraped data from Global slavery index, Global Modern slavery directory and adjust to only include sexual slavery. I calculated two features, Government effort and Non-Government Organization effort to try to determine what countries are not sufficiently addressing the needs of sexual slaves. Unfortunately, this didn't separate the countries enough to give Rescue Freedom a reasonable group of countries to consider for future growth. So to separate the countries further I used a third feature of vulnerability which allowed me to identify 5 countries with both insufficient Government and NGO efforts, as well as high vulnerability which gives Rescue Freedom a reasonable set of countries to consider.

  Results:
  Using the clusters I was able to determine the top nine countries for Rescue Freedom to consider for future opportunities, based a on low NGO effort, low government effort and high vulnerability.


# Explanation
  Clustering was calculated using Scikit-learn's KMeans clustering algorithm, and I determined the number of clusters using silhouette plots, landing on 9 clusters.
  One interesting insight was that the US was a huge outlier with a significantly larger Government and NGO effort and low vulnerability. Additionally, I originally hoped to cluster only using the NGO and Government efforts, but found that the majority of countries cluster between zero and one for both features requiring me to introduce vulnerability to spread my data points apart using the curse of dimensionality to my advantage.

# Code Walk-Through:
  To collect the data I scraped two sites, www.globalslaveryindex.org, and www.globalmodernslavery.org, both in the scraping data folder. Each of these files creates a CSV file.
  The bulk of my analysis is done in my rescue_freedom.py file where I merge several data frames, make my clusters and plot a 3D visualization of the data. It also outputs a csv including the clusters to then be introduced to my folium_map.py file in the geographic_data folder that takes the clusters and plots them geographically. This outputs an html file that I integrate into my web app which is contained in the my_app folder.
