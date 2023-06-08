import pandas as pd

csv_file = "verified.csv"

df = pd.read_csv(csv_file)

field_order = [
    'id', 'first_name', 'last_name', 'name', 'linkedin_url', 'title', 'email_status',
    'photo_url', 'twitter_url', 'github_url', 'facebook_url', 'extrapolated_email_confidence',
    'headline', 'email', 'organization_id', 'employment_history', 'state', 'city', 'country',
    'organization', 'intent_strength', 'show_intent', 'revealed_for_current_team',
    'departments', 'subdepartments', 'functions', 'seniority'
]

existing_columns = df.columns.tolist()

new_field_order = [col for col in field_order if col in existing_columns]
new_field_order += [col for col in existing_columns if col not in field_order]
df = df[new_field_order]
df.to_csv(csv_file, index=False)
print("CSV file updated with the desired field order.")
