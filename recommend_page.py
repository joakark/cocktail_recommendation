import streamlit as st
import pickle
import numpy as np
from scrape_and_model import similar_cocktail, cocktail_df


def show_recommend_page():
    st.title("Cocktail Recommendation")

    st.write("""#### Pick a cocktail that you like and we will recommend a similar one!""")

    cocktail_names = (
        '155 Belmont', '1-900-FUK-MEUP', '110 in the shade',
       '151 Florida Bushwacker', '252', '24k nightmare', '3 Wise Men',
       '3-Mile Long Island Iced Tea', '410 Gone', '50/50', '501 Blue',
       '57 Chevy with a White License Plate', '69 Special', '747',
       '747 Drink', '9 1/2 Weeks', 'A1', 'ABC', 'Ace', 'ACID', 'Adam',
       'AT&T', 'A. J.', 'Avalon', 'Apello', 'Affair', 'Abilene',
       'Almeria', 'Addison', 'Applecar', 'Acapulco', 'Affinity',
       'Aviation', 'After sex', 'Applejack', 'Afterglow', 'Afternoon',
       'Alexander', 'Autodafé', 'Allegheny', 'Americano', 'B-52', 'B-53',
       'Bijou', 'Boxcar', 'Big Red', 'Bellini', 'Bramble', 'Balmoral',
       'Bluebird', 'Brooklyn', 'Bora Bora', 'Boomerang', 'Barracuda',
       'Brigadier', 'Broadside', 'Buccaneer', 'Brain Fart', 'Blackthorn',
       'Bob Marley', 'Bible Belt', 'Bubble Gum', 'Bumble Bee',
       'Baby Eskimo', 'Boston Sour', 'Bahama Mama', 'Casino',
       'Cafe Savoy', 'Caipirinha', 'Cream Soda', 'Cuba Libra',
       'Cherry Rum', 'Cuba Libre', 'Corn n Oil', 'Citrus Coke',
       'Casa Blanca', 'Clover Club', 'Caipirissima', 'City Slicker',
       'Campari Beer', 'Chicago Fizz', 'Cosmopolitan', 'Coffee-Vodka',
       'Casino Royale', 'Corpse Reviver', 'Chocolate Milk',
       'Clove Cocktail', 'Coffee Liqueur', 'Coke and Drops',
       'Chocolate Drink', 'Cranberry Punch', 'Derby', 'Diesel',
       'Daiquiri', 'Danbooka', 'Downshift', 'Dragonfly', 'Dry Martini',
       'Dry Rob Roy', 'Dirty Nipple', 'Dirty Martini', 'Darkwood Sling',
       'Dark and Stormy', 'Dark Caipirinha', "Duchamp's Punch",
       'Damned if you do', 'Dubonnet Cocktail', 'Drinking Chocolate',
       'Death in the Afternoon', 'Egg Cream', 'Egg Nog #4',
       'English Highball', 'Espresso Martini', 'Espresso Rumtini',
       'Egg Nog - Healthy', 'English Rose Cocktail',
       'Elderflower Caipirinha', 'Egg-Nog - Classic Cooked',
       "Empellón Cocina's Fat-Washed Mezcal", 'Frosé', 'Frappé',
       'Foxy Lady', 'French 75', 'Figgy Thyme', 'Frisco Sour',
       'Fruit Shake', 'Fruit Cooler', 'Freddy Kruger', 'Funk and Soul',
       'Fuzzy Asshole', 'French Martini', 'French Negroni',
       'Fahrenheit 5000', 'Flying Dutchman', 'Frozen Daiquiri',
       'Fruit Flip-Flop', 'Flying Scotchman', 'French Connection',
       'Flaming Dr. Pepper', 'Flaming Lamborghini', "Flander's Flake-Out",
       'Frozen Mint Daiquiri', 'Frozen Pineapple Daiquiri', 'GG',
       'Gimlet', 'Godchild', 'Gin Fizz', 'Gin Sour', 'Gagliardo',
       'Godmother', 'Godfather', 'Gluehwein', 'Gin Tonic', 'Gin Toddy',
       'Gin Smash', 'Gin Daisy', 'Gin Lemon', 'Gin Sling', 'Greyhound',
       'Gin Rickey', 'Gin Squirt', 'Grand Blue', 'Gin Cooler',
       'Gin Swizzle', 'Grass Skirt', 'Grasshopper', 'Grim Reaper',
       'Gin and Soda', 'H.D.', 'Honey Bee', 'Hot Toddy', 'Herbal flame',
       "Horse's Neck", 'Happy Skipper', "Hunter's Moon",
       'Halloween Punch', 'Havana Cocktail', 'Holloween Punch',
       'Homemade Kahlua', 'Hot Creamy Bush', 'Harvey Wallbanger',
       'Hawaiian Cocktail', 'Hemingway Special',
       'Highland Fling Cocktail', 'Hot Chocolate to Die for', 'Ipamena',
       'Ice Pick', 'Iced Coffee', 'Irish Cream', 'Irish Coffee',
       'Irish Spring', 'Imperial Fizz', 'Irish Russian',
       'Imperial Cocktail', 'Iced Coffee Fillip', 'Irish Curdling Cow',
       'Jam Donut', 'Jitterbug', 'Jackhammer', 'Jelly Bean',
       'Jello shots', 'Jamaica Kiss', 'John Collins', 'Japanese Fizz',
       'Jamaican Coffee', 'Just a Moonmint', 'Jewel Of The Nile',
       'Jack Rose Cocktail', "Jack's Vanilla Coke", 'Kir', 'Karsk',
       'Kamikaze', 'Kir Royale', 'Kiwi Lemon', 'Kurant Tea',
       'Kioki Coffee', 'Kiwi Martini', 'Kiss me Quick', 'Kool-Aid Shot',
       'Kool First Aid', 'Kentucky B And B', 'Kentucky Colonel',
       'Kool-Aid Slammer', 'Kiwi Papaya Smoothie',
       'Kill the cold Smoothie', 'Limeade', 'Lunch Box', 'Lemon Drop',
       'Lemon Shot', 'Long vodka', 'Lassi Khara', 'Lassi Raita',
       'Lemouroudji', 'Loch Lomond', 'London Town', 'Lassi - Mango',
       'Lassi - Sweet', 'Limona Corona', 'Lord And Lady',
       'Lady Love Fizz', 'Long Island Tea', 'Lone Tree Cooler',
       'Lone Tree Cocktail', 'Lazy Coconut Paloma',
       'Long Island Iced Tea', 'Lemon Elderflower Spritzer',
       'Lassi - A South Indian Drink', 'Melya', 'Mojito', 'Mimosa',
       'Mai Tai', 'Martini', 'Michelada', 'Manhattan', 'Margarita',
       'Mauresque', 'Mint Julep', 'Mudslinger', 'Martinez 2',
       'Moranguito', 'Miami Vice', 'Moscow Mule', 'Mulled Wine',
       'Masala Chai', 'Munich Mule', 'Mocha-Berry', 'Mango Mojito',
       'Mojito Extra', 'Monkey Gland', 'Midnight Mint', 'Mary Pickford',
       'Monkey Wrench', 'Negroni', 'New York Sour', 'Nutty Irishman',
       'National Aquarium', 'New York Lemonade', 'Nuked Hot Chocolate',
       'Orgasm', 'Old Pal', 'Orangeade', 'Orange Whip', 'Orange Crush',
       'Orange Oasis', 'Old Fashioned', 'Oreo Mudslide', 'Oatmeal Cookie',
       'Orange Push-up', 'Orange Rosemary Collins',
       'Orange Scented Hot Chocolate', "Owen's Grandmother's Revenge",
       'Paloma', 'Paradise', 'Pink Gin', 'Pegu Club', 'Pink Lady',
       'Pink Moon', 'Penicillin', 'Pisco Sour', 'Porto flip',
       'Pina Colada', 'Pink Penocha', 'Pure Passion', 'Popped cherry',
       'Poppy Cocktail', 'Port Wine Flip', "Planter's Punch",
       'Pineapple Paloma', 'Pornstar Martini', 'Planter’s Punch',
       'Port And Starboard', 'Port Wine Cocktail', 'Pysch Vitamin Light',
       'Pink Panty Pulldowns', 'Passion Fruit Martini',
       'Pineapple Gingerale Smoothie', 'Quentin', 'Queen Bee',
       'Quick F**K', 'Quick-sand', 'Queen Charlotte', 'Queen Elizabeth',
       "Quaker's Cocktail", 'Quarter Deck Cocktail', 'Rose', 'Radler',
       'Rum Sour', 'Rum Punch', 'Rum Toddy', 'Royal Fizz', 'Rum Cooler',
       'Rum Runner', 'Rusty Nail', 'Red Snapper', 'Royal Bitch',
       'Royal Flush', 'Rum Cobbler', 'Ruby Tuesday', 'Rail Splitter',
       'Rosemary Blue', 'Ramos Gin Fizz', 'Royal Gin Fizz',
       'Rum Milk Punch', 'Raspberry Julep', 'Rum Screwdriver',
       'Raspberry Cooler', 'Rum Old-fashioned', 'Russian Spring Punch',
       'Radioactive Long Island Iced Tea', 'Smut', 'Spritz', 'Scooter',
       'Sangria', 'Stinger', 'Sazerac', 'Sidecar', 'Snowday', 'Spice 75',
       'Snowball', 'Shot-gun', 'Salty Dog', 'Stone Sour', 'Sea breeze',
       'Scotch Sour', 'Sweet Tooth', 'Screwdriver', 'Sherry Flip',
       'Sol Y Sombra', 'Shark Attack', 'San Francisco', 'Space Odyssey',
       'Sherry Eggnog', 'Sweet Bananas', 'Sweet Sangria', 'Thriller',
       'The Galah', 'Tia-Maria', 'Tipperary', 'Turkeyball', 'Texas Sling',
       'Thai Coffee', 'Tom Collins', 'Tomato Tang', 'Talos Coffee',
       'Tennesee Mud', 'Tequila Fizz', 'Tequila Sour', 'Thai Iced Tea',
       'The Last Word', 'Turf Cocktail', 'The Laverstoke',
       'Tequila Slammer', 'Tequila Sunrise', 'The Philosopher',
       'Tuxedo Cocktail', 'Tequila Surprise', 'Thai Iced Coffee',
       'The Jimmy Conway', 'Texas Rattlesnake', 'Vesper', 'Victor',
       'Vampiro', 'Vesuvio', 'Veteran', 'Van Vleet', 'Vodka Fizz',
       'Vodka Lemon', 'Vodka Slime', 'Vodka Tonic', 'Vodka Martini',
       'Vodka Russian', 'Vermouth Cassis', 'Victory Collins',
       'Vodka And Tonic', 'Valencia Cocktail', 'Whisky Mac', 'White Lady',
       'Wine Punch', 'Wine Cooler', 'Winter Rita', 'Whiskey Sour',
       'White Russian', 'Winter Paloma', 'White Wine Sangria',
       'Whitecap Margarita', 'Waikiki Beachcomber', 'Yellow Bird',
       'Yoghurt Cooler', 'Zorro', 'Zinger', 'Zoksel', 'Zombie', 'Zambeer',
       'Zorbatini', 'Zenmeister', 'Zipperhead', 'Zima Blaster',
       'Zizi Coin-coin', 'Zimadori Zinger', "Zippy's Revenge",
       'Ziemes Martini Apfelsaft'
    )


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


