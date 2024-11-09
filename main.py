import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to fetch and parse the daily menu using requests and BeautifulSoup
def fetch_menu_with_requests():
    url = 'https://bentley.sodexomyway.com/en-us/locations/the-921'
    response = requests.get(url)

    if response.status_code != 200:
        st.error("Failed to fetch data from the website.")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Parse menu items (adjust the class names based on the actual HTML structure)
    menu_items = []
    for item in soup.find_all('div', class_='menu-item'):  # Adjust the class name as needed
        try:
            name = item.find('div', class_='menu-item-name').text.strip()
            description = item.find('div', class_='menu-item-description').text.strip()
            allergens = item.find('div', class_='menu-item-allergens').text.strip()
            tags = item.find('div', class_='menu-item-tags').text.strip()  # Adjust as needed
            menu_items.append({
                'name': name,
                'description': description,
                'allergens': allergens,
                'tags': tags  # Tags for meal type, nutrition info, etc.
            })
        except AttributeError:
            # Handle missing elements gracefully
            pass

    return menu_items

# Streamlit app
st.title('The 921 Dietary Suggestions for Your Nutrition Goals')
st.write('Select your nutrition goals and see suitable menu items available.')

# User input for nutrition goals
goal = st.selectbox(
    'Select Your Nutrition Goal',
    ['Weight Loss', 'Muscle Gain', 'Balanced Diet']
)

# User input for dietary preferences (optional)
preferences = st.multiselect(
    'Dietary Preferences (optional)',
    ['Vegetarian', 'Vegan', 'Gluten-Free', 'Halal', 'Kosher', 'Nut-Free', 'Dairy-Free']
)

# Fetch and display the menu
if st.button('Show Menu'):
    menu_items = fetch_menu_with_requests()

    # Filter based on the nutrition goal
    filtered_menu = []
    for item in menu_items:
        if goal == 'Weight Loss' and ('mindful' in item['tags'].lower() or 'healthy' in item['tags'].lower()):
            filtered_menu.append(item)
        elif goal == 'Muscle Gain' and ('high protein' in item['tags'].lower() or 'protein' in item['description'].lower()):
            filtered_menu.append(item)
        elif goal == 'Balanced Diet':
            filtered_menu.append(item)  # Include most items for a balanced diet

    # Further filter by dietary preferences if selected
    if preferences:
        filtered_menu = [item for item in filtered_menu if any(pref.lower() in item['description'].lower() for pref in preferences)]

    # Display filtered results
    if filtered_menu:
        for item in filtered_menu:
            st.subheader(item['name'])
            st.write(item['description'])
            st.write(f"**Allergens:** {item['allergens']}")
            st.write(f"**Tags:** {item['tags']}")
    else:
        st.write('No menu items match your nutrition goals and dietary preferences.')
