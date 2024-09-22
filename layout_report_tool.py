from pptx import Presentation
import pandas as pd
import os

def list_placeholders(design_number: int) -> pd.DataFrame:
    """
    Lists the placeholders in a PowerPoint design and returns a DataFrame.

    Parameters:
    design_number (int): The design number of the PowerPoint file.

    Returns:
    pd.DataFrame: DataFrame containing placeholder details.
    """
    placeholders_data = []
    design_file_path = f"Powerpointer-main/Designs/Design-{design_number}.pptx"

    if not os.path.exists(design_file_path):
        raise FileNotFoundError(f"Design file '{design_file_path}' not found.")

    prs = Presentation(design_file_path)

    for i, layout in enumerate(prs.slide_layouts):
        for shape in layout.placeholders:
            placeholder_format = shape.placeholder_format
            placeholders_data.append([
                i,
                placeholder_format.idx,
                shape.shape_id,
                shape.name,
                placeholder_format.type,
                shape.width,
                shape.height,
                shape.left,
                shape.top
            ])

    df = pd.DataFrame(placeholders_data, columns=[
        'Layout Index', 'Placeholder Index', 'Shape ID', 'Name', 'Type', 'Width', 'Height', 'Left', 'Top'
    ])

    return df

def color_rows_by_layout(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies color to rows of DataFrame based on the layout index.

    Parameters:
    df (pd.DataFrame): DataFrame containing placeholder details.

    Returns:
    pd.DataFrame: DataFrame with applied row colors.
    """
    def apply_colors(row):
        colors = [
            'background-color: #ffcccc',  # Light red
            'background-color: #ccffcc',  # Light green
            'background-color: #ccccff',  # Light blue
            'background-color: #ffffcc',  # Light yellow
            'background-color: #ffccff',  # Light pink
            'background-color: #ccffff',  # Light cyan
            'background-color: #ffd700',  # Gold
            'background-color: #e6e6fa'  # Lavender
        ]
        return [colors[row['Layout Index'] % len(colors)]] * len(row)

    styled_df = df.copy()
    styled_df['Color'] = [apply_colors(row) for _, row in styled_df.iterrows()]

    return styled_df

def get_placeholder_indices_by_layout(df: pd.DataFrame) -> tuple:
    """
    Retrieves placeholder indices grouped by layout index.

    Parameters:
    df (pd.DataFrame): DataFrame containing placeholder details.

    Returns:
    tuple: A tuple containing:
        - List of lists of placeholder indices by layout.
        - List of unique layout indices.
        - List of content placeholder indices by layout.
    """
    placeholder_indices_by_layout = df.groupby('Layout Index')['Placeholder Index'].apply(list).tolist()
    layout_indices = df['Layout Index'].unique().tolist()

    filtered_df = df[df['Name'].str.startswith('Content Placeholder')]
    grouped = filtered_df.groupby('Layout Index')['Placeholder Index'].apply(list)
    index_containing_placeholders = grouped.tolist()

    return placeholder_indices_by_layout, layout_indices, index_containing_placeholders

def supporting_parameters(design_number: int) -> tuple:
    """
    Generates supporting parameters for the given design number.

    Parameters:
    design_number (int): The design number of the PowerPoint file.

    Returns:
    tuple: A tuple containing:
        - List of lists of placeholder indices by layout.
        - List of unique layout indices.
        - List of lists of content placeholder indices by layout.
    """
    placeholders_df = list_placeholders(design_number)
    styled_df = color_rows_by_layout(placeholders_df)
    placeholder_indices_by_layout_, layout_indices_, index_containing_placeholders = get_placeholder_indices_by_layout(placeholders_df)

    return placeholder_indices_by_layout_, layout_indices_, index_containing_placeholders
