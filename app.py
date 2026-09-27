import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# Load the data
df = pd.read_csv("Medical_Resources_Cleaned.csv")


# Page title and introduction
st.title("Healthcare Resources Across Lebanese Districts")

st.markdown("**Created by Celine Chatila**")

st.write(
    "This app explores how selected healthcare resources are distributed "
    "across towns within Lebanese districts."
)


# District selector
districts = sorted(df["District"].dropna().unique())

selected_district = st.selectbox(
    "Select a district",
    districts
)


# Medical resource selector
selected_resource = st.radio(
    "Select a medical resource",
    [
        "Pharmacies",
        "Hospitals",
        "Clinics",
        "Medical Centers",
        "Labs and Radiology Centers"
    ]
)


# Connect the short resource names to the dataset columns
resource_columns = {
    "Pharmacies": "Type and size of medical resources - Pharmacies",
    "Hospitals": "Type and size of medical resources - Hospitals",
    "Clinics": "Type and size of medical resources - Clinics",
    "Medical Centers": "Type and size of medical resources - Medical Centers",
    "Labs and Radiology Centers": "Type and size of medical resources - Labs and Radiology "
}

resource_column = resource_columns[selected_resource]


# Filter the data based on the selected district
filtered_df = df[df["District"] == selected_district].copy()

filtered_df[resource_column] = filtered_df[resource_column].astype(int)


# VISUALIZATION 1

st.subheader("Visualizations")

top_towns = filtered_df[["Town", resource_column]].sort_values(
    by=resource_column,
    ascending=False
).head(10)

fig_bar = px.bar(
    top_towns,
    x=resource_column,
    y="Town",
    orientation="h",
    title=f"Top 10 Towns in {selected_district} by {selected_resource}",
    labels={
        resource_column: selected_resource
    }
)

fig_bar.update_yaxes(autorange="reversed")

st.plotly_chart(fig_bar, width="stretch")


# VISUALIZATION 2

values = filtered_df[resource_column]

all_values = df[resource_column].astype(int)

max_value = int(all_values.max())

if max_value == 0:
    bin_edges = [-0.5, 0.5]
    labels = ["0"]

else:
    if max_value % 2 != 0:
        max_value = max_value + 1

    bin_edges = [-0.5, 0.5] + list(
        np.arange(2.5, max_value + 2.5, 2)
    )

    labels = ["0"] + [
        f"{i-1}-{i}"
        for i in range(2, max_value + 1, 2)
    ]


hist_values = np.histogram(
    values,
    bins=bin_edges
)[0]


range_counts = pd.DataFrame({
    "Range": labels,
    "Number of Towns": hist_values
})


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

st.plotly_chart(fig_hist, width="stretch")



# KEY INSIGHTS

st.subheader("Key Insights")

top_town = top_towns.iloc[0]["Town"]
top_value = top_towns.iloc[0][resource_column]

if top_value == 0:
    st.write(
        f"**Insight 1:** No town in {selected_district} has "
        f"any recorded {selected_resource.lower()} in this dataset."
    )
else:
    st.write(
        f"**Insight 1:** {top_town} has the highest number of "
        f"{selected_resource.lower()} in {selected_district}, "
        f"with a total of {top_value}."
    )

zero_towns = (values == 0).sum()
total_towns = len(values)

zero_percentage = round(
    (zero_towns / total_towns) * 100
)

st.write(
    f"**Insight 2:** {zero_percentage}% of towns in "
    f"{selected_district} have zero {selected_resource.lower()}."
)


# DESIGN JUSTIFICATIONS

st.subheader("Design Justifications")

with st.expander("Why use a district selectbox?"):
    st.write(
        "This feature helps the user explore one district at a time. "
        "I chose a selectbox instead of buttons or checkboxes because "
        "25 districts are represented in the dataset, and displaying "
        "all of them at once would create unnecessary clutter. "
        "The selectbox also provides geographic context by clearly "
        "showing which district is being explored."
    )


with st.expander("Why use medical resource radio buttons?"):
    st.write(
        "This feature helps the user choose one of five medical "
        "resource types. Radio buttons work well because there are "
        "only five options, so all choices can remain visible and "
        "the user can switch between them quickly. Showing one "
        "resource at a time focuses attention and keeps the "
        "comparison between towns clear."
    )
