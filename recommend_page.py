import streamlit as st
import pickle
import numpy as np
from scrape_and_model import similar_cocktail, cocktail_df


def show_recommend_page():
    st.title("Cocktail Recommendation")

    st.write("""#### Pick a cocktail that you like and we will recommend a similar one!""")

    cocktail_names = (
        '155 belmont', '1900fukmeup', '110 in the shade',
       '151 florida bushwacker', '252', '24k nightmare', '3 wise men',
       '3mile long island iced tea', '410 gone', '5050', '501 blue',
       '57 chevy with a white license plate', '69 special', '747',
       '747 drink', '9 12 weeks', 'a1', 'abc', 'ace', 'acid', 'adam',
       'att', 'a j', 'avalon', 'apello', 'affair', 'abilene', 'almeria',
       'addison', 'applecar', 'acapulco', 'affinity', 'aviation',
       'after sex', 'applejack', 'afterglow', 'afternoon', 'alexander',
       'autodafé', 'allegheny', 'americano', 'b52', 'b53', 'bijou',
       'boxcar', 'big red', 'bellini', 'bramble', 'balmoral', 'bluebird',
       'brooklyn', 'bora bora', 'boomerang', 'barracuda', 'brigadier',
       'broadside', 'buccaneer', 'brain fart', 'blackthorn', 'bob marley',
       'bible belt', 'bubble gum', 'bumble bee', 'baby eskimo',
       'boston sour', 'bahama mama', 'casino', 'cafe savoy', 'caipirinha',
       'cream soda', 'cuba libra', 'cherry rum', 'cuba libre',
       'corn n oil', 'citrus coke', 'casa blanca', 'clover club',
       'caipirissima', 'city slicker', 'campari beer', 'chicago fizz',
       'cosmopolitan', 'coffeevodka', 'casino royale', 'corpse reviver',
       'chocolate milk', 'clove cocktail', 'coffee liqueur',
       'coke and drops', 'chocolate drink', 'cranberry punch', 'derby',
       'diesel', 'daiquiri', 'danbooka', 'downshift', 'dragonfly',
       'dry martini', 'dry rob roy', 'dirty nipple', 'dirty martini',
       'darkwood sling', 'dark and stormy', 'dark caipirinha',
       'duchamps punch', 'damned if you do', 'dubonnet cocktail',
       'drinking chocolate', 'death in the afternoon', 'egg cream',
       'egg nog 4', 'english highball', 'espresso martini',
       'espresso rumtini', 'egg nog  healthy', 'english rose cocktail',
       'elderflower caipirinha', 'eggnog  classic cooked',
       'empellón cocinas fatwashed mezcal', 'frosé', 'frappé',
       'foxy lady', 'french 75', 'figgy thyme', 'frisco sour',
       'fruit shake', 'fruit cooler', 'freddy kruger', 'funk and soul',
       'fuzzy asshole', 'french martini', 'french negroni',
       'fahrenheit 5000', 'flying dutchman', 'frozen daiquiri',
       'fruit flipflop', 'flying scotchman', 'french connection',
       'flaming dr pepper', 'flaming lamborghini', 'flanders flakeout',
       'frozen mint daiquiri', 'frozen pineapple daiquiri', 'gg',
       'gimlet', 'godchild', 'gin fizz', 'gin sour', 'gagliardo',
       'godmother', 'godfather', 'gluehwein', 'gin tonic', 'gin toddy',
       'gin smash', 'gin daisy', 'gin lemon', 'gin sling', 'greyhound',
       'gin rickey', 'gin squirt', 'grand blue', 'gin cooler',
       'gin swizzle', 'grass skirt', 'grasshopper', 'grim reaper',
       'gin and soda', 'hd', 'honey bee', 'hot toddy', 'herbal flame',
       'horses neck', 'happy skipper', 'hunters moon', 'halloween punch',
       'havana cocktail', 'holloween punch', 'homemade kahlua',
       'hot creamy bush', 'harvey wallbanger', 'hawaiian cocktail',
       'hemingway special', 'highland fling cocktail',
       'hot chocolate to die for', 'ipamena', 'ice pick', 'iced coffee',
       'irish cream', 'irish coffee', 'irish spring', 'imperial fizz',
       'irish russian', 'imperial cocktail', 'iced coffee fillip',
       'irish curdling cow', 'jam donut', 'jitterbug', 'jackhammer',
       'jelly bean', 'jello shots', 'jamaica kiss', 'john collins',
       'japanese fizz', 'jamaican coffee', 'just a moonmint',
       'jewel of the nile', 'jack rose cocktail', 'jacks vanilla coke',
       'kir', 'karsk', 'kamikaze', 'kir royale', 'kiwi lemon',
       'kurant tea', 'kioki coffee', 'kiwi martini', 'kiss me quick',
       'koolaid shot', 'kool first aid', 'kentucky b and b',
       'kentucky colonel', 'koolaid slammer', 'kiwi papaya smoothie',
       'kill the cold smoothie', 'limeade', 'lunch box', 'lemon drop',
       'lemon shot', 'long vodka', 'lassi khara', 'lassi raita',
       'lemouroudji', 'loch lomond', 'london town', 'lassi  mango',
       'lassi  sweet', 'limona corona', 'lord and lady', 'lady love fizz',
       'long island tea', 'lone tree cooler', 'lone tree cocktail',
       'lazy coconut paloma', 'long island iced tea',
       'lemon elderflower spritzer', 'lassi  a south indian drink',
       'melya', 'mojito', 'mimosa', 'mai tai', 'martini', 'michelada',
       'manhattan', 'margarita', 'mauresque', 'mint julep', 'mudslinger',
       'martinez 2', 'moranguito', 'miami vice', 'moscow mule',
       'mulled wine', 'masala chai', 'munich mule', 'mochaberry',
       'mango mojito', 'mojito extra', 'monkey gland', 'midnight mint',
       'mary pickford', 'monkey wrench', 'negroni', 'new york sour',
       'nutty irishman', 'national aquarium', 'new york lemonade',
       'nuked hot chocolate', 'orgasm', 'old pal', 'orangeade',
       'orange whip', 'orange crush', 'orange oasis', 'old fashioned',
       'oreo mudslide', 'oatmeal cookie', 'orange pushup',
       'orange rosemary collins', 'orange scented hot chocolate',
       'owens grandmothers revenge', 'paloma', 'paradise', 'pink gin',
       'pegu club', 'pink lady', 'pink moon', 'penicillin', 'pisco sour',
       'porto flip', 'pina colada', 'pink penocha', 'pure passion',
       'popped cherry', 'poppy cocktail', 'port wine flip',
       'planters punch', 'pineapple paloma', 'pornstar martini',
       'port and starboard', 'port wine cocktail', 'pysch vitamin light',
       'pink panty pulldowns', 'passion fruit martini',
       'pineapple gingerale smoothie', 'quentin', 'queen bee', 'quick fk',
       'quicksand', 'queen charlotte', 'queen elizabeth',
       'quakers cocktail', 'quarter deck cocktail', 'rose', 'radler',
       'rum sour', 'rum punch', 'rum toddy', 'royal fizz', 'rum cooler',
       'rum runner', 'rusty nail', 'red snapper', 'royal bitch',
       'royal flush', 'rum cobbler', 'ruby tuesday', 'rail splitter',
       'rosemary blue', 'ramos gin fizz', 'royal gin fizz',
       'rum milk punch', 'raspberry julep', 'rum screwdriver',
       'raspberry cooler', 'rum oldfashioned', 'russian spring punch',
       'radioactive long island iced tea', 'smut', 'spritz', 'scooter',
       'sangria', 'stinger', 'sazerac', 'sidecar', 'snowday', 'spice 75',
       'snowball', 'shotgun', 'salty dog', 'stone sour', 'sea breeze',
       'scotch sour', 'sweet tooth', 'screwdriver', 'sherry flip',
       'sol y sombra', 'shark attack', 'san francisco', 'space odyssey',
       'sherry eggnog', 'sweet bananas', 'sweet sangria', 'thriller',
       'the galah', 'tiamaria', 'tipperary', 'turkeyball', 'texas sling',
       'thai coffee', 'tom collins', 'tomato tang', 'talos coffee',
       'tennesee mud', 'tequila fizz', 'tequila sour', 'thai iced tea',
       'the last word', 'turf cocktail', 'the laverstoke',
       'tequila slammer', 'tequila sunrise', 'the philosopher',
       'tuxedo cocktail', 'tequila surprise', 'thai iced coffee',
       'the jimmy conway', 'texas rattlesnake', 'vesper', 'victor',
       'vampiro', 'vesuvio', 'veteran', 'van vleet', 'vodka fizz',
       'vodka lemon', 'vodka slime', 'vodka tonic', 'vodka martini',
       'vodka russian', 'vermouth cassis', 'victory collins',
       'vodka and tonic', 'valencia cocktail', 'whisky mac', 'white lady',
       'wine punch', 'wine cooler', 'winter rita', 'whiskey sour',
       'white russian', 'winter paloma', 'white wine sangria',
       'whitecap margarita', 'waikiki beachcomber', 'yellow bird',
       'yoghurt cooler', 'zorro', 'zinger', 'zoksel', 'zombie', 'zambeer',
       'zorbatini', 'zenmeister', 'zipperhead', 'zima blaster',
       'zizi coincoin', 'zimadori zinger', 'zippys revenge',
       'ziemes martini apfelsaft'
    )


    cocktail = st.selectbox("Cocktail:", cocktail_names)

    button_clicked = st.button("Recommend Cocktail")
    if button_clicked:
        new_cocktail = similar_cocktail(cocktail_df, cocktail)
        st.subheader(f"You might like the cocktail: {new_cocktail}")

