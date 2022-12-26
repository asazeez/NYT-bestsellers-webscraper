import pandas as pd

def newTable():
    df = pd.read_csv('nyt-bestseller.csv')
    df2 = pd.DataFrame()
    df['Hardcover'] = df[['AzHardcover','IndHardcover']].min(axis=1,numeric_only=True)
    df['Hardcover Seller'] = df[['AzHardcover','IndHardcover']].idxmin(axis=1)
    df['Paperback'] = df[['AzPaperback','IndPaperback']].min(axis=1,numeric_only=True)
    df['Paperback Seller'] = df[['AzPaperback','IndPaperback']].idxmin(axis=1)
    df['Kindle'] = df[['AzEbook','IndEbook']].min(axis=1,numeric_only=True)
    df['Kindle Seller'] = df[['AzEbook','IndEbook']].idxmin(axis=1)
    df.to_csv('nyt-bestseller.csv', index=False, encoding='utf8')

    df2 ['Title'] = df[['Title']].copy()
    df2 ['Authour'] = df[['Authour']].copy()
    df2 ['Description'] = df[['Description']].copy()
    df2 ['Paperback']= df[['Paperback']].copy()
    df2 ['Paperback Seller'] = df[['Paperback Seller']].copy().replace(['AzPaperback','IndPaperback'],['Amazon','Indigo'])
    df2 ['Hardcover']= df[['Hardcover']].copy()
    df2 ['Hardcover Seller'] = df[['Hardcover Seller']].copy().replace(['AzHardcover','IndHardcover'],['Amazon','Indigo'])
    df2 ['Kindle']= df[['Kindle']].copy()
    df2 ['Kindle Seller'] = df[['Kindle Seller']].copy().replace(['AzEbook','IndEbook'],['Amazon','Indigo'])
    df2.to_csv('nyt-bestsellers prices.csv', index=False, encoding='utf8')
