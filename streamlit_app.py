import streamlit as st

# Initialize recipes list (in-memory)
if 'recipes' not in st.session_state:
    st.session_state.recipes = []

# Initialize saved recipes
if 'saved_recipes' not in st.session_state:
    st.session_state.saved_recipes = []

def add_recipe(title, ingredients, instructions, language):
    recipe = {
        'title': title,
        'ingredients': ingredients,
        'instructions': instructions,
        'language': language,
        'upvotes': 0,
        'id': len(st.session_state.recipes) + 1
    }
    st.session_state.recipes.append(recipe)

def suggest_alternatives(ingredients):
    # Placeholder for AI ingredient suggestions
    return "AI suggestions coming soon!"

def upvote_recipe(recipe_id):
    for recipe in st.session_state.recipes:
        if recipe['id'] == recipe_id:
            recipe['upvotes'] += 1
            break

def save_recipe(recipe_id):
    for recipe in st.session_state.recipes:
        if recipe['id'] == recipe_id and recipe not in st.session_state.saved_recipes:
            st.session_state.saved_recipes.append(recipe)
            break

def unsave_recipe(recipe_id):
    st.session_state.saved_recipes = [recipe for recipe in st.session_state.saved_recipes if recipe['id'] != recipe_id]

# Streamlit App
st.title("Indian Recipe Exchange")

# Recipe Submission Form
with st.expander("Submit Your Recipe"):
    with st.form("recipe_form"):
        title = st.text_input("Recipe Title")
        ingredients = st.text_area("Ingredients (separate by commas)")
        instructions = st.text_area("Instructions")
        language = st.text_input("Language")
        submitted = st.form_submit_button("Submit")

        if submitted:
            add_recipe(title, ingredients, instructions, language)
            st.success("Recipe submitted!")

# Recipe Display
st.header("Recipes")

# Category Filter (Language)
languages = ['All'] + list(set([recipe['language'] for recipe in st.session_state.recipes]))
selected_language = st.selectbox("Select Language", languages)

# Display Recipes
filtered_recipes = st.session_state.recipes if selected_language == 'All' else [recipe for recipe in st.session_state.recipes if recipe['language'] == selected_language]

if not filtered_recipes:
    st.write("No recipes found for the selected language.")
else:
    for recipe in filtered_recipes:
        st.subheader(recipe['title'])
        st.write(f"Language: {recipe['language']}")
        st.write(f"Ingredients: {recipe['ingredients']}")
        st.write(f"Instructions: {recipe['instructions']}")
        st.write(f"Upvotes: {recipe['upvotes']}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"Upvote", key=f"upvote_{recipe['id']}"):
                upvote_recipe(recipe['id'])
                st.rerun()
        with col2:
            if recipe in st.session_state.saved_recipes:
                if st.button("Unsave", key=f"unsave_{recipe['id']}"):
                    unsave_recipe(recipe['id'])
                    st.rerun()
            else:
                if st.button("Save", key=f"save_{recipe['id']}"):
                    save_recipe(recipe['id'])
                    st.rerun()
        with col3:
            if st.button("Suggest Alternatives", key=f"suggest_{recipe['id']}"):
                alternatives = suggest_alternatives(recipe['ingredients'])
                st.write(alternatives)

# Saved Recipes
st.header("Saved Recipes")
if not st.session_state.saved_recipes:
    st.write("No recipes saved yet.")
else:
    for recipe in st.session_state.saved_recipes:
        st.subheader(recipe['title'])
        st.write(f"Language: {recipe['language']}")
        st.write(f"Ingredients: {recipe['ingredients']}")
        st.write(f"Instructions: {recipe['instructions']}")
        st.write(f"Upvotes: {recipe['upvotes']}")
        if st.button("Unsave", key=f"unsave_saved_{recipe['id']}"):
            unsave_recipe(recipe['id'])
            st.rerun()
