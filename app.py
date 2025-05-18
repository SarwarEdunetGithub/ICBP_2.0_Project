import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

@st.cache_data
def load_data():
    data = pd.read_csv("food_nutrition.csv")
    data['cook_time_minutes'] = data['cook_time_minutes'].fillna(data['cook_time_minutes'].median())
    return data

data = load_data()

st.set_page_config(
    page_title="The Smartest AI Nutrition Assistant",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title("👤 User Profile")
    st.subheader("Tell us about yourself")
    
    age = st.slider("Age", 18, 80, 30)
    gender = st.radio("Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", 40, 150, 70)
    height = st.number_input("Height (cm)", 140, 220, 170)
    activity_level = st.selectbox(
        "Activity Level",
        ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
    )
    dietary_preferences = st.multiselect(
        "Dietary Preferences",
        ["Vegetarian", "Vegan", "Gluten-Free", "Low-Carb", "High-Protein", "Low-Fat", "Dairy-Free"]
    )
    health_goals = st.multiselect(
        "Health Goals",
        ["Weight Loss", "Muscle Gain", "Maintenance", "Heart Health", "Diabetes Management", "Energy Boost"]
    )
    allergies = st.multiselect(
        "Allergies",
        ["Nuts", "Shellfish", "Dairy", "Eggs", "Soy", "Wheat", "Fish", "None"]
    )
    
    st.divider()
    st.subheader("Daily Targets")
    target_calories = st.slider("Calories (kcal)", 1200, 3000, 2000)
    target_protein = st.slider("Protein (g)", 20, 200, 100)
    target_carbs = st.slider("Carbs (g)", 50, 400, 200)
    target_fat = st.slider("Fat (g)", 20, 150, 70)
    
    st.divider()
    if st.button("Reset Preferences"):
        st.experimental_rerun()

st.title("🍏 The Smartest AI Nutrition Assistant")
st.subheader("Personalized nutrition guidance powered by AI")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Dashboard", 
    "🔍 Food Explorer", 
    "🍽️ Meal Planner", 
    "📊 Nutrition Analysis", 
    "📝 Health Insights"
])

with tab1: 
    st.subheader("Recommended Foods")
    
    
    filtered_data = data.copy()
    
    if "Vegetarian" in dietary_preferences:
        filtered_data = filtered_data[~filtered_data['name'].str.contains('chicken|beef|pork|shrimp|bacon', case=False)]
    if "Vegan" in dietary_preferences:
        filtered_data = filtered_data[~filtered_data['name'].str.contains('chicken|beef|pork|shrimp|bacon|cheese|cream|milk|egg', case=False)]
    if "Gluten-Free" in dietary_preferences:
        filtered_data = filtered_data[~filtered_data['name'].str.contains('pasta|bread|flour|pancake|cookie|cake', case=False)]
    if "High-Protein" in health_goals:
        filtered_data = filtered_data.sort_values(by='protein', ascending=False)
    if "Low-Carb" in health_goals:
        filtered_data = filtered_data.sort_values(by='carbohydrates', ascending=True)
    
    if "Nuts" in allergies:
        filtered_data = filtered_data[~filtered_data['name'].str.contains('nut|peanut|almond', case=False)]
    if "Dairy" in allergies:
        filtered_data = filtered_data[~filtered_data['name'].str.contains('cheese|cream|milk|butter|parmesan|cheddar', case=False)]
    if "Eggs" in allergies:
        filtered_data = filtered_data[~filtered_data['name'].str.contains('egg', case=False)]
    
    st.write("Based on your profile, we recommend these foods:")
    for i, row in filtered_data.head(5).iterrows():
        with st.expander(f"🍴 {row['name']} - ⏱️{row['cook_time_minutes']} min - ⭐{row['user_ratings']:.2f}"):
            st.write(f"**Description:** {row['description']}")
            cols = st.columns(3)
            cols[0].metric("Calories", f"{row['calories']} kcal")
            cols[1].metric("Protein", f"{row['protein']}g")
            cols[2].metric("Carbs", f"{row['carbohydrates']}g")
    
    st.subheader("Nutrition Summary")
    
    bmi = weight / ((height/100) ** 2)
    bmi_status = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
    
    cols = st.columns(2)
    cols[0].metric("BMI", f"{bmi:.1f}", bmi_status)
    cols[1].metric("Target Calories", f"{target_calories} kcal")
    
    st.write("**Daily Macronutrient Targets**")
    fig, ax = plt.subplots()
    sizes = [target_protein*4, target_carbs*4, target_fat*9]
    labels = ['Protein', 'Carbs', 'Fat']
    colors = ['#ff9999','#66b3ff','#99ff99']
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
    
    water_intake = weight * 0.033  
    st.metric("Recommended Water Intake", f"{water_intake:.1f} liters per day")

with tab2: 
    st.subheader("Explore Our Food Database")
    
    search_query = st.text_input("Search for foods by name or ingredients")
    
    cols = st.columns(3)
    with cols[0]:
        min_calories = st.slider("Min Calories", 0, 2000, 0)
    with cols[1]:
        max_calories = st.slider("Max Calories", 0, 2000, 2000)
    with cols[2]:
        max_cook_time = st.slider("Max Cook Time (minutes)", 0, 120, 60)
    
    filtered_foods = data[
        (data['calories'] >= min_calories) & 
        (data['calories'] <= max_calories) & 
        (data['cook_time_minutes'] <= max_cook_time)
    ]
    
    if search_query:
        filtered_foods = filtered_foods[
            filtered_foods['name'].str.contains(search_query, case=False) | 
            filtered_foods['description'].str.contains(search_query, case=False)
        ]
    
    st.write(f"Found {len(filtered_foods)} foods matching your criteria")
    
    for i, row in filtered_foods.iterrows():
        with st.expander(f"🍽️ {row['name']} ({row['country']}) - ⏱️{row['cook_time_minutes']} min - ⭐{row['user_ratings']:.2f}"):
            st.write(f"**Description:** {row['description']}")
            
            cols = st.columns(4)
            cols[0].metric("Calories", f"{row['calories']} kcal")
            cols[1].metric("Protein", f"{row['protein']}g")
            cols[2].metric("Carbs", f"{row['carbohydrates']}g")
            cols[3].metric("Fat", f"{row['fat']}g")
            
            nutrients = {
                'Protein': row['protein'],
                'Carbs': row['carbohydrates'],
                'Fat': row['fat'],
                'Fiber': row['fiber'],
                'Sugar': row['sugar']
            }
            fig, ax = plt.subplots()
            ax.bar(nutrients.keys(), nutrients.values(), color=['blue', 'green', 'orange', 'purple', 'red'])
            plt.xticks(rotation=45)
            plt.ylabel('Grams')
            plt.title('Nutritional Content')
            st.pyplot(fig)

with tab3:  
    st.subheader("AI-Powered Meal Planner")
    
    cols = st.columns(2)
    with cols[0]:
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
    with cols[1]:
        time_available = st.slider("Time Available (minutes)", 5, 120, 30)
    
    if st.button("Generate Meal Plan"):
        suitable_foods = data[data['cook_time_minutes'] <= time_available]
        
        if meal_type == "Breakfast":
            suitable_foods = suitable_foods[suitable_foods['name'].str.contains('pancake|muffin|banana|oat', case=False)]
        elif meal_type == "Lunch":
            suitable_foods = suitable_foods[suitable_foods['name'].str.contains('salad|sandwich|soup|pasta', case=False)]
        elif meal_type == "Dinner":
            suitable_foods = suitable_foods[suitable_foods['name'].str.contains('pasta|chicken|beef|fish|stir-fry', case=False)]
        elif meal_type == "Snack":
            suitable_foods = suitable_foods[suitable_foods['name'].str.contains('cookie|cake|muffin|bite', case=False)]
        
        if "High-Protein" in health_goals:
            suitable_foods = suitable_foods.sort_values(by='protein', ascending=False)
        if "Low-Carb" in health_goals:
            suitable_foods = suitable_foods.sort_values(by='carbohydrates', ascending=True)
        
        if len(suitable_foods) > 0:
            st.success("Here are your personalized meal options:")
            options = suitable_foods.head(3)
            
            for i, row in options.iterrows():
                with st.expander(f"🍴 {row['name']} - ⏱️{row['cook_time_minutes']} min - ⭐{row['user_ratings']:.2f}"):
                    st.write(f"**Description:** {row['description']}")
                    
                    cols = st.columns(4)
                    cols[0].metric("Calories", f"{row['calories']} kcal")
                    cols[1].metric("Protein", f"{row['protein']}g")
                    cols[2].metric("Carbs", f"{row['carbohydrates']}g")
                    cols[3].metric("Fat", f"{row['fat']}g")
                    
                    st.write("**% of Daily Targets**")
                    cols = st.columns(4)
                    cols[0].metric("Calories", f"{row['calories']/target_calories*100:.1f}%")
                    cols[1].metric("Protein", f"{row['protein']/target_protein*100:.1f}%")
                    cols[2].metric("Carbs", f"{row['carbohydrates']/target_carbs*100:.1f}%")
                    cols[3].metric("Fat", f"{row['fat']/target_fat*100:.1f}%")
        else:
            st.warning("No meals found matching your criteria. Try adjusting your filters.")

with tab4: 
    st.subheader("Nutrition Analysis")
    
    selected_food = st.selectbox("Select a food to analyze", data['name'])
    
    food_data = data[data['name'] == selected_food].iloc[0]
    
    st.write(f"**Nutrition Facts for {selected_food}**")
    st.write(f"🍽️ **Description:** {food_data['description']}")
    st.write(f"⏱️ **Cook Time:** {food_data['cook_time_minutes']} minutes")
    st.write(f"⭐ **User Rating:** {food_data['user_ratings']:.2f}/1.0")
    
    cols = st.columns(2)
    
    with cols[0]:
        st.write("**Macronutrients**")
        st.metric("Calories", f"{food_data['calories']} kcal")
        st.metric("Protein", f"{food_data['protein']}g")
        st.metric("Carbohydrates", f"{food_data['carbohydrates']}g")
        st.metric("Fat", f"{food_data['fat']}g")
    
    with cols[1]:
       
        fig1, ax1 = plt.subplots()
        macronutrients = [food_data['protein'], food_data['carbohydrates'], food_data['fat']]
        labels = ['Protein', 'Carbs', 'Fat']
        colors = ['#ff9999','#66b3ff','#99ff99']
        ax1.pie(macronutrients, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)
        
        fig2, ax2 = plt.subplots()
        micronutrients = {
            'Fiber': food_data['fiber'],
            'Sugar': food_data['sugar']
        }
        ax2.bar(micronutrients.keys(), micronutrients.values(), color=['purple', 'red'])
        plt.ylabel('Grams')
        plt.title('Micronutrients')
        st.pyplot(fig2)
    
    st.subheader("Health Impact Analysis")
    
    if "Weight Loss" in health_goals:
        if food_data['calories'] > 500:
            st.warning("⚠️ This meal is high in calories for weight loss goals.")
        else:
            st.success("✅ This meal fits well with weight loss goals.")
    
    if "High-Protein" in health_goals:
        if food_data['protein'] > 20:
            st.success(f"✅ Excellent protein source ({food_data['protein']}g)")
        else:
            st.warning(f"⚠️ Moderate protein content ({food_data['protein']}g)")
    
    if "Low-Carb" in health_goals:
        if food_data['carbohydrates'] > 50:
            st.warning(f"⚠️ High carb content ({food_data['carbohydrates']}g)")
        else:
            st.success(f"✅ Low carb option ({food_data['carbohydrates']}g)")

with tab5: 
    st.subheader("Personalized Health Insights")
    
    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    activity_factors = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extremely Active": 1.9
    }
    tdee = bmr * activity_factors[activity_level]
    
    cols = st.columns(2)
    with cols[0]:
        st.metric("Basal Metabolic Rate (BMR)", f"{bmr:.0f} kcal/day")
        st.metric("Total Daily Energy Expenditure (TDEE)", f"{tdee:.0f} kcal/day")
        
        if "Weight Loss" in health_goals:
            st.info("For weight loss, aim for 300-500 kcal below your TDEE")
            recommended_intake = tdee - 500
            st.metric("Recommended Daily Intake", f"{recommended_intake:.0f} kcal")
        elif "Muscle Gain" in health_goals:
            st.info("For muscle gain, aim for 300-500 kcal above your TDEE")
            recommended_intake = tdee + 500
            st.metric("Recommended Daily Intake", f"{recommended_intake:.0f} kcal")
    
    with cols[1]:
        st.write("**Recommended Macronutrient Distribution**")
        
        if "Weight Loss" in health_goals:
            st.write("- Protein: 30-35% of calories")
            st.write("- Carbs: 30-40% of calories")
            st.write("- Fat: 25-35% of calories")
        elif "Muscle Gain" in health_goals:
            st.write("- Protein: 25-35% of calories")
            st.write("- Carbs: 40-50% of calories")
            st.write("- Fat: 15-25% of calories")
        else:  
            st.write("- Protein: 20-30% of calories")
            st.write("- Carbs: 45-55% of calories")
            st.write("- Fat: 20-35% of calories")
    
    st.divider()
    st.subheader("Nutrition Tips Based on Your Profile")
    
    if "Weight Loss" in health_goals:
        st.write("""
        - Focus on high-protein, high-fiber foods to stay full longer
        - Reduce added sugars and refined carbohydrates
        - Drink plenty of water before meals to reduce appetite
        - Incorporate healthy fats in moderation
        """)
    
    if "Muscle Gain" in health_goals:
        st.write("""
        - Consume protein with every meal (aim for 1.6-2.2g per kg of body weight)
        - Time carbohydrates around workouts for energy and recovery
        - Don't neglect healthy fats for hormone production
        - Consider protein-rich snacks between meals
        """)
    
    if "Heart Health" in health_goals:
        st.write("""
        - Increase intake of omega-3 fatty acids (fish, flaxseeds, walnuts)
        - Choose unsaturated fats over saturated fats
        - Eat plenty of fruits and vegetables for antioxidants
        - Reduce sodium intake to support healthy blood pressure
        """)
    
    if "Diabetes Management" in health_goals:
        st.write("""
        - Focus on low-glycemic index carbohydrates
        - Pair carbs with protein and fat to slow digestion
        - Choose high-fiber foods to help regulate blood sugar
        - Spread carbohydrate intake evenly throughout the day
        """)

st.divider()
st.write("""
The Smartest AI Nutrition Assistant provides general nutrition information and should not be considered 
medical advice. Always consult with a healthcare professional before making significant dietary changes.
""")