def style_toplist(df):
    """Tar emot en DataFrame och returnerar en stylad version med svarta headers."""
    styled_df = df.style.set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#000000'), ('color', '#ffffff')]}
    ])
    return styled_df