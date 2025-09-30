# from bs4 import BeautifulSoup 
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


# url="https://www.iea.org/data-and-statistics/data-tools/global-ev-policy-explorer"
DATA_PATH = Path.cwd() / "data" / "policies.csv"
if __name__ == "__main__":
    # try: 
    df = pd.read_csv(DATA_PATH)
    # print(df.columns)
    # print("Country: ", df['Country/Economy'].nunique(), df['Country/Economy'].value_counts())
    # print("Level: ", df['Level'].nunique(), df['Level'].value_counts())
    # print("Policy Type: ", df['Policy type'].nunique(), df['Policy type'].value_counts())
    # print("Category: ", df['Category'].nunique(), df['Category'].value_counts())
    df["category_list"] = df['Category'].apply(lambda x: x.split(", "))
    unique_categories= set()
    # df=df.query("'Year announced' > 2015")

    # One hot encode the categories column
    for idx, row in df.iterrows():
        for item in row['category_list']:
            # print(item)
            unique_categories.add(item)
    for cat in unique_categories:
        df[cat] = False
    for idx, row in df.iterrows():
        dummies = pd.get_dummies(pd.Series(row['category_list']))
        for dummy in dummies:
            # print("d", dummy)
            df.loc[idx, dummy] = True
    # print(type(df["Country/Economy"].value_counts().head(25)))
    countrydf = df["Country/Economy"].value_counts().head(25)
    # print(countrydf[:10])
    # print(pd.crosstab(df["Country/Economy"], df["Policy type"]))
    fig, axs = plt.subplots(1,1, figsize = (10,6))

    print(df)
    '''
    # Policies by Country
    axs.bar(countrydf.index, countrydf)
    axs.set_title("Policies by Country")
    axs.set_xlabel("Country")
    axs.set_ylabel("Number of Policies")
    axs.set_xticklabels(countrydf.index, rotation=75)
    
    cats = list(unique_categories)
    category_count = [sum(df[cat]) for cat in cats]
    print(cats, category_count)
    # Categories of Policies
    # renamed_cats = ["Light-Duty", "Bus", "2/3 Wheelers",  "Multiple", "Supply Equipment",  "Manufacturing", "Taxation", "Med/Heavy-Duty"]
    
    axs.bar(cats,  category_count, label = "Unique Categories")
    # axs.bar(cats, category_count, bottom )
    axs.set_title("Number of Policies by Category")
    axs.set_xlabel("Category")
    axs.set_ylabel("Number of Policies")
    axs.set_xticklabels(cats, rotation=75)
    '''
    # print(df.groupby(["Year announced", "Policy type"]).size().unstack(fill_value=0))
    '''
    # Policy Count by Year and Type
    df["Year announced"] = pd.to_numeric(df["Year announced"]).astype("Int64")

    policy_counts = df.groupby(["Year announced", "Policy type"]).size().unstack(fill_value=0)

    # Plot stacked bar chart
    policy_counts.plot(
        kind="bar",
        stacked=True,
        figsize=(10,8),
        cmap="Accent"
    )
    plt.title("EV Policies by Year and Policy Type")
    plt.xlabel("Year Announced")
    plt.ylabel("Number of Policies")
    plt.legend(title="Policy Type")
    '''
    '''
    # Policy type by Country
    # convert df year to int
    df["Year announced"] = pd.to_numeric(df["Year announced"]).astype("Int64")
    
    # count top 6 countries w most policies 
    topcountries = df["Country/Economy"].value_counts().head(6).index
    topdf=df[df["Country/Economy"].isin(topcountries)]
    policy_counts = topdf.groupby(["Year announced", "Country/Economy"]).size().unstack(fill_value=0)

    # Plot stacked bar chart
    policy_counts.plot(
        kind="bar",
        stacked=True,
        figsize=(10,8),
        cmap="Set1"
    )
    plt.title("EV Policies by Year and Country")
    plt.xlabel("Year Announced")
    plt.ylabel("Number of Policies")
    plt.legend(title="Countries")
    plt.tight_layout()
    plt.show()
    '''

    df["Year announced"] = pd.to_numeric(df["Year announced"]).astype("Int64")

    # sum the values
    group = df.groupby(["Year announced"]).sum()#.unstack(fill_value=0)
    cats = list(unique_categories)
    print(group[cats])

    # for cat in unique_categories:

    # # Plot stacked bar chart
    bottom=None
    # print()
    for cat in cats:
        axs.bar(group.index, group[cat], label=cat, bottom = bottom)
        bottom = bottom if bottom is None else bottom +group[cat]
    plt.title("EV Policies by Year and Category")
    plt.xlabel("Year Announced")
    axs.set_xticks(group.index)                 # positions
    axs.set_xticklabels(group.index.astype(str))  # labels as strings

    plt.ylabel("Policy category")
    plt.legend(title="Policy Category")
    # Adjust the spacing
    plt.subplots_adjust(bottom=0.3)
    plt.show()