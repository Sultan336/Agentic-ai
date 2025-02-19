import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# ----------------------------
# Simulation Functions
# ----------------------------

def simulate_text(text_name, num_chapters, verses_range, avg_words, std_words):
    """
    Simulate chapter and verse data for a given text.
    """
    data = []
    for chapter in range(1, num_chapters + 1):
        # Randomly decide the number of verses in this chapter.
        num_verses = np.random.randint(verses_range[0], verses_range[1] + 1)
        for verse in range(1, num_verses + 1):
            # Simulate word count using a normal distribution.
            word_count = int(np.random.normal(avg_words, std_words))
            word_count = max(word_count, 1)  # Ensure at least one word.
            data.append({
                "Text": text_name,
                "Chapter": chapter,
                "Verse": verse,
                "WordCount": word_count
            })
    return pd.DataFrame(data)

# ----------------------------
# Simulate Data for Each Text
# ----------------------------

# Quran: 114 chapters, verses between 3 and 30, ~15 words per verse on average.
df_quran = simulate_text("Quran", num_chapters=114, verses_range=(3, 30), avg_words=15, std_words=4)
# Add revelation info for the Quran.
# Traditionally, approximately 86 chapters are Meccan and 28 are Medinan.
df_quran["Revelation"] = df_quran["Chapter"].apply(lambda x: "Makkah" if x <= 86 else "Madinah")

# Torah: 187 chapters (across 5 books), verses between 10 and 40, ~20 words per verse on average.
df_torah = simulate_text("Torah", num_chapters=187, verses_range=(10, 40), avg_words=20, std_words=5)

# Bible: Simulated with 100 chapters (for demonstration), verses between 5 and 40, ~25 words per verse on average.
df_bible = simulate_text("Bible", num_chapters=100, verses_range=(5, 40), avg_words=25, std_words=6)

# Combine all data.
df = pd.concat([df_quran, df_torah, df_bible], ignore_index=True)

# ----------------------------
# Sidebar for Interactive Filtering
# ----------------------------

st.sidebar.header("Filter Options")
selected_texts = st.sidebar.multiselect(
    "Choose one or more texts:",
    options=df["Text"].unique(),
    default=df["Text"].unique()
)

# Determine chapter range from the selected texts.
if not df[df["Text"].isin(selected_texts)].empty:
    min_chapter = int(df[df["Text"].isin(selected_texts)]["Chapter"].min())
    max_chapter = int(df[df["Text"].isin(selected_texts)]["Chapter"].max())
else:
    min_chapter, max_chapter = 1, 1

selected_range = st.sidebar.slider(
    "Select Chapter Range:",
    min_value=min_chapter,
    max_value=max_chapter,
    value=(min_chapter, max_chapter)
)

# Filter data based on selected texts and chapter range.
filtered_df = df[
    (df["Text"].isin(selected_texts)) & 
    (df["Chapter"] >= selected_range[0]) & 
    (df["Chapter"] <= selected_range[1])
]

# ----------------------------
# Main Dashboard Title & Description
# ----------------------------

st.title("Enhanced Comparative EDA: Quran, Bible, and Torah")
st.markdown("""
This interactive dashboard compares key structural metrics of three major religious texts. In addition to the standard charts (distribution, boxplots, line charts, etc.), 
there’s a special focus on the Quran’s revelation details. Traditionally, the Quran’s 114 chapters are divided into those revealed in **Makkah** and **Madinah**. 
Use the sidebar to filter by text and chapter range, and check the boxes below for additional interactive charts.
""")

# ----------------------------
# Check for Data
# ----------------------------

if filtered_df.empty:
    st.write("No data available for the selected options. Adjust your filters and try again.")
else:
    # 1. Distribution: Histogram with marginal boxplot for Word Count per Verse.
    st.subheader("Word Count Distribution per Verse")
    fig_hist = px.histogram(
        filtered_df,
        x="WordCount",
        color="Text",
        nbins=30,
        marginal="box",
        opacity=0.7,
        title="Distribution of Word Counts per Verse"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # 2. Boxplot: Average Word Count per Chapter.
    avg_per_chapter = filtered_df.groupby(["Text", "Chapter"])["WordCount"].mean().reset_index()
    st.subheader("Boxplot of Average Word Count per Chapter")
    fig_box = px.box(
        avg_per_chapter,
        x="Text",
        y="WordCount",
        points="all",
        title="Average Word Count per Chapter"
    )
    fig_box.update_traces(opacity=0.7)
    st.plotly_chart(fig_box, use_container_width=True)

    # 3. Line Chart: Trend of Average Word Count by Chapter.
    st.subheader("Line Chart: Average Word Count by Chapter")
    fig_line = px.line(
        avg_per_chapter,
        x="Chapter",
        y="WordCount",
        color="Text",
        title="Trend of Average Word Count Across Chapters"
    )
    fig_line.update_traces(opacity=0.7)
    st.plotly_chart(fig_line, use_container_width=True)

    # 4. Violin Plot: Detailed Distribution of Average Word Count per Chapter.
    st.subheader("Violin Plot: Distribution of Average Word Count per Chapter")
    fig_violin = px.violin(
        avg_per_chapter,
        x="Text",
        y="WordCount",
        box=True,
        points="all",
        title="Violin Plot of Average Word Count per Chapter",
       # opacity=0.7
    )
    st.plotly_chart(fig_violin, use_container_width=True)

    # 5. Density Plot: Kernel Density Estimation of Verse Word Counts.
    st.subheader("Density Plot: Verse Word Count Density")
    fig_density = px.histogram(
        filtered_df,
        x="WordCount",
        color="Text",
        nbins=30,
        histnorm="density",
        opacity=0.7,
        title="Density Plot of Word Counts per Verse"
    )
    st.plotly_chart(fig_density, use_container_width=True)

    # 6. Scatter Plot: Individual Verse Word Counts vs. Chapter Number.
    st.subheader("Scatter Plot: Word Count vs. Chapter")
    fig_scatter = px.scatter(
        filtered_df,
        x="Chapter",
        y="WordCount",
        color="Text",
        title="Scatter Plot of Verse Word Counts by Chapter",
        opacity=0.7
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # 7. Summary Statistics Table.
    st.subheader("Summary Statistics")
    summary_stats = filtered_df.groupby("Text")["WordCount"].describe().reset_index()
    st.dataframe(summary_stats)

    # ----------------------------
    # Additional Interactive Section for Quran Revelation Analysis
    # ----------------------------
    if "Quran" in selected_texts:
        st.subheader("Quran Revelation Analysis")
        st.markdown("""
        The Quran is traditionally divided into chapters revealed in **Makkah** and **Madinah**. 
        Approximately 75% of its chapters are classified as Makkah (typically earlier revelations) and 25% as Madinah.
        """)
        show_quran_revelation = st.checkbox("Show Quran Revelation Charts", value=True)
        if show_quran_revelation:
            # Filter Quran-specific data from the original (non-filtered) df_quran to get complete chapter info.
            df_quran_chapters = df_quran.groupby(["Chapter", "Revelation"])["WordCount"].mean().reset_index()
            
            # a) Pie Chart: Proportion of Chapters by Revelation.
            revelation_counts = df_quran_chapters.groupby("Revelation")["Chapter"].nunique().reset_index()
            fig_quran_pie = px.pie(
                revelation_counts,
                names="Revelation",
                values="Chapter",
                title="Proportion of Quran Chapters by Revelation",
                hole=0.3,
                opacity=0.7
            )
            st.plotly_chart(fig_quran_pie, use_container_width=True)

            # b) Bar Chart: Average Word Count per Chapter by Revelation.
            avg_word_revelation = df_quran_chapters.groupby("Revelation")["WordCount"].mean().reset_index()
            fig_quran_bar = px.bar(
                avg_word_revelation,
                x="Revelation",
                y="WordCount",
                title="Average Word Count per Chapter by Revelation (Quran)",
                opacity=0.7
            )
            st.plotly_chart(fig_quran_bar, use_container_width=True)

            # c) Violin Plot: Distribution of Chapter Average Word Counts by Revelation.
            fig_quran_violin = px.violin(
                df_quran_chapters,
                x="Revelation",
                y="WordCount",
                box=True,
                points="all",
                title="Distribution of Chapter Average Word Count by Revelation (Quran)",
               # opacity=0.7
            )
            st.plotly_chart(fig_quran_violin, use_container_width=True)

    # ----------------------------
    # Final Remarks
    # ----------------------------
    st.markdown("### Key Takeaways")
    st.markdown("""
    - **Multiple Chart Types:** From histograms and boxplots to violin and density plots, different charts provide unique insights.
    - **Interactive Filters:** Use the sidebar to select texts and adjust the chapter range.
    - **Quran Revelation Analysis:** Additional charts reveal that approximately 75% of Quran chapters are Makkah-revealed while 25% are Madinah-revealed, with differences in average word counts.
    - **Transparency:** Adjusted opacities help clarify overlapping data.
    - **Summary Stats:** The table offers numeric context for the visual insights.
    """)
