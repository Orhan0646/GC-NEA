"""
migrate_stage9.py
Run ONCE to add exam_questions and exam_responses tables.
Safe to run multiple times — uses IF NOT EXISTS.
"""
import sqlite3

conn   = sqlite3.connect("database.db")
cursor = conn.cursor()

# ── exam_questions table ─────────────────────────────────────────────
cursor.execute("""
    CREATE TABLE IF NOT EXISTS exam_questions (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        topic        TEXT    NOT NULL,
        marks        INTEGER NOT NULL,
        question_text TEXT   NOT NULL,
        model_answer  TEXT   NOT NULL
    )
""")
print("[OK] exam_questions table ready.")

# ── exam_responses table ─────────────────────────────────────────────
cursor.execute("""
    CREATE TABLE IF NOT EXISTS exam_responses (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id      INTEGER NOT NULL,
        question_id     INTEGER NOT NULL,
        response_text   TEXT    NOT NULL,
        marks_awarded   INTEGER DEFAULT NULL,
        feedback        TEXT    DEFAULT NULL,
        marked          INTEGER DEFAULT 0,
        date_submitted  DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id)  REFERENCES students(id),
        FOREIGN KEY (question_id) REFERENCES exam_questions(id)
    )
""")
print("[OK] exam_responses table ready.")

# ── Seed AQA-style exam questions ────────────────────────────────────
questions = [

    # ── COASTAL LANDSCAPES ──────────────────────────────────────────
    (
        "Coastal Landscapes", 1,
        "State one process of coastal erosion.",
        "Any one of: hydraulic action (waves compress air into cracks, widening them), "
        "abrasion (waves hurl sediment against cliffs, wearing them away), "
        "attrition (rocks carried by waves knock together and become smaller and rounder), "
        "solution/corrosion (seawater dissolves soluble minerals from rock). "
        "[1 mark for a correct named process]"
    ),
    (
        "Coastal Landscapes", 4,
        "Explain how a spit is formed. [4 marks]",
        "A spit forms where a coastline changes direction, such as at a river mouth or bay. "
        "Longshore drift transports material along the coast in a zigzag pattern due to the "
        "swash moving sediment at an angle and the backwash returning it straight down the beach. "
        "When the coastline changes direction the water loses energy and deposits its load, "
        "building up a finger of sand and shingle extending out to sea. "
        "The end of the spit often curves due to secondary wind directions creating a recurved end. "
        "A sheltered lagoon or saltmarsh may form behind the spit. "
        "[1 mark each for: longshore drift process, change in coastline direction causing deposition, "
        "spit extending into sea, curved end / sheltered area behind]"
    ),
    (
        "Coastal Landscapes", 6,
        "Explain how cliff retreat leads to the formation of a wave-cut platform. [6 marks]",
        "Waves attack the base of a cliff between the high and low water marks through "
        "hydraulic action and abrasion, creating a wave-cut notch. As the notch deepens "
        "the overlying rock becomes unsupported and the cliff collapses, retreating inland. "
        "Repeated collapse causes the cliff to retreat further, leaving a gently sloping "
        "rocky platform at the base called a wave-cut platform. "
        "The platform itself limits further erosion as it causes waves to break earlier "
        "and lose energy before reaching the cliff. "
        "Over time the platform widens as the cliff retreats further inland. "
        "[Level 3 (5-6): Detailed explanation of the process sequence with accurate terminology. "
        "Level 2 (3-4): Some explanation with some accurate terminology. "
        "Level 1 (1-2): Basic description with limited terminology.]"
    ),
    (
        "Coastal Landscapes", 8,
        "Evaluate the effectiveness of hard engineering strategies in managing coastal erosion. [8 marks]",
        "Hard engineering strategies include sea walls, groynes, rock armour (rip-rap) and offshore breakwaters. "
        "Sea walls are effective at directly preventing wave erosion but are very expensive (£10,000+ per metre), "
        "visually intrusive and can increase erosion at their base due to wave reflection. "
        "Groynes trap sediment and build up beaches which naturally protect the coast, but interrupt longshore drift "
        "causing erosion further down the coast (terminal groyne syndrome). "
        "Rock armour is cheaper and more natural-looking but requires regular maintenance and is less effective "
        "in high-energy environments. "
        "Overall, hard engineering provides short-term protection for high-value assets such as settlements "
        "but can create new problems elsewhere on the coast and does not address the underlying causes of erosion. "
        "Soft engineering (beach nourishment, managed retreat) is increasingly preferred as it works with "
        "natural processes. "
        "[Level 4 (7-8): Balanced evaluation with named examples and judgement. "
        "Level 3 (5-6): Explanation of advantages and disadvantages. "
        "Level 2 (3-4): Describes strategies with some comment. "
        "Level 1 (1-2): Basic knowledge of hard engineering.]"
    ),

    # ── RIVER LANDSCAPES ────────────────────────────────────────────
    (
        "River Landscapes", 1,
        "State one feature of a river in its lower course.",
        "Any one of: wide floodplain, meanders, oxbow lakes, levees, large channel width, "
        "low gradient, deposition is dominant, high discharge. "
        "[1 mark for any correct feature]"
    ),
    (
        "River Landscapes", 4,
        "Explain how meanders are formed. [4 marks]",
        "Meanders form in the middle and lower course of a river where the gradient is gentler. "
        "Water moves faster on the outside of a bend due to the thalweg (line of fastest flow) "
        "being pushed to the outer bank, causing lateral erosion through hydraulic action and abrasion "
        "creating a river cliff. "
        "On the inside of the bend water moves more slowly and deposits its load, forming a slip-off slope "
        "or point bar. "
        "This erosion on the outside and deposition on the inside causes the bend to become more pronounced "
        "over time, forming a meander. "
        "[1 mark each for: faster flow on outside, erosion on outside forming river cliff, "
        "deposition on inside forming slip-off slope, meander becoming more pronounced over time]"
    ),
    (
        "River Landscapes", 6,
        "Explain the causes of river flooding. [6 marks]",
        "River flooding occurs when a river's discharge exceeds the capacity of its channel. "
        "Physical causes include prolonged or intense rainfall which saturates the ground and "
        "increases surface runoff reaching the river quickly. Snowmelt in spring can rapidly "
        "increase discharge. Impermeable rock geology prevents infiltration, increasing runoff. "
        "Steep valley sides increase the speed at which water reaches the river. "
        "Human causes include urbanisation which replaces permeable surfaces with impermeable "
        "concrete, increasing surface runoff and reducing lag time. Deforestation reduces "
        "interception and increases runoff. River management such as channelisation can "
        "increase the speed of flow downstream, increasing flood risk there. "
        "[Level 3 (5-6): Detailed explanation of both physical and human causes. "
        "Level 2 (3-4): Explains some causes, may lack balance. "
        "Level 1 (1-2): Basic description of flooding.]"
    ),
    (
        "River Landscapes", 8,
        "Evaluate the effectiveness of river flood management strategies. [8 marks]",
        "Flood management strategies can be divided into hard engineering (dams, embankments, "
        "channelisation) and soft engineering (floodplain zoning, afforestation, washlands). "
        "Dams such as the Three Gorges Dam in China are very effective at regulating discharge "
        "but are extremely expensive, displace communities and alter ecosystems downstream. "
        "Embankments (raised levees) protect settlements but can increase flood risk further "
        "downstream and give a false sense of security leading to increased development on "
        "floodplains. Channelisation speeds up flow reducing local flood risk but transfers "
        "the problem downstream. Soft engineering strategies such as afforestation increase "
        "interception and slow runoff, addressing root causes rather than symptoms, but take "
        "many years to become effective. Floodplain zoning prevents new development in "
        "high-risk areas but is difficult to enforce retrospectively. Overall, an integrated "
        "approach combining hard and soft engineering tailored to local conditions is most "
        "effective, as no single strategy addresses all causes of flooding. "
        "[Level 4 (7-8): Balanced evaluation with named examples and clear judgement. "
        "Level 3 (5-6): Discusses advantages and disadvantages of multiple strategies. "
        "Level 2 (3-4): Describes strategies with limited evaluation. "
        "Level 1 (1-2): Basic knowledge only.]"
    ),

    # ── RESOURCE MANAGEMENT ─────────────────────────────────────────
    (
        "Resource Management", 1,
        "State one way in which water can be conserved.",
        "Any one of: fixing leaking pipes, using water meters, low-flush toilets, "
        "grey water recycling, drip irrigation, rainwater harvesting, public education campaigns. "
        "[1 mark for any correct method]"
    ),
    (
        "Resource Management", 4,
        "Explain why water availability varies around the world. [4 marks]",
        "Water availability varies due to both physical and human factors. "
        "Physical factors include climate — areas with high rainfall such as the UK have "
        "greater water availability than arid areas like the Sahel. Seasonal variation means "
        "some areas have water only during wet seasons. "
        "Human factors include population growth which increases demand, "
        "pollution of water sources which reduces usable supply, and poverty which limits "
        "investment in water infrastructure meaning safe water is unavailable even where "
        "it physically exists. Economic development also increases per capita water consumption "
        "through industry and agriculture. "
        "[1 mark each for: climate/rainfall variation, seasonal variation, population growth "
        "increasing demand, human factors such as pollution or poverty]"
    ),
    (
        "Resource Management", 6,
        "Explain how food production can be made more sustainable. [6 marks]",
        "Food production can be made more sustainable through a range of strategies. "
        "Organic farming avoids synthetic pesticides and fertilisers, reducing soil and water "
        "pollution and preserving biodiversity. Crop rotation maintains soil fertility naturally "
        "and reduces the need for chemical inputs. Irrigation efficiency can be improved through "
        "drip irrigation which delivers water directly to plant roots, reducing water waste "
        "compared to flood irrigation. Reducing food waste throughout the supply chain would "
        "reduce the resources needed to produce food overall. Eating less meat reduces the "
        "large land and water inputs required for livestock farming. Biotechnology such as "
        "drought-resistant crops can increase yields in water-scarce areas without increasing "
        "environmental impact. "
        "[Level 3 (5-6): Detailed explanation of multiple strategies clearly linked to sustainability. "
        "Level 2 (3-4): Explains some strategies with some reference to sustainability. "
        "Level 1 (1-2): Basic description of food production methods.]"
    ),
    (
        "Resource Management", 8,
        "Evaluate the extent to which increasing energy supply is a better solution to the "
        "energy gap than reducing energy consumption. [8 marks]",
        "The energy gap refers to the difference between growing energy demand and current supply. "
        "Increasing energy supply through renewables such as solar, wind and HEP offers long-term "
        "sustainable solutions that do not deplete finite resources. However, large-scale renewable "
        "infrastructure is expensive, intermittent (wind and solar depend on weather), and can have "
        "environmental impacts such as habitat loss from wind farms or HEP reservoirs. "
        "Fossil fuel supply can be increased rapidly and reliably but contributes to climate change "
        "and is finite. On the other hand, reducing energy consumption through improved insulation, "
        "energy-efficient appliances and public behaviour change addresses the root cause of the "
        "energy gap without requiring new infrastructure. However, in rapidly developing countries "
        "such as India and China, reducing consumption conflicts with economic development goals. "
        "Overall, neither approach alone is sufficient — an integrated strategy combining increased "
        "renewable supply with reduced consumption through efficiency measures offers the most "
        "sustainable solution to the energy gap. "
        "[Level 4 (7-8): Balanced evaluation of both sides with named examples and clear judgement. "
        "Level 3 (5-6): Discusses both approaches with some evaluation. "
        "Level 2 (3-4): Describes both approaches with limited evaluation. "
        "Level 1 (1-2): Basic knowledge of energy supply or demand.]"
    ),
]

# Insert questions (skip if already exist)
inserted = 0
for topic, marks, question_text, model_answer in questions:
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

conn.commit()
conn.close()
print(f"[OK] {inserted} exam questions added ({len(questions) - inserted} already existed).")
print("[OK] Stage 9 migration complete. You can now run app.py.")