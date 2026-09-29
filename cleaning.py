import os
import pandas as pd

os.makedirs("data", exist_ok=True) # create a seperate folder to store cleaned files
df = pd.read_csv("survey_data_updated.csv")
# Filter needed columns
COLS = [
    "ResponseId",
    "MainBranch",
    "Age",
    "Employment",
    "RemoteWork",
    "CodingActivities",
    "EdLevel",
    "YearsCodePro",
    "DevType",
    "OrgSize",
    "Country",
    "Currency",
    "CompTotal",
    "LanguageHaveWorkedWith",
    "LanguageWantToWorkWith",
    "DatabaseHaveWorkedWith",
    "DatabaseWantToWorkWith",
    "PlatformHaveWorkedWith",
    "PlatformWantToWorkWith",
    "WebframeHaveWorkedWith",
    "WebframeWantToWorkWith",
    "Frustration",
    "Industry",
    "ConvertedCompYearly",
    "JobSat",
]

df = df[COLS]

def YearsCodeTransform(val):
    '''
    Classifies YearsCodePro into 5 professional experience tiers.
    '''
    if pd.isna(val) or val is None:
        return 'Unknown'
    
    if str(val).strip() == 'Less than 1 year':
        val = 0
    elif str(val).strip() == 'More than 50 years':
        val = 50
    
    try:
        years = float(val)
    except ValueError:
        return 'Unknown'
    
    if years < 2:
        return '< 2 years'
    elif years <= 5:
        return '3-5 years'
    elif years <= 10:
        return '6-10 years'
    elif years <= 20:
        return '11-20 years'
    else:
        return '20+ years'

def OrgSizeTransform(val):
    '''
    Classifies OrgSize into company-size tiers.
    '''
    if pd.isna(val) or val is None or val == 'I don’t know':
        return 'Unknown'
    
    val_str = str(val).strip()
    
    if 'Just me' in val_str:
        return 'Solo / Freelance'
    elif val_str in ['2 to 9 employees', '10 to 19 employees', '20 to 99 employees']:
        return 'Small (< 100)'
    elif val_str in ['100 to 499 employees', '500 to 999 employees']:
        return 'Mid-size (100-999)'
    elif val_str in ['1,000 to 4,999 employees', '5,000 to 9,999 employees', '10,000 or more employees']:
        return 'Enterprise (1,000+)'
    else:
        return 'Unknown'

def CurrentTechTransform(df):
    """
    YearsCodePro (str) for 2nd dimension of stacked bar chart of Language Used and Web Frameworks bubble
    OrgSize      (str) for 2nd dimension of stacked columns chart of Database Used
    """
    df['YearsCodePro_Transform'] = df['YearsCodePro'].apply(YearsCodeTransform)
    df['OrgSize_Transform'] = df['OrgSize'].apply(OrgSizeTransform)

    language = df[["ResponseId", "LanguageHaveWorkedWith", "YearsCodePro_Transform"]].copy()
    language["LanguageHaveWorkedWith"] = language["LanguageHaveWorkedWith"].str.split(";")
    language = language.explode("LanguageHaveWorkedWith")

    db = df[["ResponseId", "DatabaseHaveWorkedWith", "OrgSize_Transform"]].copy()
    db["DatabaseHaveWorkedWith"] = db["DatabaseHaveWorkedWith"].str.split(";")
    db = db.explode("DatabaseHaveWorkedWith")

    platform = df["PlatformHaveWorkedWith"].str.split(";").explode()
    platform = (platform
                .value_counts()
                .sort_values(ascending=False).head(10)
                .reset_index()
    )


    df["YearsCodePro"] = df["YearsCodePro"].replace({'Less than 1 year': 0, 'More than 50 years': 50}).astype(float)
    framework = df[["ResponseId","WebframeHaveWorkedWith", "YearsCodePro"]].copy()
    framework["WebframeHaveWorkedWith"] = framework["WebframeHaveWorkedWith"].str.split(";")
    framework = framework.explode("WebframeHaveWorkedWith")

    for i in (language, db, framework):
        path = f"{i.columns[1]}.csv"
        print("Saved as: "+path)
        i.to_csv("data/"+path, index=False)
    print("Saved as: PlatformHaveWorkedWith.csv")
    platform.to_csv("data/PlatformHaveWorkedWith.csv", index=False)

def FutureTechTransform(df):
    """
    YearsCodePro (str) for 2nd dimension of stacked bar chart of Language Desired
    OrgSize      (str) for 2nd dimension of stacked columns chart of Database Desired
    """
    df['YearsCodePro_Transform'] = df['YearsCodePro'].apply(YearsCodeTransform)
    df['OrgSize_Transform'] = df['OrgSize'].apply(OrgSizeTransform)

    language = df[["ResponseId", "LanguageWantToWorkWith", "YearsCodePro_Transform"]].copy()
    language["LanguageWantToWorkWith"] = language["LanguageWantToWorkWith"].str.split(";")
    language = language.explode("LanguageWantToWorkWith")

    db = df[["ResponseId", "DatabaseWantToWorkWith", "OrgSize_Transform"]].copy()
    db["DatabaseWantToWorkWith"] = db["DatabaseWantToWorkWith"].str.split(";")
    db = db.explode("DatabaseWantToWorkWith")

    platform = df["PlatformWantToWorkWith"].str.split(";").explode()
    platform = (platform
                .value_counts()
                .sort_values(ascending=False).head(10)
                .reset_index()
    )

    df["YearsCodePro"] = df["YearsCodePro"].replace({'Less than 1 year': 0, 'More than 50 years': 50}).astype(float)
    framework = df[["ResponseId","WebframeWantToWorkWith", "YearsCodePro"]].copy()
    framework["WebframeWantToWorkWith"] = framework["WebframeWantToWorkWith"].str.split(";")
    framework = framework.explode("WebframeWantToWorkWith")

    for i in (language, db, framework):
        path = f"{i.columns[1]}.csv"
        print("Saved as: "+path)
        i.to_csv("data/"+path, index=False)
    print("Saved as: PlatformWantToWorkWith.csv")
    platform.to_csv("data/PlatformWantToWorkWith.csv", index=False)

def Demographics(df):
    cols = ["ResponseId", "Age", "Country", "EdLevel"]
    df = df[cols]
    
    df['EdLevel_short'] = df['EdLevel'].str.replace(r'\s*\(.*?\)', '', regex=True)
    df['EdLevel_short'] = df['EdLevel_short'].replace({
        'Some college/university study without earning a degree': 'College study, no degree'
    })

    country_map = {
    'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
    'United States of America': 'United States',
    'Republic of North Macedonia': 'North Macedonia',
    'United Republic of Tanzania': 'Tanzania',
    'Russian Federation': 'Russia',
    'Viet Nam': 'Vietnam',
    'Venezuela, Bolivarian Republic of...': 'Venezuela',
    'Iran, Islamic Republic of...': 'Iran',
    'Hong Kong (S.A.R.)': 'Hong Kong',
    'Republic of Korea': 'South Korea',
    'Republic of Moldova': 'Moldova',
    'Syrian Arab Republic': 'Syria',
    'Congo, Republic of the...': 'Republic of the Congo',
    'Brunei Darussalam': 'Brunei',
    'Côte d\'Ivoire': 'Cote d\'Ivoire',
    'Nomadic': None  # Set non-geographic responses to null/NaN
    }

    df['Country'] = df['Country'].replace(country_map)

    path = "Demographics.csv"
    print("Saved as: "+path)
    df.to_csv("data/"+path, index=False)

if __name__ == '__main__':
    CurrentTechTransform(df)
    FutureTechTransform(df)
    Demographics(df)