import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Set page config ---
st.set_page_config(page_title="Mortgage Retention Analysis", layout="wide")

# --- Title and Introduction ---
st.title("📈 Mortgage Retention Campaign Insights")
st.markdown("""
Welcome to the interactive dashboard analyzing the **Mortgage Retention Dialer Campaign**.

This site answers:
-  *Does answering a call increase mortgage retention?*
-  *What is the potential business impact of improved answer rates?*

Use the tabs below to explore findings, causal analysis, and strategic recommendations.
""")

# --- Sidebar ---
st.sidebar.title("Navigation")
st.sidebar.info("Use the top tabs to explore different parts of the analysis.")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("mortgage_dialer_campaign.csv")
    df['treatment'] = (df['call_result'] == 'answer').astype(int)
    return df

df = load_data()

# --- Tabs ---
tabs = st.tabs(["Executive Summary", "EDA", "Causal Analysis", "LTV Simulator", "Recommendations"])

# --- Executive Summary ---
with tabs[0]:
    st.header("📌 Executive Summary")
    st.markdown("""
    **Business Context:**
    - Retaining mortgage customers increases their 3-year LTV by €2,000 each.
    - Calls were made to customers via a dialer campaign.
    - Objective: Determine if answered calls increase retention.

    **Key Results:**
    """)
    
    model_choice = st.selectbox("Choose causal estimation method", ["OLS (16.3%)", "IV (Unstable)", "Naive"])
    causal_effect = {
        "OLS (16.3%)": 0.163,
        "IV (Unstable)": -0.25,
        "Naive": 0.283
    }[model_choice]

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Selected Estimate", f"{causal_effect*100:.1f}%", model_choice)
    kpi2.metric("Current Answer Rate", f"{(df['treatment'].mean()*100):.1f}%")
    uplift = 50000 * 0.05 * causal_effect * 2000 / 3
    kpi3.metric("Projected LTV Uplift (5% ↑)", f"€{uplift:,.0f}")

# --- EDA ---
with tabs[1]:
    st.header("🔍 Exploratory Data Analysis")

    st.subheader("Call Result Distribution")
    fig1 = px.histogram(df, x='call_result', color='call_result')
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Retention Rate by Call Result")
    grouped = df.groupby('call_result')['retained'].mean().reset_index()
    fig2 = px.bar(grouped, x='call_result', y='retained', labels={'retained': 'Retention Rate'})
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Customer Segmentation")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.histogram(df, x='age', nbins=30, title='Age Distribution'), use_container_width=True)
    with col2:
        st.plotly_chart(px.histogram(df, x='tenure', nbins=30, title='Tenure Distribution'), use_container_width=True)

# --- Causal Analysis ---
with tabs[2]:
    st.header("🧠 Causal Impact Estimation")
    st.markdown("""
    We applied multiple approaches to estimate the causal effect of a successful call (treatment):

    | Method                     | Estimated Effect | Assumptions                                      |
    |----------------------------|------------------|--------------------------------------------------|
    | Propensity Score Matching | 22%              | Conditional independence, balanced covariates    |
    | Instrumental Variable     | **-25%**         | Valid instrument (call_hour), but weak           |
    | OLS Regression            | **16.3%**        | Controls for age, balance, tenure, holdings      |
    | Naive Difference          | 28.3%            | No confounders (less trustworthy)                |

    **Conclusion:** OLS is our most reliable estimate based on statistical significance and assumptions.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/86/Causal_Model_Graphical.png", caption="Causal Graph Example")

# --- LTV Simulator ---
with tabs[3]:
    st.header("💸 Business Impact Calculator")
    st.markdown(f"""
    Adjust the slider to see the **annualized LTV uplift** from improving answer rates.

    **Assumptions:**
    - Segment = 20% of 250,000 customers = 50,000
    - LTV per additional retained = €2,000 (over 3 years)
    - Uplift per answered call = {causal_effect:.3f} (based on {model_choice})
    """)
    uplift_rate = st.slider("Increase in Answer Rate (%)", 0, 20, 5)
    estimated_uplift = 50000 * uplift_rate / 100 * causal_effect * 2000 / 3
    st.success(f"Projected Annual LTV Gain: €{estimated_uplift:,.0f}")

# --- Recommendations ---
with tabs[4]:
    st.header("📍 Recommendations & Next Steps")
    st.markdown("""
    ### 📌 Recommendation:
    **Continue the dialer campaign**, with a more **targeted approach**, focusing on customers who are:
    - **Tenure > 7 years**
    - **Age between 36 and 50**
    - **Mortgage balance in the Medium–High group**


    ### 📈 Projected Benefits:
    - Retention uplift: **Based on selected model**
    - Significant LTV gains for small answer rate improvements

    ### ⚠️ Limitations:
    - Unobserved factors may still bias estimates
    - Assumes consistent treatment effect across subsegments

    ### 🧪 Next Steps:
    - A/B test by randomizing call times
    - Cluster analysis to refine target personas
    - Follow-up with multiyear retention tracking
    """)
