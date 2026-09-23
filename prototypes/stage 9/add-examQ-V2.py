"""
add_exam_questions_v2.py
Adds 2, 3, 5, and 9 mark questions for all 3 topics.
Safe to run multiple times — checks for duplicates first.
"""
import sqlite3

conn   = sqlite3.connect("database.db")
cursor = conn.cursor()

new_questions = [

    # ══ COASTAL LANDSCAPES ══════════════════════════════════════════

    (
        "Coastal Landscapes", 2,
        "Describe one difference between a constructive wave and a destructive wave.",
        "Constructive waves have a strong swash and weak backwash, building up beaches through deposition. [1 mark] "
        "Destructive waves have a weak swash and strong backwash, removing material and causing erosion. [1 mark] "
        "[Award 1 mark for each correct difference clearly stated. Must be a comparison, not just a description of one type.]"
    ),
    (
        "Coastal Landscapes", 3,
        "Explain how longshore drift transports material along a coastline. [3 marks]",
        "Waves approach the beach at an angle determined by the prevailing wind direction. [1] "
        "The swash carries sediment up the beach at this angle. [1] "
        "The backwash returns sediment straight down the beach at 90 degrees due to gravity, "
        "moving material along the coast in a zigzag pattern. [1] "
        "[1 mark for: waves approaching at an angle; swash moving sediment at an angle; "
        "backwash returning sediment perpendicular to shore / zigzag movement described]"
    ),
    (
        "Coastal Landscapes", 5,
        "Explain how headlands and bays are formed. [5 marks]",
        "Headlands and bays form along discordant coastlines where bands of hard and soft rock "
        "alternate at right angles to the sea. [1] "
        "Soft rock such as clay or sand is eroded more quickly by wave action through processes "
        "such as hydraulic action and abrasion. [1] "
        "This forms an indentation in the coastline called a bay. [1] "
        "The harder, more resistant rock on either side erodes more slowly and protrudes "
        "out to sea, forming a headland. [1] "
        "Over time the headland becomes more exposed to wave energy and begins to erode "
        "through processes such as wave refraction concentrating energy at its sides. [1] "
        "[1 mark each for: discordant coastline / alternating rock types; differential erosion; "
        "bay formation in soft rock; headland formation in hard rock; headland erosion / wave refraction]"
    ),
    (
        "Coastal Landscapes", 9,
        "Evaluate the costs and benefits of managed retreat as a coastal management strategy. "
        "Refer to a named example in your answer. [9 marks]",
        "Managed retreat (also called coastal realignment) involves allowing the sea to flood "
        "low-lying coastal land, creating new intertidal habitats such as saltmarshes and mudflats. "
        "A key example is Medmerry in West Sussex, where 7km of shingle bank was breached in 2013 "
        "to create 183 hectares of new intertidal habitat, protecting nearby Selsey from flooding. "
        "\nBenefits: Managed retreat is significantly cheaper than hard engineering — Medmerry cost "
        "£28 million compared to the estimated £300 million to maintain the existing sea defences. "
        "It creates valuable habitat for wildlife including wading birds and supports biodiversity. "
        "It works with natural processes rather than against them, providing sustainable long-term "
        "protection. New saltmarshes also act as natural carbon stores, providing additional "
        "environmental benefits. "
        "\nCosts: Agricultural land and property are permanently lost, which is deeply unpopular with "
        "landowners and farmers who may have owned the land for generations. Compensation schemes "
        "are complex and expensive. The strategy is not suitable where high-value settlements or "
        "infrastructure are threatened. It can also be politically difficult to implement as "
        "communities resist losing land. "
        "\nOverall, managed retreat is most effective in areas of low-value agricultural land where "
        "alternative hard engineering would be prohibitively expensive. It is not a universal "
        "solution and must be considered as part of a Shoreline Management Plan alongside other "
        "strategies for higher-value areas. "
        "[Level 4 (8-9): Detailed evaluation with named example, balanced argument and clear judgement. "
        "Level 3 (6-7): Good explanation of costs and benefits, named example used. "
        "Level 2 (4-5): Some explanation of costs and/or benefits, limited use of example. "
        "Level 1 (1-3): Basic knowledge of managed retreat.]"
    ),

    # ══ RIVER LANDSCAPES ════════════════════════════════════════════

    (
        "River Landscapes", 2,
        "State two differences between the upper course and lower course of a river.",
        "Award 1 mark for each correct difference up to 2 marks. Accept any two of: "
        "Upper course has a steep gradient / lower course has a gentle gradient. [1] "
        "Upper course has a narrow, shallow channel / lower course has a wide, deep channel. [1] "
        "Upper course is dominated by vertical erosion / lower course by deposition. [1] "
        "Upper course has fast-flowing water over rocks / lower course has slow-flowing water. [1] "
        "Upper course has a V-shaped valley / lower course has a wide floodplain. [1]"
    ),
    (
        "River Landscapes", 3,
        "Explain how a waterfall is formed. [3 marks]",
        "A waterfall forms where a band of hard rock lies over softer rock. [1] "
        "The softer rock is eroded more quickly by the river through hydraulic action and abrasion, "
        "undercutting the hard rock above. [1] "
        "The hard rock is left overhanging and eventually collapses, causing the waterfall to retreat "
        "upstream, leaving a steep-sided gorge. [1] "
        "[1 mark each for: hard over soft rock / differential erosion; undercutting of soft rock; "
        "collapse and retreat / gorge formation]"
    ),
    (
        "River Landscapes", 5,
        "Explain how an oxbow lake is formed. [5 marks]",
        "Oxbow lakes form from meanders in the middle and lower course of a river. [1] "
        "Erosion occurs on the outside of the meander bend where water flows fastest, "
        "creating a river cliff through hydraulic action and abrasion. [1] "
        "Deposition occurs on the inside of the bend where water flows more slowly, "
        "building up a slip-off slope. [1] "
        "Over time the meander becomes more pronounced and the neck of the meander narrows. [1] "
        "During a flood the river cuts through the narrow neck, taking the straightest course. "
        "Deposition seals off the old meander loop, forming a horseshoe-shaped oxbow lake. [1] "
        "[1 mark each for: meander context; outside bank erosion; inside bank deposition; "
        "neck narrowing; flood cuts through / deposition seals off lake]"
    ),
    (
        "River Landscapes", 9,
        "Evaluate the effectiveness of hard and soft engineering strategies in managing the "
        "risk of river flooding. Refer to examples in your answer. [9 marks]",
        "Hard engineering strategies attempt to control rivers directly using artificial structures. "
        "Dams and reservoirs, such as the Kielder Reservoir in Northumberland, regulate river flow "
        "by storing water during periods of high rainfall and releasing it slowly. They are very "
        "effective at preventing flooding downstream but are extremely expensive to build, can "
        "displace communities and alter sediment supply downstream causing erosion. "
        "Embankments (raised levees) protect settlements along the river banks but can increase "
        "flood risk further downstream by speeding up the flow of water. The Thames Barrier is "
        "highly effective but cost over £500 million and requires ongoing maintenance. "
        "Channelisation straightens and deepens the river channel, increasing its capacity, "
        "but transfers flood risk downstream. "
        "\nSoft engineering strategies work with natural processes. Floodplain zoning prevents "
        "new development in high-risk areas, reducing future flood damage, but cannot protect "
        "existing buildings. Afforestation increases interception and slows runoff, reducing "
        "peak discharge, but takes many years to become effective. Washlands allow rivers to "
        "flood designated areas of low-value land, protecting higher-value areas downstream. "
        "\nOverall, hard engineering provides immediate, reliable protection for high-value "
        "urban areas but is expensive and can create problems elsewhere. Soft engineering is "
        "cheaper and more sustainable but slower to take effect. The most effective approach "
        "combines both — hard engineering to protect existing settlements and soft engineering "
        "to reduce future risk — as seen in integrated catchment management schemes. "
        "[Level 4 (8-9): Balanced evaluation of both types with named examples and clear judgement. "
        "Level 3 (6-7): Explains effectiveness of both with some named examples. "
        "Level 2 (4-5): Describes strategies with limited evaluation. "
        "Level 1 (1-3): Basic knowledge only.]"
    ),

    # ══ RESOURCE MANAGEMENT ═════════════════════════════════════════

    (
        "Resource Management", 2,
        "Describe two impacts of water insecurity on people.",
        "Award 1 mark for each correct impact up to 2 marks. Accept any two of: "
        "Disease / contaminated water causes illness such as cholera or typhoid. [1] "
        "Reduced food production / crop failure due to lack of irrigation water. [1] "
        "Economic impacts — reduced GDP as industries require water to function. [1] "
        "Conflict between countries or communities over shared water resources. [1] "
        "Time poverty — especially for women and girls who travel long distances to collect water. [1]"
    ),
    (
        "Resource Management", 3,
        "Explain why some countries have a greater demand for energy than others. [3 marks]",
        "More economically developed countries (MEDCs) have greater energy demand because "
        "they have more industry, manufacturing and services that require large amounts of energy. [1] "
        "Higher standards of living in wealthier countries mean greater energy use for "
        "heating, cooling, transport and electronics per person. [1] "
        "Rapidly industrialising countries such as China and India have dramatically increasing "
        "energy demand as their economies grow and more people adopt higher-consumption lifestyles. [1] "
        "[1 mark each for: industrial/economic development; higher living standards / per capita consumption; "
        "rapid industrialisation / named example of developing country]"
    ),
    (
        "Resource Management", 5,
        "Explain how the demand for food is increasing globally. [5 marks]",
        "The global population is growing rapidly, currently over 8 billion, which directly "
        "increases the total amount of food required. [1] "
        "Rising incomes in developing countries, particularly in Asia, mean people can afford "
        "more varied diets including more meat, which requires significantly more land and water "
        "to produce than plant-based foods. [1] "
        "Urbanisation means more people live in cities and purchase food rather than growing "
        "their own, increasing demand in commercial food supply chains. [1] "
        "Changing diets due to globalisation have introduced Western-style high-calorie diets "
        "to countries that previously had lower-consumption food cultures. [1] "
        "Food waste throughout the supply chain means more food must be produced to meet "
        "actual nutritional needs, artificially inflating demand. [1] "
        "[1 mark each for: population growth; rising incomes / meat consumption; "
        "urbanisation; changing diets / globalisation; food waste]"
    ),
    (
        "Resource Management", 9,
        "Evaluate the extent to which large-scale water transfer schemes are the best way "
        "to solve water insecurity. Refer to examples in your answer. [9 marks]",
        "Water transfer schemes move water from areas of surplus to areas of deficit through "
        "pipelines, canals or aqueducts. The South-North Water Transfer Project in China, "
        "costing over $60 billion, is the world's largest, transferring water from the Yangtze "
        "River to the drier north. It has successfully increased water supply to hundreds of "
        "millions of people in Beijing and other northern cities. "
        "\nHowever, large-scale transfer schemes have significant disadvantages. They are "
        "extremely expensive and only accessible to wealthy nations. They can cause environmental "
        "damage by reducing water levels in source rivers, harming ecosystems and agriculture "
        "downstream. Large infrastructure projects also displace communities. "
        "\nAlternative approaches may be more appropriate in different contexts. Water conservation "
        "measures such as fixing leaking pipes (the UK loses 20% of water through leakage), "
        "metered supplies and public education can reduce demand without new infrastructure. "
        "Desalination, used extensively in Israel and Saudi Arabia, provides reliable supply "
        "from seawater but is very energy-intensive. Groundwater extraction is affordable for "
        "smaller communities but risks long-term depletion of aquifers. Rainwater harvesting "
        "is a low-cost, locally appropriate solution for rural areas in developing countries. "
        "\nOverall, large-scale transfer schemes are effective where water deficits are severe "
        "and governments have the financial resources to invest, but they are not universally "
        "the best solution. A combination of approaches tailored to local conditions — including "
        "demand management and appropriate technology — is likely to be most effective in "
        "addressing global water insecurity. "
        "[Level 4 (8-9): Balanced evaluation with named examples, considers alternatives, clear judgement. "
        "Level 3 (6-7): Explains strengths and weaknesses with some examples. "
        "Level 2 (4-5): Describes transfer schemes with limited evaluation. "
        "Level 1 (1-3): Basic knowledge of water insecurity.]"
    ),
]

inserted = 0
skipped  = 0
for topic, marks, question_text, model_answer in new_questions:
    cursor.execute(
        "SELECT COUNT(*) FROM exam_questions WHERE question_text = ?",
        (question_text,)
    )
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO exam_questions (topic, marks, question_text, model_answer)
            VALUES (?, ?, ?, ?)
        """, (topic, marks, question_text, model_answer))
        inserted += 1
    else:
        skipped += 1

conn.commit()
conn.close()
print(f"[OK] {inserted} new exam questions added.")
print(f"[OK] {skipped} questions already existed — skipped.")
print("[OK] Done. Your exam_questions table now has full coverage of all mark values.")