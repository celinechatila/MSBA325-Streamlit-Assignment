import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("Medical_Resources_Cleaned.csv")
st.title("Healthcare Resources Across Lebanese Districts")

st.markdown("**Created by Celine Chatila**")

st.write(
    "This app explores how selected healthcare resources are distributed across towns within Lebanese districts."
)

districts = sorted(df["District"].dropna().unique())

selected_district = st.selectbox(
    "Select a district",
    districts
)


selected_resource = st.radio(
    "Select a medical resource",
    ["Pharmacies", "Hospitals", "Clinics", "Medical Centers", "Labs and Radiology Centers"]
)


resource_columns = {
    "Pharmacies": "Type and size of medical resources - Pharmacies",
    "Hospitals": "Type and size of medical resources - Hospitals",
    "Clinics": "Type and size of medical resources - Clinics",
    "Medical Centers": "Type and size of medical resources - Medical Centers",
    "Labs and Radiology Centers": "Type and size of medical resources - Labs and Radiology "
}

filtered_df = df[df["District"] == selected_district]

resource_column = resource_columns[selected_resource]

display_df = filtered_df[["Town", resource_column]].rename(
    columns={resource_column: selected_resource}
)

top_towns = display_df.sort_values(
    by=selected_resource,
    ascending=False
).head(10)

top_town = top_towns.iloc[0]["Town"]
top_value = top_towns.iloc[0][selected_resource]



st.subheader("Visualizations")


fig_bar = px.bar(
    top_towns,
    x=selected_resource,
    y="Town",
    orientation="h",
    title=f"Top 10 Towns in {selected_district} by {selected_resource}"
)

fig_bar.update_yaxes(autorange="reversed")

st.plotly_chart(fig_bar, use_container_width=True)

all_values = df[resource_column].fillna(0).astype(int)
max_value = int(all_values.max())

if max_value % 2 != 0:
    max_value = max_value + 1

bins = [-1, 0] + list(range(2, max_value + 2, 2))

labels = ["0"] + [
    f"{i-1}-{i}" for i in range(2, max_value + 2, 2)
]

hist_df = filtered_df.copy()

hist_df["Range"] = pd.cut(
    hist_df[resource_column].fillna(0).astype(int),
    bins=bins,
    labels=labels
)

range_counts = hist_df["Range"].value_counts().reindex(labels, fill_value=0).reset_index()
range_counts.columns = ["Range", "Number of Towns"]

fig_hist = px.bar(
    range_counts,
    x="Range",
    y="Number of Towns",
    title=f"Distribution of {selected_resource} in {selected_district}"
)

fig_hist.update_layout(
    xaxis_title=f"Number of {selected_resource}",
    yaxis_title="Number of Towns"
)

st.plotly_chart(fig_hist, use_container_width=True)


st.subheader("Key Insights")

st.write(
    f"**Insight 1:** {top_town} has the highest number of {selected_resource.lower()} "
    f"in {selected_district}, with a total of {top_value} {selected_resource}."
)


zero_towns = (filtered_df[resource_column] == 0).sum()
total_towns = len(filtered_df)

zero_percentage = round((zero_towns / total_towns) * 100)

st.write(
    f"**Insight 2:** {zero_percentage}% of towns in {selected_district} "
    f"have zero {selected_resource.lower()}."
)


st.subheader("Design Justifications")

with st.expander("Why use a district dropdown?"):
    st.write(
        "This feature helps the user explore healthcare resources within one specific district in Lebanon at a time. "
        "The district dropdown was chosen instead of buttons and checkboxes because there are 25 districts represented in the dataset "
        "and having them displayed on the screen all at once would create unnecessary clutter. "
        "This widget provides the user with geographic context by showing the user which district he is exploring."
    )

with st.expander("Why use medical resource radio buttons?"):
    st.write(
        "This feature helps the user choose which medical resource type he wants to examine within the selected district. "
        "There are only five options of medical resources, so using radio buttons and making them visible all at once allows the user to quickly and easily switch between them. "
        "This widget focuses the user's attention on one resource at a time and keeps the comparison between towns clear."
    )
