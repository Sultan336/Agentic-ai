import streamlit as st
import requests
from typing import Optional, Tuple

def fetch_country_data(country_name: str) -> Optional[Tuple[str, str, int, float, str, str]]:
    url = f"https://restcountries.com/v3/name/{country_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        
        # Debugging: Print the entire data to check the structure
       # st.write(data)  # This will display the JSON response in the Streamlit app

        if isinstance(data, list) and len(data) > 0:
            country_data = data[0]
            name = country_data["name"]["common"]
            capital = country_data["capital"][0]
            population = country_data["population"]
            area = country_data["area"]
            region = country_data["region"]
            country_code = country_data["cca2"]
            flag_emoji = chr(127397 + ord(country_code[0])) + chr(127397 + ord(country_code[1]))
            return name, capital, population, area, region, flag_emoji
        else:
            st.error("⚠️ Error: Unexpected data format received from API.")
            return None
    except (requests.exceptions.HTTPError, IndexError, KeyError, TypeError) as e:
        st.error(f"❌ Error fetching data: {e}")
        return None

def main() -> None:
    st.title("🌍 Country Information App")
    country_name = st.text_input("🔍 Enter a country name: ")

    if country_name:
        with st.spinner("Fetching data..."):
            country_info = fetch_country_data(country_name)
        if country_info:
            name, capital, population, area, region, flag_emoji = country_info

            st.subheader("📋 Country Information")
            st.write(f'**Name**: {name} {flag_emoji}')
            st.write(f'**Capital**: {capital}')
            st.write(f'**Population**: {population:,}')
            st.write(f'**Area**: {area:,} square kilometers')
            st.write(f'**Region**: {region}')
        else:
            st.error("⚠️ Error: Country data not found!")

if __name__ == "__main__":
    main()