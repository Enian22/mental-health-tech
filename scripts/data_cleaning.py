import pandas as pd

def load_and_clean(filepath):
    """
    Loads and cleans the OSMI Mental Health dataset.

    Parameters:
    filepath (str): Path to CSV file

    Returns:
    pd.DataFrame: Cleaned DataFrame
    """
    df = pd.read_csv(filepath)
    
    # Fill missing values
    df.fillna('Unknown', inplace=True)

    # Remove outlier ages
    df = df[df['Age'].between(18, 65)]

    # Normalize gender
    df['Gender'] = df['Gender'].str.strip().str.lower()
    
    # Group messy entries into 'male', 'female', or 'other'
    gender_replacements = {
        # Male variations
        'male-ish': 'male',
        'cis male': 'male',
        'm': 'male',
        'man': 'male',
        'make': 'male',
        'mal': 'male',
        'maile': 'male',
        'guy (-ish) ^_^': 'male',
        'male (cis)': 'male',
        'male leaning androgynous': 'male',
        'msle': 'male',
        'mail': 'male',
        'malr': 'male',
        'cis man': 'male',
        'something kinda male?': 'male',
        'ostensibly male, unsure what that really means': 'male',  # Longest string

        # Female variations
        'cis female': 'female',
        'f': 'female',
        'woman': 'female',
        'femake': 'female',
        'femail': 'female',
        'female (trans)': 'female',
        # Keep trans female as 'female' based on common interpretation unless 'other' is strongly preferred
        'trans woman': 'female',  # Keep trans woman as 'female'
        'cis-female/femme': 'female',
        'female (cis)': 'female',

        # Other/Non-binary/Ambiguous/Unspecified
        'trans female': 'other',  # If you want to group all trans identities into 'other'
        'trans male': 'other',
        'non-binary': 'other',
        'queer/she/they': 'other',
        'enby': 'other',
        'fluid': 'other',
        'androgyne': 'other',
        'agender': 'other',
        'neuter': 'other',
        'queer': 'other',
        'genderqueer': 'other',
        'trans-female': 'other',
        'nah': 'other',  # This looks like an invalid/unspecified response
        # 'other' should already be lowercase if it exists

    }
    # Any values not in the dictionary keys will remain unchanged, so 'male', 'female', 'other' (if already present) will stay as they are.
    df['Gender'] = df['Gender'].replace(gender_replacements)

    # Define desired explicit gender mapping
    gender_mapping = {
        'male': 0,
        'female': 1,
        'other': 2
    }

    # Apply the mapping using .map()
    df['Gender_Encoded'] = df['Gender'].map(gender_mapping)

    # Define desired explicit work_interfere mapping
    work_interfere_mapping = {
        'Never': 0,
        'Rarely': 1,
        'Sometimes': 2,
        'Often': 3,
        'Unknown': 4
    }

    # Apply the mapping using .map()
    df['Work_Interfere_Encoded'] = df['work_interfere'].map(work_interfere_mapping)

    # Define desired explicit care_options mapping
    care_options_mapping = {
        'No': 0,
        'Yes': 1,
        'Not sure': 2
    }

    # Apply the mapping using .map()
    df['Care_Options_Encoded'] = df['care_options'].map(care_options_mapping)
    
    # Binary encode important fields
    binary_map = {'Yes': 1, 'No': 0}
    for col in ['family_history', 'treatment', 'remote_work']:
        df[col] = df[col].map(binary_map)

    
    return df
