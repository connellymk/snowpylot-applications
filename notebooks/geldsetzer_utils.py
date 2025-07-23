import pandas as pd
import numpy as np

# Load Geldsetzer table of density values
geldsetzer_df = pd.read_csv('geldsetzer_table.csv', index_col=0)

def get_density(hand_hardness, grain_form, df=geldsetzer_df):
    """
    Get density value for a specific hand hardness and grain form combination.
    
    Parameters:
    df (pd.DataFrame): The Geldsetzer table DataFrame
    hand_hardness (str): Hand hardness value (e.g., 'F-', '4F+', 'P-', etc.)
    grain_form (str): Grain form (e.g., 'PP', 'DF', 'RG', 'FC', 'DH', etc.)
    
    Returns:
    float: Density value, or NaN if not available
    """
    try:
        return df.loc[hand_hardness, grain_form]
    except KeyError:
        return np.nan

def convert_grain_form(layer):
    """
    Convert grain form to code needed for Geldsetzer table.
    
    Parameters:
    layer: Snow layer object with grain_form_primary attribute
    
    Returns:
    str: Grain form code for Geldsetzer table lookup
    """
    if layer.grain_form_primary.sub_grain_class_code in ["PPgp","RGmx","FCmx"]:
        return layer.grain_form_primary.sub_grain_class_code
    else:
        return layer.grain_form_primary.basic_grain_class_code 