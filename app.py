import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from openai import OpenAI

temperature=0.4
frequency_penalty=0.0

client = OpenAI(
    api_key=st.secrets["OPENAI_API"]
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

def convert_dataframe_to_prompt(df, title):
    prompt = f"This data contains data about {title}:\n"
    for column in df.columns:
        prompt += f"{column}: \n"
        for value in df[column]:
            prompt += f"{value} "
        prompt += "\n"
    prompt += "\n\n"
    return prompt



def generate_gpt4_response(prompt, api_key):
    client = OpenAI(api_key=api_key)
    gpt_assistant_prompt = f"You are a professional tour firms / agents / operators manager!"

    message=[{"role": "assistant", "content": gpt_assistant_prompt}, {"role": "user", "content": prompt}]

    st.session_state.messages.append({"role": "assistant", "content": gpt_assistant_prompt})
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=st.session_state.openai_model,
        messages = message,
        temperature=temperature,
        frequency_penalty=frequency_penalty
    )

    return response.choices[0].message.content

st.set_page_config(
    layout="wide",
    page_title="TourChecker",
    page_icon="🌎"
)

model_id = "lmsys/fastchat-t5-3b-v1.0"
filenames = [ 
    "pytorch_model.bin", "added_tokens.json", "config.json", "generation_config.json",
    "special_tokens_map.json", "spiece.model", "tokenizer_config.json"
]

st.title("🌴 TourChecker")
st.write("Welcome to TourChecker! This app is designed to help you find secure and reliable travel agencies and operators in Kazakhstan!")

tour_agents_df = pd.read_csv("data/tour_agents.csv")
tour_operators_df = pd.read_csv("data/tour_operators.csv")

# Search Bar
search_query = st.text_input("Ask a question about tour agents", "")

# Search Button
search_button = st.button("🔍 Search")

# Check Reliability
if search_button:
    st.subheader("Search Results")
    with st.spinner('⚙ Searching...'):
        try:
            tour_prompt = convert_dataframe_to_prompt(tour_agents_df[:50], "Tour Agents")
            response = generate_gpt4_response(search_query + tour_prompt, st.secrets["OPENAI_API"])
            st.markdown(response)

        except Exception as e:
            print('Error:', e)
            st.info("No results found. Please try again.")

colA, colB = st.columns(2)
with colA:
    # download button for tour agents csv
    st.markdown(
        f'<a href="data/tour_agents.csv" download="tour_agents.csv">Download Tour Agents CSV</a>',
        unsafe_allow_html=True
    )

with colB:
    # download button for tour operators csv
    st.markdown(
        f'<a href="data/tour_operators.csv" download="tour_operators.csv">Download Tour Operators CSV</a>',
        unsafe_allow_html=True
    )

st.markdown("---")

def bar_chart_by_city(df, title):
    city_counts = df['city'].value_counts()

    plt.figure(figsize=(8, 4))  # Adjust the figsize to make the chart smaller
    city_counts.plot(kind='bar')
    plt.title(f'Number of Tour {title} by City')
    plt.xlabel('City')
    plt.ylabel(f'Number of Tour {title}')
    plt.xticks(rotation=45) 
    st.pyplot(plt.gcf())

def histogram_by_scores(df):
    # Create subplots with shared y-axis
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharey=True)

    # Plot histogram for system review scores on the left
    ax1.hist(df['system_score'].dropna(), bins=10, color='blue', alpha=0.7, rwidth=0.8)
    ax1.set_title('System Review Scores Histogram', fontsize=6)
    ax1.set_xlabel('System Review Score', fontsize=6)
    ax1.set_ylabel('Frequency', fontsize=6)
    ax1.grid(True)

    # Plot histogram for user review scores on the right
    ax2.hist(df['user_score'].dropna(), bins=10, color='green', alpha=0.7, rwidth=0.8)
    ax2.set_title('User Review Scores Histogram', fontsize=6)
    ax2.set_xlabel('User Review Score', fontsize=6)
    ax2.grid(True)

    # Adjust layout to prevent overlapping of labels
    plt.tight_layout()
    st.pyplot(plt.gcf())

def main():
    # Review Scores Histogram
    st.subheader('Tour Agents Review Scores Analysis')
    histogram_by_scores(tour_agents_df)
    st.subheader('Tour Operators Review Scores Analysis')
    histogram_by_scores(tour_operators_df)

    st.markdown("---")
    
    # Tour Agents by City Bar Chart
    st.subheader('Tour Agents by City')
    bar_chart_by_city(tour_agents_df, 'Agents')
    st.subheader('Tour Operators by City')
    bar_chart_by_city(tour_operators_df, 'Operators')

    # Tables for Tour Agents and Tour Operators
    st.subheader('Tour Agents')
    st.dataframe(tour_agents_df)
    st.subheader('Tour Operators')
    st.dataframe(tour_operators_df)

if __name__ == "__main__":
    main()
