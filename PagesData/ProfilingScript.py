import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from multipage_streamlit import State
from Utility.Languages import language_complex_analysis, language_dynamic_analysis


def complex_analysis() -> None:
    state = State(__name__)
    """Create complex analysis from load data frame. We can choose column for detail analysis"""
    # choose Language dictionary for translation
    L = language_complex_analysis[st.session_state.LANGUAGE]

    st.title(L["title"])

    _df = st.session_state.df

    # Store selected columns in session_state with a key
    selected_columns = st.multiselect(
        L["select_columns"],
        _df.columns.to_list(),
        key=state("complex_analysis_selected_columns")

    )
    # Main Information
    with st.expander(L["main_info"], expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(L["total_records"], _df.shape[0])
        with col2:
            st.metric(L["num_features"], _df.shape[1])
        with col3:
            st.metric(L["missing_values"], _df.isna().sum().sum())

        st.write(L["data_types"])
        dtypes = _df.dtypes.reset_index()
        dtypes.columns = [L["column"], L["type"]]
        st.dataframe(dtypes, hide_index=True)

    if not selected_columns:
        st.warning(L["no_columns_selected"])
        st.stop()

    filtered_df = _df[selected_columns]

    # Data Type Separation
    numeric_cols = filtered_df.select_dtypes(include='number').columns.tolist()
    categorical_cols = filtered_df.select_dtypes(exclude='number').columns.tolist()

    # Statistics
    with st.expander(L["statistics"]):
        if numeric_cols:
            st.subheader(L["numeric_stats"])
            st.dataframe(filtered_df[numeric_cols].describe().T)

        if categorical_cols:
            st.subheader(L["categorical_stats"])
            stats = []
            for col in categorical_cols:
                stats.append({
                    L["column_name"]: col,
                    L["unique_values"]: filtered_df[col].nunique(),
                    L["most_frequent"]: filtered_df[col].mode().iloc[0],
                    L["frequency"]: filtered_df[col].value_counts().iloc[0]
                })
            st.dataframe(pd.DataFrame(stats))


    # Visualizations
    with st.expander(L["visualizations"]):
        tab1, tab2, tab3, tab4 = st.tabs([
            L["distributions"],
            L["correlations"],
            L["missing_values_heatmap"],
            L["categorical_analysis"],
        ])

        with tab1:
            try:
                if numeric_cols:

                    col = st.selectbox(L["select_numeric_column"], numeric_cols, key=state("complex_analysis_numeric_column_selectbox"))
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

                    # Histogram
                    sns.histplot(filtered_df[col], kde=True, ax=ax1)
                    ax1.set_title(f"{L['distribution']} {col}")

                    # Boxplot
                    sns.boxplot(x=filtered_df[col], ax=ax2)
                    ax2.set_title(f"{L['boxplot']} {col}")
                    st.pyplot(fig)
                else:
                    st.warning(L["no_numeric_cols"])
            except Exception as e:
                st.error(e)

        with tab2:
            if len(numeric_cols) > 1:
                st.subheader(L["correlation_matrix"])
                corr = filtered_df[numeric_cols].corr()
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
                st.pyplot(fig)
            else:
                st.warning(L["need_more_numeric_cols"])

        with tab3:
            st.subheader(L["missing_values_matrix"])
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.heatmap(filtered_df.isna().T, cmap="viridis", cbar=False)
            ax.set_title(L["missing_values_heatmap_title"])
            st.pyplot(fig)

        with tab4:
            if categorical_cols:
                col = st.selectbox(L["select_categorical_column"], categorical_cols,key=state("complex_analysis_categorical_column_selectbox"))
                top_n = st.slider(L["top_n_values"], 5, 50, 10,key="complex_analysis_top_n_slider")
                counts = filtered_df[col].value_counts().nlargest(top_n)
                fig, ax = plt.subplots(figsize=(10, 4))
                sns.barplot(x=counts.index, y=counts.values, ax=ax)
                plt.xticks(rotation=45)
                ax.set_title(f"{L['top_n_values']} {top_n} {L['in']} {col}")  # Improved title
                st.pyplot(fig)
            else:
                st.warning(L["no_categorical_cols"])

    # Detailed Analysis
    with st.expander(L["detailed_analysis"]):
        st.subheader(L["data_preview"])
        rows = st.slider(L["num_rows"], 5, 100, 10,key="complex_analysis_rows_slider")
        st.dataframe(filtered_df.head(rows), use_container_width=True)
        if st.checkbox(L["show_column_info"],key=state("complex_analysis_show_column_info_checkbox")):
            for col in selected_columns:
                st.write(f"**{col}**")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(L["first_values"], filtered_df[col].head().tolist())
                with col2:
                    st.write(L["unique_values_count"], filtered_df[col].nunique())
                st.divider()
        state.save()

def dynamic_analysis() -> None:
    state = State(__name__)
    # Language selection
    L = language_dynamic_analysis[st.session_state.LANGUAGE]
    st.title(L["title"])
    filtered_df = st.session_state.df
    selected_columns = st.multiselect(
        "Выберите колонки:",
        filtered_df.columns,
        key=state("dynamic_analysis")
    )
    if not selected_columns:
        st.warning("please select columns for analise")
        st.stop()


    # 2. Dynamic cascade filters
    with st.expander("Dynamic cascade filters"):
        for idx, column in enumerate(selected_columns):
            available_options = filtered_df[column].unique().tolist()
            selected_values = st.multiselect(
                L["filter_label"].format(column, len(available_options)),
                options=available_options,
                key=state(f"filter_{column}_{idx}")
            )
            if selected_values:
                filtered_df = filtered_df[filtered_df[column].isin(selected_values)]
    updated_df = filtered_df[selected_columns] if selected_columns else filtered_df
    # 3. Display filtered results

    st.subheader(L["results_header"])
    st.write(L["found_records"].format(len(filtered_df)))
    st.dataframe(updated_df)
    # 4. Analysis section
    st.subheader(L["analysis_header"])

    # 5. Grouping and aggregation with all functions
    st.markdown(f"**{L['grouping_header']}**")
    group_cols = st.multiselect(
        L["group_columns"],
        options=updated_df.columns,
        key=state("group_by")
    )

    numeric_cols = updated_df.select_dtypes(include=np.number).columns.tolist()
    agg_cols = st.multiselect(
        L["agg_columns"],
        options=numeric_cols,
        key=state("agg_cols")
    )

    # Fixed aggregation functions
    agg_funcs = ['sum', 'mean', 'median', 'min', 'max', 'count']

    if group_cols and agg_cols:
        try:
            grouped_df = updated_df.groupby(group_cols)[agg_cols].agg(agg_funcs)
            st.write(L["group_result"])
            st.dataframe(grouped_df.reset_index().round(2))
        except Exception as e:
            st.error(L["error_grouping"].format(str(e)))

    # 6. Pivot table
    st.markdown(f"**{L['pivot_header']}**")
    col1, col2, col3 = st.columns(3)

    with col1:
        pivot_index = st.selectbox(L["pivot_rows"], updated_df.columns, key=state("pivot_index"))
    with col2:
        pivot_columns = st.selectbox(L["pivot_columns"], updated_df.columns, key=state("pivot_columns"))
    with col3:
        pivot_values = st.selectbox(L["pivot_values"], numeric_cols, key=state("pivot_values"))

    pivot_func = st.selectbox(
        L["agg_function"],
        options=['mean', 'sum', 'count', 'min', 'max'],
        key=state("pivot_func")
    )

    if pivot_index and pivot_values and pivot_func:
        try:
            pivot_table = pd.pivot_table(
                filtered_df,
                index=pivot_index,
                columns=pivot_columns,
                values=pivot_values,
                aggfunc=pivot_func,
                fill_value=0
            )
            st.write(L["pivot_result"])
            st.dataframe(pivot_table.round(2))
        except Exception as e:
            st.error(L["error_pivot"].format(str(e)))

    state.save()