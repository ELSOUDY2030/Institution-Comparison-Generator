
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import random
from huggingface_hub import login


login("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")

name_model = 'google/gemma-2-9b-it'

quantization_config = BitsAndBytesConfig(load_in_4bit=True)

tokenizer = AutoTokenizer.from_pretrained(name_model)
model = AutoModelForCausalLM.from_pretrained(name_model, quantization_config=quantization_config,
                                                low_cpu_mem_usage=True,
                                                device_map="auto" )


st.title("Institution Comparative Analysis Generator")

institution_name = st.text_input("Enter the name of the institution:", "Police")

use_random_countries = st.checkbox("Use random countries for comparison")

if use_random_countries:
    country1 = st.text_input("Enter the first country:", "EGYPT")
    prompt = f"""
    You will be provided with the name of an institution and its country.
    Your task is to perform a concise comparative analysis by evaluating this institution and its counterparts in THREE COUNTRIES, including the provided country and two additional countries of your choice.
    The analysis for each country should be structured as follows:

    **[Country Name] [Institution Name]**

    *   **Performance Metrics:**
        *   **Response Time:** [Metric]
        *   **Clearance Rate:** [Metric]
        *   **Public Satisfaction:** [Metric]
    *   **Key Risks:**
        *   **Risk 1:** [Description]
        *   **Risk 2:** [Description]
        *   **Risk 3:** [Description]
    *   **Strategies for Mitigating Risks:**
        *   **Strategy 1:** [Description]
        *   **Strategy 2:** [Description]
        *   **Strategy 3:** [Description]

    Provide the analysis for each country in a concise manner.
    Do not include any additional observations or conclusions after the comparison.

    Institution: {institution_name}, COUNTRY: {country1}, and TWO ADDITIONAL COUNTRIES of your choice.
    """

else:
    country1 = st.text_input("Enter the first country:", "EGYPT")
    country2 = st.text_input("Enter the second country:", "QATAR")
    country3 = st.text_input("Enter the third country:", "KSA")
    prompt = f"""
    You will be given the name of an institution and its country.
    Your task is to perform a concise comparative analysis by evaluating this institution and its counterparts in the following THREE COUNTRIES: {country1}, {country2} and {country3}.
    The analysis for each country should be structured as follows:

    **[Country Name] [Institution Name]**

    *   **Performance Metrics:**
        *   **Response Time:** [Metric]
        *   **Clearance Rate:** [Metric]
        *   **Public Satisfaction:** [Metric]
    *   **Key Risks:**
        *   **Risk 1:** [Description]
        *   **Risk 2:** [Description]
        *   **Risk 3:** [Description]
    *   **Strategies for Mitigating Risks:**
        *   **Strategy 1:** [Description]
        *   **Strategy 2:** [Description]
        *   **Strategy 3:** [Description]

    Provide the analysis in a brief and concise manner for each country.
    Do not add any observations or conclusions after the comparison.

    Institution: {institution_name} and the THREE COUNTRIES: {country1}, {country2} and {country3}
    """

if st.button("Generate Analysis"):
    inputs = tokenizer(prompt, return_tensors="pt")

    output = model.generate(**inputs,
                            max_length=1500,
                            num_return_sequences=1,
                            do_sample=True,
                            temperature=0.3,
                            top_p=0.6,
                            top_k=30
                           )


    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)


    st.subheader("Generated Analysis:")
    st.write(generated_text)

