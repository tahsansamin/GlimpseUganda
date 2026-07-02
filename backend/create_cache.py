
import hashlib

import redis

import os
from dotenv import load_dotenv,find_dotenv




import time


import json



load_dotenv(find_dotenv())

redis_client = redis.from_url(os.getenv("REDIS_URL"))


name_spaces = ["kampala","entebbe","jinja","murchison_falls_national_park","bwindi_forest","mbarara","queen_elizabeth_national_park","gulu","kidepo_national_park","kibale_national_park","rwenzori_mountains","lake_bunyonyi","sipi_falls","lake_mburo_national_park","kabale"]
def create_cache(prompt:str,namespace:str):
    #creating unique key for caching
    raw_key = f"{namespace}:{prompt.strip().lower()}"
    return hashlib.md5(raw_key.encode()).hexdigest()

# redis_client.ping()
common_prompts = ["What's the best time to visit?", "Top things to do here?","Local food recommendations?","Weather forecast?"]

tourism_knowledge = {
    "kampala": {
        "What's the best time to visit?": {
            "answer": "The dry months from December to February and June to August offer the most comfortable weather for exploring. You'll avoid heavy downpours, making it much easier to navigate the city's busy streets and open-air markets."
        },
        "Top things to do here?": {
            "answer": "Immerse yourself in history at the Uganda Museum and Kasubi Tombs, or take in panoramic city views from the Gaddafi National Mosque tower. Don't miss the beautiful Bahá'í Temple and the vibrant, chaotic energy of Owino Market."
        },
        "Local food recommendations?": {
            "answer": "You absolutely have to try a 'Rolex' (a popular street food consisting of a rolled chapati with eggs and veggies) and traditional matoke with rich luwombo stew. For a casual evening out, head over to local spots for grilled tilapia or sizzling nyama choma."
        },
        "Weather forecast?": {
            "answer": "Kampala enjoys a warm, tropical climate with temperatures usually hovering comfortably between 18°C and 28°C. While it features pleasant, sunny days year-round, brief afternoon downpours are common during the rainy seasons."
        },
    },

    "entebbe": {
        "What's the best time to visit?": {
            "answer": "Plan your trip during the dry spans of June to August or December to February for ideal lakeside weather. These months offer clear skies and refreshing breezes perfect for boat cruises and outdoor walks."
        },
        "Top things to do here?": {
            "answer": "Get close to rescued wildlife at the Uganda Wildlife Education Centre and take a tranquil walk through the historic Entebbe Botanical Gardens. You can also catch a boat to the Ngamba Island Chimpanzee Sanctuary or unwind on Lake Victoria's sandy beaches."
        },
        "Local food recommendations?": {
            "answer": "The ultimate Entebbe experience is enjoying fresh, crispy-fried Nile perch or whole grilled tilapia right along the lakeside beaches. Pair your fish with a side of local chips or a freshly rolled street Rolex."
        },
        "Weather forecast?": {
            "answer": "Entebbe stays pleasantly warm with strong breezes coming off Lake Victoria that keep temperatures around 20°C to 27°C. Humidity is generally higher here due to the lake, bringing frequent morning showers."
        },
    },

    "jinja": {
        "What's the best time to visit?": {
            "answer": "June to August and December to February are the premier months for adventure seekers. The dry weather ensures optimal water conditions and keeps trails clear for land-based activities."
        },
        "Top things to do here?": {
            "answer": "Take a scenic boat cruise to discover the legendary Source of the Nile where the river begins its long journey north. For big thrills, Jinja is world-famous for white-water rafting, bungee jumping, quad biking, and kayaking."
        },
        "Local food recommendations?": {
            "answer": "Savor freshly caught tilapia from the Nile, or grab a classic street-side Rolex while exploring the town. The local chapatis here are exceptionally flaky and make a perfect quick snack between adventures."
        },
        "Weather forecast?": {
            "answer": "Jinja maintains an ideal outdoor climate with average daytime temperatures sitting around 26°C to 28°C. The proximity to the Nile and Lake Victoria means you can expect refreshing evening breezes and sudden, cooling showers."
        },
    },

    "murchison_falls_national_park": {
        "What's the best time to visit?": {
            "answer": "December to February and June to September are prime times because animals congregate around remaining water sources. Vegetation is also thinner during these dry months, making wildlife much easier to spot."
        },
        "Top things to do here?": {
            "answer": "Embark on classic savannah game drives to spot elephants, lions, and giraffes before taking a boat safari to the base of the explosive falls. For an unforgettable view, hike up to the top of the falls to feel the ground vibrate from the sheer force of the Nile."
        },
        "Local food recommendations?": {
            "answer": "Safari lodges inside the park serve excellent multi-course meals blending international flavors with Ugandan staples. Be sure to try matoke served with savory peanut or groundnut sauce during your stay."
        },
        "Weather forecast?": {
            "answer": "This is one of the warmer regions in Uganda, with daytime temperatures frequently reaching 30°C or higher. It stays hot and relatively dry, though heavy downpours can reshape safari tracks during April and May."
        },
    },

    "bwindi_forest": {
        "What's the best time to visit?": {
            "answer": "June to August and December to February are by far the best months for gorilla trekking. The forest trails are significantly less muddy, making the steep mountain hikes much safer and more manageable."
        },
        "Top things to do here?": {
            "answer": "The absolute highlight is mountain gorilla trekking, an intimate encounter with these gentle giants in their natural habitat. You can also explore lush nature trails for world-class bird watching and participate in cultural walks with the indigenous Batwa community."
        },
        "Local food recommendations?": {
            "answer": "Fuel up after a long trek with hearty, comforting Ugandan meals like steaming matoke, fresh mountain beans, and locally grown vegetables. Most eco-lodges also serve fantastic locally sourced organic coffee to kickstart your mornings."
        },
        "Weather forecast?": {
            "answer": "Bwindi features a cool, misty rainforest climate where temperatures range from 15°C to 25°C. Because it is a dense rainforest, weather is highly unpredictable and light showers can happen at any time, even during the dry season."
        },
    },

    "mbarara": {
        "What's the best time to visit?": {
            "answer": "The driest months from June to August and December to February provide the smoothest travel conditions. The roads are clear, making it a pleasant stopover on your way to western Uganda's safari circuits."
        },
        "Top things to do here?": {
            "answer": "Explore the Igongo Cultural Centre and the Ankole Museum to dive deep into the fascinating history of the region's ancient kingdoms. It also serves as the perfect launchpad for day trips into Lake Mburo National Park."
        },
        "Local food recommendations?": {
            "answer": "You must try traditional eshabwe (a rich, savory ghee sauce) paired with millet bread and tender Ankole long-horn beef. Don't leave without tasting the exceptionally fresh, rich dairy products the region is famous for."
        },
        "Weather forecast?": {
            "answer": "Mbarara enjoys a highly consistent and pleasant climate, staying warm during the day around 26°C and cooling off beautifully at night. It sees less intense rainfall than the lake regions, making it a very comfortable travel hub."
        },
    },

    "queen_elizabeth_national_park": {
        "What's the best time to visit?": {
            "answer": "The dry windows of June to August and December to February are perfect for game viewing as animals gather near water. Tracks are also dry and firm, preventing safari vehicles from getting stuck."
        },
        "Top things to do here?": {
            "answer": "Take an unforgettable boat cruise along the Kazinga Channel to see massive pods of hippos and elephants lining the shore. Afterward, head south to the Ishasha sector to track the park's legendary tree-climbing lions."
        },
        "Local food recommendations?": {
            "answer": "Indulge in freshly caught tilapia and Nile perch sourced directly from Lakes George and Edward, expertly prepared by safari chefs. Most lodges compliment these meals with a mix of fresh local produce and international cuisine."
        },
        "Weather forecast?": {
            "answer": "Located right on the equator, the park experiences warm daytime temperatures averaging 28°C. Evening temperatures drop comfortably, but you should prepare for humid conditions and sudden downpours if visiting between March and May."
        },
    },

    "gulu": {
        "What's the best time to visit?": {
            "answer": "December to February is the absolute best window, bringing dry, pleasant weather that is perfect for outdoor exploring. Traveling during these months avoids the heavy northern mud of the wet season."
        },
        "Top things to do here?": {
            "answer": "Visit the historic ruins of Fort Patiko to learn about the region's complex 19th-century history. Afterward, explore Gulu's bustling local markets and community centers to immerse yourself in rich Acholi cultural heritage."
        },
        "Local food recommendations?": {
            "answer": "Taste authentic northern flavors by ordering boo or malakwang, delicious local leafy greens cooked in a rich, savory peanut and sesame paste. Pair these stews with traditional millet bread and smoky grilled goat."
        },
        "Weather forecast?": {
            "answer": "Gulu is noticeably warmer and drier than southern Uganda, with daytime temperatures regularly climbing to around 30°C. The dry season brings plenty of sunshine, while the wet season features dramatic, rolling thunderstorms."
        },
    },

    "kidepo_national_park": {
        "What's the best time to visit?": {
            "answer": "September to March is the ideal window for wildlife viewing as the landscape dries out. Animals are forced to gather around the permanent Narus Valley wetlands, guaranteeing spectacular sightings."
        },
        "Top things to do here?": {
            "answer": "Enjoy rugged game drives through a dramatic wilderness that feels entirely untouched by time. You can also take guided nature walks to spot unique birds and arrange an insightful cultural visit with the nearby Karamojong communities."
        },
        "Local food recommendations?": {
            "answer": "Meals are primarily hosted at the safari lodges, which serve a sophisticated mix of international dishes and traditional Ugandan classics. Ask your hosts if you can sample traditional roasted meats prepared in the authentic Karamoja style."
        },
        "Weather forecast?": {
            "answer": "Kidepo features a semi-arid climate, making it hot and dusty with temperatures frequently pushing past 32°C. The vast savannah skies are typically bright and clear, but the park can become difficult to access during peak rainy months."
        },
    },

    "kibale_national_park": {
        "What's the best time to visit?": {
            "answer": "The primary dry months of June to August and December to February offer the easiest trekking terrain. Clear weather means the forest floor is less slippery, making it much easier to keep pace with the primates."
        },
        "Top things to do here?": {
            "answer": "Embark on an exhilarating chimpanzee tracking excursion in the 'Primate Capital of the World' to see our closest wild relatives. You can also explore the Bigodi Wetland Sanctuary boardwalk for incredible bird and monkey sightings."
        },
        "Local food recommendations?": {
            "answer": "Savor classic Ugandan dishes like matoke, sweet potatoes, and rich groundnut stews at the lovely eco-lodges nearby. Be sure to try the locally sourced, aromatic organic tea grown on the beautiful estates bordering the forest."
        },
        "Weather forecast?": {
            "answer": "Kibale maintains a refreshing and humid forest climate, with daytime temperatures averaging a comfortable 20°C to 25°C. Expect a high chance of rainfall at any time, which keeps this beautiful evergreen forest lush and thriving."
        },
    },

    "rwenzori_mountains": {
        "What's the best time to visit?": {
            "answer": "January to February and June to August are the safest, driest windows for mountaineering. Clear skies during these months offer unmatched, crisp alpine views and reduce the risk of dangerous, slippery trails."
        },
        "Top things to do here?": {
            "answer": "Challenge yourself with a multi-day trek up the legendary 'Mountains of the Moon' to see rare equatorial glaciers. For less intense adventures, enjoy nature walks through unique heather forests and look out for endemic mountain birds."
        },
        "Local food recommendations?": {
            "answer": "Replenish your energy on the trails with hearty local Bakonzo dishes, including comforting cassava bread and fresh mountain greens. Mountain lodges focus on serving high-carbohydrate, warm meals to keep hikers fueled and energized."
        },
    },

    "lake_bunyonyi": {
        "What's the best time to visit?": {
            "answer": "The dry seasons from June to August and December to February provide bright, calm days that are ideal for watersports. You'll get beautifully clear water reflections and gorgeous sunset views over the terraced hills."
        },
        "Top things to do here?": {
            "answer": "Explore the lake's 29 islands via a traditional dugout canoe or high-speed motorboat tour. Because the lake is entirely free of bilharzia, hippos, and crocodiles, it is one of the safest places in Africa for open-water swimming."
        },
        "Local food recommendations?": {
            "answer": "Lake Bunyonyi is legendary for its local freshwater crayfish, served up in everything from garlic stir-fries to rich, creamy soups. Pair them with locally grown Irish potatoes and a cup of freshly brewed Kigezi coffee."
        },
        "Weather forecast?": {
            "answer": "Set high in the southwestern highlands, Bunyonyi enjoys a crisp, temperate climate with daily temperatures peaking around 25°C. Evenings get surprisingly chilly, so you'll want to pack a warm sweater for nights by the water."
        },
    },

    "sipi_falls": {
        "What's the best time to visit?": {
            "answer": "December to February and June to August feature the best hiking conditions with minimal mud on the steep cliffside paths. However, visiting right at the end of the rainy season offers the most powerful, roaring waterfall views."
        },
        "Top things to do here?": {
            "answer": "Hike the scenic trail that links all three breathtaking waterfalls, and try thrilling cliffside abseiling if you are feeling brave. You can also take an immersive tour of a local Bugisu coffee farm to see how world-class Arabica is grown and roasted."
        },
        "Local food recommendations?": {
            "answer": "You must treat yourself to a cup of locally grown, hand-roasted Bugisu Arabica coffee right at the source. Pair it with traditional matoke or freshly harvested volcanic vegetables grown on the fertile slopes of Mount Elgon."
        },
        "Weather forecast?": {
            "answer": "Sipi Falls sits on an elevated mountain slope, making the air delightfully cool and fresh with average temperatures around 22°C. The area receives plenty of highland rainfall, which keeps the falls flowing and the surrounding landscape beautifully green."
        },
    },

    "lake_mburo_national_park": {
        "What's the best time to visit?": {
            "answer": "The dry months are the premium choice for viewing wildlife around the park's central lakes. The short grass makes it incredibly easy to spot zebras, impalas, and elusive leopards."
        },
        "Top things to do here?": {
            "answer": "Experience a thrilling horseback safari or a guided walking safari to get uniquely close to the wildlife without the noise of an engine. You can also take a peaceful boat cruise on Lake Mburo to spot hippos and brilliant African finfoots."
        },
        "Local food recommendations?": {
            "answer": "The park's safari lodges serve an excellent mix of continental favorites and Ugandan delicacies. Enjoy fresh milk and traditional beef dishes influenced by the neighboring Ankole pastoral communities."
        },
        "Weather forecast?": {
            "answer": "The park features a very mild savannah climate with daytime highs averaging around 27°C. It is generally drier here than in other parks, but downpours in April and November can make some of the low-lying valley tracks muddy."
        },
    },

    "kabale": {
        "What's the best time to visit?": {
            "answer": "June to August and December to February offer dry weather that is perfect for scenic mountain driving and hiking. The roads are firm, making it easy to access the remote southwestern highlands."
        },
        "Top things to do here?": {
            "answer": "Use the town as a base to explore nearby Lake Bunyonyi, or hike the surrounding terraced hillsides for incredible alpine views. You can also explore local markets to experience the authentic daily rhythm of Kigezi culture."
        },
        "Local food recommendations?": {
            "answer": "This region is famous for producing the best Irish potatoes in Uganda, usually served alongside hearty bean stews and fresh matoke. Don't miss out on trying the local freshwater crayfish caught fresh from the nearby waters."
        },
        "Weather forecast?": {
            "answer": "Known as the 'Switzerland of Africa,' Kabale has a unique, refreshingly cool highland climate where daytime temperatures hover around 20°C. Heavy morning mists are a signature feature, and nights can get quite cold."
        },
    },
}
#used to create cache
# for name_space in tourism_knowledge.keys():
#     place_dict = tourism_knowledge[name_space]
#     for key,value in place_dict.items():
#         prompt = key
#         answer_object = value["answer"]
#         print(answer_object)
#         cache_key = create_cache(prompt, name_space)
#         redis_client.set(cache_key, json.dumps(answer_object))


# def time_redis_response():
#     start_time = time.time()
#     value = redis_client.get(create_cache("What's the best time to visit?", "kampala"))
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     return elapsed_time, value
# time_taken, value = time_redis_response()
def redis_call(prompt:str,namespace:str):
    
    cache_key = create_cache(prompt, namespace)
    value = redis_client.get(cache_key)
    if value is not None:
        return json.loads(value)
    else:
        return None

# def time_llm_response():
#     from app_main import run_query_test
#     start_time = time.time()
#     value = run_query_test("kampala","Kampala", "What's the best time to visit?",[])
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     return elapsed_time, value

# time_taken_llm, value_llm = time_llm_response()
# print(f"Time taken for Redis response: {time_taken:.6f} seconds")
# print(f"Time taken for LLM response: {time_taken_llm:.6f} seconds")









