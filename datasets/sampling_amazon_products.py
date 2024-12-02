"""
old source: https://cseweb.ucsd.edu/~jmcauley/datasets/amazon/links.html
new source: https://amazon-reviews-2023.github.io

download the Digital_Music sub-dataset

columns of joined new source: 
    rating               130434
    title_x              130434
    text                 130434
    images_x             130434
    asin                 130434
    parent_asin          130434
    user_id              130434
    timestamp            130434
    helpful_vote         130434
    verified_purchase    130434
    main_category        130434
    title_y              130434
    average_rating       130434
    rating_number        130434
    features             130434
    description          130434
    price                 81492
    images_y             130434
    videos               130434
    store                124010
    categories           130434
    details              130434
    bought_together           0
"""
import pandas as pd
def extract_format(store_str):
    if store_str is None or "Format" not in store_str:
        return ""
    return store_str.split("Format: ")[-1].strip()

review_df = pd.read_json("Digital_Music.jsonl.gz", lines=True, compression='gzip')
meta_df = pd.read_json("meta_Digital_Music.jsonl.gz", lines=True, compression='gzip')
meta_df["Format"] = meta_df["store"].map(extract_format)
#print(meta_df["Format"].unique())
df = review_df.merge(meta_df, on="parent_asin", how="inner")
#print(df.head(3))
#print(df.count())

old_columns = ["asin", "text", "verified_purchase", "rating", "title_x", "Format", "description"]
new_columns = ["asin", "reviewText", "verified", "overall", "summary", "Format", "description"]
old2new_map = {old_columns[i]:new_columns[i] for i in range(len(old_columns))}

sampled_df = df.sample(n=15014, random_state=0)[old_columns].rename(columns=old2new_map)
#print(sampled_df[["summary", "Format", "description"]].head())
output_file_path = "Amazon_Product_Reviews.jsonl.gz"
sampled_df.to_json(output_file_path, orient='records', lines=True, compression='gzip')
