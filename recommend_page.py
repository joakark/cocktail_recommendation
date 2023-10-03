import streamlit as st
from scrape_and_model import similar_cocktail, cocktail_df


def show_recommend_page():
    st.title("Cocktail Recommendation")

    st.write("""#### Pick a cocktail that you like and we will recommend a similar one!""")

    cocktail_names = cocktail_df.drink.unique()

    chosen_cocktail = st.selectbox("**Cocktail**:", cocktail_names)
    chosen_cocktail_ingredients_and_quantities = cocktail_df[cocktail_df.drink == chosen_cocktail].ingredients_and_quantities.values

    st.write(f"The **{chosen_cocktail}** cocktail has the following ingredients:")
    for ingredient in chosen_cocktail_ingredients_and_quantities[0].rstrip().rstrip(",").split(","):
        st.write(f"- {ingredient}")


    button_clicked = st.button("Recommend Cocktail")
    if button_clicked:
        new_cocktail = similar_cocktail(cocktail_df, chosen_cocktail)
        st.subheader(f"You might like the cocktail: {new_cocktail}")

        new_cocktail_ingredients_and_quantities = cocktail_df[cocktail_df.drink == new_cocktail].ingredients_and_quantities.values
        new_cocktail_instructions = cocktail_df[cocktail_df.drink == new_cocktail].instructions.values

        st.write(f"**Ingredients:**")
        for ingredient in new_cocktail_ingredients_and_quantities[0].rstrip().rstrip(",").split(","):
            st.write(f"- {ingredient}")

        st.write(f"**Instructions**:")
        st.write(new_cocktail_instructions[0])


