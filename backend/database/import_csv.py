import pandas as pd

from database.database import SessionLocal

from models.compliance import (
    Act,
    ComplianceParticular
)
#open database session
db = SessionLocal()
#read csv
df = pd.read_csv("data/compliance_list.csv")

print("CSV Loaded Successfully!")
print(f"Total records: {len(df)}")

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())
print(df["cmplst_act"].dropna().unique())


act_lookup = {}

# Get all unique acts from the CSV
unique_acts = (
    df["cmplst_act"]
    .dropna()
    .str.strip()
    .str.upper()
    .unique()
)

print("\n========== Creating Acts ==========\n")

for act_value in unique_acts:

    act_name = str(act_value).strip().upper()

    print(f"Checking -> {act_name}")

    act = db.query(Act).filter(
        Act.act_name == act_name
    ).first()

    if not act:

        print("Creating:", act_name)

        act = Act(
            act_name=act_name,
            country=(
                df.loc[
                    df["cmplst_act"].str.strip().str.upper() == act_name,
                    "cmplst_country"
                ]
                .iloc[0]
            )
            
        )

        db.add(act)
        db.commit()
        db.refresh(act)

    else:

        print("Already Exists:", act_name)

    act_lookup[act_name] = act.id

print("\nFinal Lookup")
print(act_lookup)

#to check how many records were imported and skipped
imported_count = 0
skipped_count = 0

#looping through the csv
for _, row in df.iterrows():

    act_name = str(row["cmplst_act"]).strip().upper()
    print("Row Act:", act_name)

    # Skip unsupported acts
    if act_name not in act_lookup:        #reads the act name, if not one of our supported acts, ignores it.
        continue   
        
    act_id = act_lookup[act_name]    #every row knows which act_id it belongs to.
        
    existing = db.query(ComplianceParticular).filter(
        ComplianceParticular.csv_id == row["cmplst_id"]
    ).first()

    if existing:          #running the importer twice, so that it won't create duplicate records.
        skipped_count += 1
        continue

    #creating the compliance Particular
    compliance = ComplianceParticular(
        csv_id=row["cmplst_id"],
        act_id=act_id,
        particular=row["cmplst_particular"],
        description=row["cmplst_description"],
        compliance_key=row["cmplst_compliance_key"]
    )
    print("Importing:", row["cmplst_particular"])

    db.add(compliance)
    imported_count += 1

db.commit() #comitting once at the end is faster, than comitting after every row.

print("\nImport Complete!")
print(f"Imported: {imported_count}")
print(f"Skipped: {skipped_count}")

db.close()
