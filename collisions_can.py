
import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px
from matplotlib.ticker import FuncFormatter

# pickel for fast load times -> pickleize.py
collision_df = pd.read_pickle('./data/2019_collisions.pkl')
collision_df = collision_df[collision_df['C_WDAY'] != 'U']

st.set_page_config(layout="wide", page_title="Collisions Canada")
st.header(f"Collisions Canada - 2019")
st.link_button(label='Go to Data Source - National Collision Database', url="https://open.canada.ca/data/dataset/1eb9eba7-71d1-4b30-9fb1-30cbdab7e63a")

year_tab, avg_tab = st.tabs(["Yearly & Totalized Statistics", "Averages"])
# hackity-hack
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


with year_tab:
  # only keep first occurence of each unique ud in the 'C_CASE' col
  # rows with the same 'C_CASE' value are from the same accident
  unique_collisions = collision_df.drop_duplicates(subset='C_CASE', keep='first')
  n_formatted = f"{len(unique_collisions):,}"
  col1, col2 = st.columns(2)

  with col1:
    # graph that shit
    st.subheader(f"# of Collisions by Day of the Week (n={(n_formatted)})")
    fig, ax = plt.subplots(figsize=(9, 5.5), facecolor='none')
    ax.set_facecolor('none')
    n, bins, patches = ax.hist(unique_collisions['C_WDAY'], bins=range(1, 9), align='left', color='#76b5c5', edgecolor='none', rwidth=0.8)
    ax.set_xticks(range(1, 8))
    ax.set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'], color='white', )
    ax.set_frame_on(False)
    ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.25)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.tick_params(axis='x', which='major', labelsize=10, colors='white')
    ax.tick_params(axis='y', which='major', labelsize=10, colors='white')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x:,.0f}'))
    st.pyplot(fig, transparent=True)

  with col2:
    st.subheader(f"Collisions by Type (n={(n_formatted)})")
    code_descriptions = {
        1: 'Hit a moving object',
        2: 'Hit a stationary object',
        3: 'Ran off left shoulder',
        4: 'Ran off right shoulder',
        5: 'Rollover on roadway',
        6: 'Other single vehicle collision',
        21: 'Rear-end collision',
        22: 'Side swipe',
        23: 'Vehicle passing left or left turn conflict',
        24: 'Vehicle passing right or right turn conflict',
        25: 'Other two vehicle - same direction',
        31: 'Head-on collision',
        32: 'Approaching side-swipe',
        33: 'Left turn across opposing traffic',
        34: 'Right turn, including conflicts',
        35: 'Right angle collision',
        36: 'Other two-vehicle - different direction',
        41: 'Hit a parked motor vehicle',
        'QQ': 'Other',
        'UU': 'Unknown',
        'XX': 'Data not provided'
    }

    unique_collisions['C_CONF_DESC'] = unique_collisions['C_CONF'].map(code_descriptions)
    fig, ax = plt.subplots(figsize=(11, 11), facecolor='none')  # Adjusted figure size
    collision_counts = unique_collisions['C_CONF_DESC'].value_counts()
    wedges, texts, autotexts = ax.pie(collision_counts, colors=plt.cm.tab20.colors, autopct='', startangle=90)
    legend = ax.legend(wedges, collision_counts.index,
                      title="Collision Types",
                      loc="center left",
                      bbox_to_anchor=(1, 0, 0.5, 1),
                      frameon=False,
                      )

    plt.setp(legend.get_texts(), color='white', size=20)
    ax.axis('equal')
    plt.setp(autotexts, size=8, weight="bold", color='white')
    st.pyplot(fig, transparent=True)

with avg_tab:
  pass
