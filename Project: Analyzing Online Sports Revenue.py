# Start coding here... 
import pandas as pd

# Read in the data
info = pd.read_csv("info.csv")
finance = pd.read_csv("finance.csv")
reviews = pd.read_csv("reviews.csv")
brands = pd.read_csv("brands.csv")

# Merge the data and drop null values
merged_df = info.merge(finance, on="product_id")
merged_df = merged_df.merge(reviews, on="product_id")
merged_df = merged_df.merge(brands, on="product_id")
merged_df.dropna(inplace=True)

# Add price labels based on listing_price quartiles
merged_df["price_label"] = pd.qcut(merged_df["listing_price"], q=4, labels=["Budget", "Average", "Expensive", "Elite"])

# Group by brand and price_label to get volume and mean revenue
adidas_vs_nike = merged_df.groupby(["brand", "price_label"], as_index=False).agg(
    num_products=("price_label", "count"), 
    mean_revenue=("revenue", "mean")
).round(2)

print(adidas_vs_nike)

# Store the length of each description
merged_df["description_length"] = merged_df["description"].str.len()

# Upper description length limits
lengthes = [0, 100, 200, 300, 400, 500, 600, 700]

# Description length labels
labels = ["100", "200", "300", "400", "500", "600", "700"]

# Cut into bins
merged_df["description_length"] = pd.cut(merged_df["description_length"], bins=lengthes, labels=labels)

# Group by the bins
description_lengths = merged_df.groupby("description_length", as_index=False).agg(
    mean_rating=("rating", "mean"), 
    num_reviews=("reviews", "count")
).round(2)

print(description_lengths)

# List of footwear keywords
mylist = "shoe*|trainer*|foot*"

# Filter for footwear products
shoes = merged_df[merged_df["description"].str.contains(mylist)]

# Filter for clothing products
clothing = merged_df[~merged_df.isin(shoes["product_id"])]

# Remove null product_id values from clothing DataFrame
clothing.dropna(inplace=True)

# Create product_types DataFrame
product_types = pd.DataFrame({"num_clothing_products": len(clothing), 
                              "median_clothing_revenue": clothing["revenue"].median(), 
                              "num_footwear_products": len(shoes), 
                              "median_footwear_revenue": shoes["revenue"].median()}, 
                              index=[0])

print(product_types)
