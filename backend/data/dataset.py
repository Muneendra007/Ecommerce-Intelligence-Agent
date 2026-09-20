"""
Simulated Multi-Marketplace Dataset for GlowSkin D2C Skincare Brand.

Contains:
- Brand: GlowSkin with 6 SKUs across core skincare categories
- Competitors: DermaCare (6 SKUs), PureSkin (6 SKUs) - Total 18 Products
- Marketplaces: Amazon, Nykaa, Flipkart, Blinkit (Quick Commerce), Brand D2C Store
- 140-175 reviews per product (~2,800+ total reviews)
- 4-month sales & return trends (Nov 2025 - Feb 2026)
- Comprehensive feature lists, pricing, and category market intelligence
"""

from __future__ import annotations
import random
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════
# 1. PRODUCTS & SALES DATA
# ═══════════════════════════════════════════════════════════════

GLOWSKIN_PRODUCTS = [
    {
        "sku": "VITC30",
        "name": "GlowSkin Vitamin C Serum 30ml",
        "brand": "GlowSkin",
        "price": 899,
        "rating": 4.2,
        "marketplace": "Amazon",
        "category": "Serum",
        "features": [
            "20% Vitamin C (L-Ascorbic Acid)",
            "Hyaluronic Acid infused",
            "Paraben-free formula",
            "Suitable for all skin types",
            "30ml glass dropper bottle",
            "Brightening and anti-aging",
            "Dermatologist tested",
        ],
        "sales_data": [
            {"month": "2025-11", "units_sold": 1950, "revenue": 1753050, "returns": 85},
            {"month": "2025-12", "units_sold": 1820, "revenue": 1635780, "returns": 91},
            {"month": "2026-01", "units_sold": 1650, "revenue": 1483350, "returns": 115},
            {"month": "2026-02", "units_sold": 1480, "revenue": 1330520, "returns": 133},
        ],
        "market_trends": {
            "category_growth_rate": "18% YoY",
            "seasonal_peak": "Oct-Dec (wedding/festive season)",
            "online_share": "62% of category sales online",
            "avg_repurchase_cycle": "45 days",
        },
    },
    {
        "sku": "HYALU50",
        "name": "GlowSkin Hyaluronic Acid Moisturizer 50ml",
        "brand": "GlowSkin",
        "price": 1299,
        "rating": 4.5,
        "marketplace": "Amazon",
        "category": "Moisturizer",
        "features": [
            "Triple Molecular Weight Hyaluronic Acid",
            "Ceramide complex for barrier repair",
            "72-hour hydration lock",
            "Fragrance-free",
            "50ml airless pump bottle",
            "Non-comedogenic",
            "Clinically tested on sensitive skin",
            "Vegan and cruelty-free",
        ],
        "sales_data": [
            {"month": "2025-11", "units_sold": 2100, "revenue": 2727900, "returns": 42},
            {"month": "2025-12", "units_sold": 2350, "revenue": 3052650, "returns": 47},
            {"month": "2026-01", "units_sold": 2580, "revenue": 3351420, "returns": 52},
            {"month": "2026-02", "units_sold": 2710, "revenue": 3520290, "returns": 41},
        ],
        "market_trends": {
            "category_growth_rate": "22% YoY",
            "seasonal_peak": "Nov-Feb (winter dryness)",
            "online_share": "58% of category sales online",
            "avg_repurchase_cycle": "60 days",
        },
    },
    {
        "sku": "RETA15",
        "name": "GlowSkin Retinol Night Cream 15ml",
        "brand": "GlowSkin",
        "price": 1499,
        "rating": 3.8,
        "marketplace": "Amazon",
        "category": "Night Cream",
        "features": [
            "0.5% Encapsulated Retinol",
            "Niacinamide + Peptide complex",
            "Night repair formula",
            "Anti-wrinkle and firming",
            "15ml jar packaging",
            "Dermatologist recommended",
        ],
        "sales_data": [
            {"month": "2025-11", "units_sold": 1120, "revenue": 1678880, "returns": 95},
            {"month": "2025-12", "units_sold": 980, "revenue": 1469020, "returns": 108},
            {"month": "2026-01", "units_sold": 870, "revenue": 1304130, "returns": 122},
            {"month": "2026-02", "units_sold": 740, "revenue": 1109260, "returns": 141},
        ],
        "market_trends": {
            "category_growth_rate": "25% YoY",
            "seasonal_peak": "Year-round (anti-aging is evergreen)",
            "online_share": "55% of category sales online",
            "avg_repurchase_cycle": "30 days (small bottle)",
        },
    },
    {
        "sku": "SUN50",
        "name": "GlowSkin Ultra Matte Sunscreen Gel SPF 50 PA++++ 50g",
        "brand": "GlowSkin",
        "price": 699,
        "rating": 4.3,
        "marketplace": "Nykaa",
        "category": "Sunscreen",
        "features": [
            "Broad Spectrum SPF 50 PA++++",
            "Ultra-matte finish with zero white cast",
            "Cica extract + Niacinamide for calming",
            "Sweat and water resistant (80 mins)",
            "Non-greasy silicone-free gel formula",
            "Tested on Indian skin tones (Fitzpatrick IV-VI)",
            "50g travel-friendly pump tube",
        ],
        "sales_data": [
            {"month": "2025-11", "units_sold": 2800, "revenue": 1957200, "returns": 84},
            {"month": "2025-12", "units_sold": 3200, "revenue": 2236800, "returns": 96},
            {"month": "2026-01", "units_sold": 3550, "revenue": 2481450, "returns": 112},
            {"month": "2026-02", "units_sold": 4100, "revenue": 2865900, "returns": 128},
        ],
        "market_trends": {
            "category_growth_rate": "38% YoY",
            "seasonal_peak": "Feb-June (summer onset) + holiday travel",
            "online_share": "68% of category sales online",
            "avg_repurchase_cycle": "40 days",
        },
    },
    {
        "sku": "NIAC10",
        "name": "GlowSkin 10% Niacinamide Clarifying Serum 30ml",
        "brand": "GlowSkin",
        "price": 649,
        "rating": 4.4,
        "marketplace": "Amazon",
        "category": "Serum",
        "features": [
            "10% Pure Niacinamide (Vitamin B3)",
            "1% Zinc PCA for active sebum control",
            "Fades post-acne blemishes and dark spots",
            "Refines enlarged pores and balances oily T-zone",
            "Alcohol, paraben, and synthetic fragrance free",
            "Ultra-lightweight watery texture",
            "30ml amber bottle with dropper",
        ],
        "sales_data": [
            {"month": "2025-11", "units_sold": 1950, "revenue": 1265550, "returns": 58},
            {"month": "2025-12", "units_sold": 2180, "revenue": 1414820, "returns": 65},
            {"month": "2026-01", "units_sold": 2320, "revenue": 1505680, "returns": 71},
            {"month": "2026-02", "units_sold": 2490, "revenue": 1616010, "returns": 79},
        ],
        "market_trends": {
            "category_growth_rate": "30% YoY",
            "seasonal_peak": "Monsoon & Summer (humidity breakouts)",
            "online_share": "72% of category sales online",
            "avg_repurchase_cycle": "50 days",
        },
    },
    {
        "sku": "SALI100",
        "name": "GlowSkin 2% Salicylic Acid Acne Control Cleanser 100ml",
        "brand": "GlowSkin",
        "price": 499,
        "rating": 4.1,
        "marketplace": "Blinkit",
        "category": "Cleanser",
        "features": [
            "2% Encapsulated Salicylic Acid (BHA)",
            "Tea Tree Oil and Centella Asiatica",
            "Sulphate-free foaming gel base",
            "Deep pore unclogging to prevent blackheads",
            "Maintains skin pH at 5.5",
            "100ml pump bottle dispenser",
        ],
        "sales_data": [
            {"month": "2025-11", "units_sold": 2100, "revenue": 1047900, "returns": 105},
            {"month": "2025-12", "units_sold": 1950, "revenue": 973050, "returns": 118},
            {"month": "2026-01", "units_sold": 1820, "revenue": 908180, "returns": 142},
            {"month": "2026-02", "units_sold": 1610, "revenue": 803390, "returns": 165},
        ],
        "market_trends": {
            "category_growth_rate": "20% YoY",
            "seasonal_peak": "Summer & Monsoon",
            "online_share": "54% online (high quick-commerce adoption)",
            "avg_repurchase_cycle": "35 days",
        },
    },
]

DERMACARE_PRODUCTS = [
    {
        "sku": "DC-VITC25",
        "name": "DermaCare Vitamin C Glow Serum 25ml",
        "brand": "DermaCare",
        "price": 799,
        "rating": 4.4,
        "marketplace": "Amazon",
        "category": "Serum",
        "features": [
            "25% Stabilized Vitamin C (Ethyl Ascorbic Acid)",
            "Ferulic Acid + Vitamin E",
            "SPF booster technology",
            "Quick-absorb formula",
            "25ml bottle with dropper",
            "Suitable for oily and combination skin",
            "ISO certified manufacturing",
            "2-year warranty on efficacy",
        ],
    },
    {
        "sku": "DC-MOIST60",
        "name": "DermaCare Aqua Surge Moisturizer 60ml",
        "brand": "DermaCare",
        "price": 1199,
        "rating": 4.3,
        "marketplace": "Amazon",
        "category": "Moisturizer",
        "features": [
            "Aquaporin technology",
            "Hyaluronic Acid + Aloe Vera",
            "Oil-free gel cream",
            "48-hour moisture retention",
            "60ml tube packaging",
            "Dermatologically tested",
        ],
    },
    {
        "sku": "DC-RETIN20",
        "name": "DermaCare Pro Retinol Cream 20ml",
        "brand": "DermaCare",
        "price": 1399,
        "rating": 4.1,
        "marketplace": "Amazon",
        "category": "Night Cream",
        "features": [
            "1% Retinol (Retinyl Palmitate)",
            "Bakuchiol + Squalane blend",
            "Gradual release technology",
            "20ml pump bottle",
            "Suitable for mature skin",
            "Clinical study backed results",
            "Money-back guarantee",
        ],
    },
    {
        "sku": "DC-SUN50",
        "name": "DermaCare Ultra Matte UV Defense SPF 50 PA++++ 50g",
        "brand": "DermaCare",
        "price": 649,
        "rating": 4.5,
        "marketplace": "Amazon",
        "category": "Sunscreen",
        "features": [
            "SPF 50+ PA++++ with German UV filters",
            "Oil-free mattifying formula",
            "Sebum regulator technology",
            "Zero white cast guarantee",
            "Water resistant 120 mins",
            "Free from benzophenones and oxybenzone",
        ],
    },
    {
        "sku": "DC-NIAC10",
        "name": "DermaCare Niacinamide 10% + Cica Complex 30ml",
        "brand": "DermaCare",
        "price": 599,
        "rating": 4.3,
        "marketplace": "Nykaa",
        "category": "Serum",
        "features": [
            "10% Niacinamide with Centella Asiatica",
            "Zinc PCA and Green Tea extract",
            "Targets PIH (post-inflammatory hyperpigmentation)",
            "Fragrance-free formula",
            "Dropper with dosage calibration marks",
        ],
    },
    {
        "sku": "DC-SALI100",
        "name": "DermaCare BHA Pore Purifying Face Wash 100ml",
        "brand": "DermaCare",
        "price": 449,
        "rating": 4.4,
        "marketplace": "Flipkart",
        "category": "Cleanser",
        "features": [
            "2% Salicylic Acid + LHA blend",
            "Anti-acne zinc active",
            "Leak-proof twist-lock pump bottle",
            "Gentle foaming without skin tightness",
            "Dermatologist tested for daily acne management",
        ],
    },
]

PURESKIN_PRODUCTS = [
    {
        "sku": "PS-VITCR30",
        "name": "PureSkin Vitamin C Radiance Drops 30ml",
        "brand": "PureSkin",
        "price": 949,
        "rating": 4.0,
        "marketplace": "Amazon",
        "category": "Serum",
        "features": [
            "15% Vitamin C (Sodium Ascorbyl Phosphate)",
            "Turmeric extract",
            "Organic ingredients",
            "30ml glass bottle",
            "Suitable for sensitive skin",
        ],
    },
    {
        "sku": "PS-HYDRA45",
        "name": "PureSkin Deep Hydra Cream 45ml",
        "brand": "PureSkin",
        "price": 1349,
        "rating": 4.2,
        "marketplace": "Nykaa",
        "category": "Moisturizer",
        "features": [
            "Plant-based Hyaluronic Acid",
            "Shea Butter + Jojoba Oil",
            "Rich cream texture",
            "45ml recycled packaging",
            "100% organic certified",
            "Eco-friendly brand",
        ],
    },
    {
        "sku": "PS-RETSERUM",
        "name": "PureSkin Retinol Renewal Serum 20ml",
        "brand": "PureSkin",
        "price": 1599,
        "rating": 3.9,
        "marketplace": "Amazon",
        "category": "Night Cream",
        "features": [
            "0.3% Pure Retinol",
            "Rosehip oil base",
            "Night use only",
            "20ml dropper bottle",
            "Vegan formula",
        ],
    },
    {
        "sku": "PS-SUN50",
        "name": "PureSkin Mineral Tinted Sun Fluid SPF 50 50ml",
        "brand": "PureSkin",
        "price": 799,
        "rating": 4.1,
        "marketplace": "Nykaa",
        "category": "Sunscreen",
        "features": [
            "100% Non-nano Zinc Oxide mineral filter",
            "Universal sheer tint for warm skin tones",
            "Infused with carrot seed and aloe oil",
            "Reef-safe and biodegradable packaging",
            "Slight dewy glow finish",
        ],
    },
    {
        "sku": "PS-NIAC10",
        "name": "PureSkin Organic Niacinamide & Rice Water Elixir 30ml",
        "brand": "PureSkin",
        "price": 699,
        "rating": 4.2,
        "marketplace": "Amazon",
        "category": "Serum",
        "features": [
            "8% Niacinamide + Fermented Rice Water",
            "Ayurvedic liquorice root extract",
            "Clean glass packaging with wooden dropper cap",
            "Nourishing and barrier-supportive",
            "Certified cruelty-free and vegan",
        ],
    },
    {
        "sku": "PS-SALI100",
        "name": "PureSkin Willow Bark Natural Salicylic Cleanser 100ml",
        "brand": "PureSkin",
        "price": 549,
        "rating": 3.9,
        "marketplace": "Blinkit",
        "category": "Cleanser",
        "features": [
            "Natural BHA from Organic Willow Bark",
            "Neem and holy basil (Tulsi) extracts",
            "Mild jelly texture cleanser",
            "Post-consumer recycled bottle packaging",
            "Ayush certified formulation",
        ],
    },
]

ALL_PRODUCTS = GLOWSKIN_PRODUCTS + DERMACARE_PRODUCTS + PURESKIN_PRODUCTS


# ═══════════════════════════════════════════════════════════════
# 2. REVIEW TEMPLATES (EXPANDED TO COVER ALL CATEGORIES)
# ═══════════════════════════════════════════════════════════════

_CITIES = [
    "Bengaluru", "Mumbai", "Delhi NCR", "Pune", "Hyderabad",
    "Chennai", "Kolkata", "Ahmedabad", "Jaipur", "Chandigarh"
]

_MARKETPLACES = ["Amazon", "Flipkart", "Nykaa", "Blinkit", "GlowSkin Direct"]
_MARKETPLACE_WEIGHTS = [0.55, 0.20, 0.15, 0.06, 0.04]

# ── Vitamin C Templates ───────────────────────────────────────
_VITC_POSITIVE = [
    "Amazing serum! My skin looks visibly brighter after just 2 weeks of use.",
    "Love the lightweight texture. Absorbs quickly without any sticky residue.",
    "Great value for the price. Better than many premium brands I've tried.",
    "My dark spots have noticeably faded. Will definitely repurchase.",
    "The dropper design makes it easy to control the amount. Very hygienic.",
    "Dermatologist recommended this to me and I'm so glad I tried it.",
    "Gives a natural glow to my skin. I've received so many compliments.",
    "Non-irritating formula even for my sensitive skin. Very gentle.",
    "The vitamin C concentration is perfect - effective without causing redness.",
    "My morning skincare routine is incomplete without this serum now.",
    "Excellent for anti-aging. Fine lines around my eyes have reduced.",
    "The glass bottle keeps the formula fresh and potent for longer.",
    "Fast delivery and well-packaged. The product arrived in perfect condition.",
    "I've been using this for 3 months and the results are remarkable.",
    "Great for combination skin. Doesn't make my T-zone oily at all.",
    "The formula is stable and doesn't oxidize quickly like other vitamin C serums.",
    "Perfect for Indian climate. Light enough for hot and humid weather.",
    "Best vitamin C serum in this price range. I've tried at least 5 others.",
    "As a 45-year-old with mature skin, this serum has genuinely reversed some sun damage.",
    "Customer service was phenomenal — they replaced a damaged bottle within 3 days.",
    "I compared this side-by-side with DermaCare's serum and GlowSkin wins on texture.",
    "Wedding prep essential! My bridal glow was 100% thanks to this serum.",
    "Survived monsoon season without oxidizing. Impressive stability.",
    "Applied it before my Haldi ceremony and my skin was glowing in all photos.",
    "My pigmentation from PCOD has visibly reduced after 8 weeks.",
    "Works great under mineral sunscreen. No pilling or white cast issues.",
    "Refilled for the 4th time. Consistent quality across batches.",
    "Better absorption than Minimalist and Plum vitamin C serums I've tried.",
]

_VITC_NEUTRAL = [
    "Decent product but nothing extraordinary. Does what it says.",
    "Good serum but takes about 4-6 weeks to see visible results.",
    "The texture is fine but I wish it came in a bigger bottle.",
    "Works okay for brightening but I expected faster results.",
    "It's an average vitamin C serum. Nothing special but nothing bad either.",
    "The price is fair but competitors offer more quantity for similar price.",
    "Mild improvement in skin tone. Not as dramatic as I hoped.",
    "The dropper sometimes gets stuck. Minor inconvenience.",
    "Packaging could be improved. The box arrived slightly damaged.",
]

_VITC_NEGATIVE = [
    "Product oxidized within 2 weeks of opening. Turned dark yellow color.",
    "Caused breakouts on my cheeks. Had to stop using after 5 days.",
    "The serum feels watery and thin. Doesn't feel premium for the price.",
    "No visible difference even after using for 6 weeks consistently.",
    "Received an expired product. Very disappointed with quality control.",
    "The glass dropper broke during transit. Poor packaging.",
    "Irritated my skin badly. Red patches appeared after first application.",
    "The consistency changed after 3 weeks. Became thick and clumpy.",
    "Smells slightly chemical. Not pleasant for daily use.",
    "Price keeps increasing every month. Was ₹699 when I first bought it.",
    "The 30ml runs out too quickly. Need to reorder every 3-4 weeks.",
    "The product leaked inside the package. Messy delivery experience.",
    "DermaCare's serum is cheaper AND more effective. Switching permanently.",
    "The batch I received had a manufacturing date from 8 months ago.",
    "Stings terribly on active acne. Should come with a stronger warning.",
    "The dropper sucks up air bubbles. Hard to get a clean dose.",
    "Tried it during summer in Chennai — the heat destroyed it in 10 days.",
    "Refund process took 3 weeks. Amazon seller support was terrible.",
]

# ── Moisturizer Templates ─────────────────────────────────────
_MOIST_POSITIVE = [
    "Best moisturizer I've ever used! My skin stays hydrated all day.",
    "The airless pump is genius. No contamination and perfect dispensing.",
    "Completely transformed my dry, flaky skin in winter. Life saver!",
    "Fragrance-free is a huge plus for my sensitive, eczema-prone skin.",
    "72-hour hydration claim is actually true. Tested it over a weekend.",
    "The ceramide complex makes a noticeable difference in skin barrier.",
    "Lightweight yet deeply moisturizing. Perfect under makeup.",
    "My skin texture has improved dramatically. Smoother and plumper.",
    "Non-comedogenic formula works great for my acne-prone skin.",
    "The 50ml bottle lasts almost 2 months with daily use. Great value.",
    "My dermatologist approved this for my rosacea-prone skin.",
    "The triple hyaluronic acid technology is superior to single-weight alternatives.",
    "No white cast or pilling under sunscreen. Smooth base for SPF.",
    "The pump dispenses the perfect amount every time.",
]

_MOIST_NEUTRAL = [
    "Good moisturizer but the price is a bit high for the quantity.",
    "Does the job but I've seen similar results from cheaper alternatives.",
    "Packaging is nice but the pump mechanism could be smoother.",
    "Hydrates well but doesn't do much for anti-aging as claimed.",
    "Works better in winter than summer. Too heavy for humid climate.",
    "The texture is a bit thick for morning use. Better as night cream.",
]

_MOIST_NEGATIVE = [
    "Made my skin feel greasy and clogged my pores within a week.",
    "Developed small bumps after using for 10 days. Had to discontinue.",
    "The 50ml feels inadequate for the price. Should be at least 75ml.",
    "The pump stopped working after 2 weeks. Had to pry it open.",
    "Caused white heads on my forehead. Not suitable for oily skin despite claims.",
    "Received a product that was manufactured over a year ago.",
]

# ── Retinol Night Cream Templates ─────────────────────────────
_RETINOL_POSITIVE = [
    "My wrinkles have visibly reduced after 6 weeks of consistent use.",
    "The encapsulated retinol is gentle enough for retinol beginners.",
    "Night repair formula actually works. My skin looks refreshed every morning.",
    "Love the combination with niacinamide. Reduces irritation potential.",
    "My skin texture has completely changed. From rough to smooth.",
    "Perfect starter retinol. No peeling or excessive dryness.",
    "The peptide complex adds extra anti-aging benefits. Multi-functional.",
    "Absorbed quickly and didn't stain my pillow. Clean formula.",
    "After 3 months, my skin age assessment improved noticeably!",
    "The 0.5% concentration is medically sound for daily use. Well formulated.",
]

_RETINOL_NEUTRAL = [
    "Decent retinol cream but the 15ml is gone too quickly.",
    "Results are there but very gradual. Need patience with this one.",
    "The jar packaging is not the most hygienic. A pump would be better.",
    "Good product but the price per ml is very high compared to competitors.",
    "The texture is a bit heavy for Indian summers. Better for winter use.",
]

_RETINOL_NEGATIVE = [
    "Severe peeling and redness within first week. Way too strong for sensitive skin.",
    "₹1,499 for 15ml is daylight robbery. DermaCare offers 20ml for less.",
    "The jar design lets air in, which degrades retinol. Poor packaging choice.",
    "My skin purged badly and the breakouts lasted for 3 weeks.",
    "No visible anti-aging results even after 8 weeks of nightly use.",
    "The cream pills under my night moisturizer. Doesn't layer well.",
    "Gave me contact dermatitis. Had to see a doctor and use steroids.",
    "Inconsistent texture between batches. My second jar was much thinner.",
    "15ml runs out in 2-3 weeks with recommended amount. Expensive habit.",
    "Product arrived without a seal. Concerned about contamination.",
    "Customer service didn't acknowledge my skin reaction complaint.",
]

# ── Sunscreen Templates ───────────────────────────────────────
_SUN_POSITIVE = [
    "Absolute holy grail sunscreen! ZERO white cast on dusky Indian skin.",
    "The ultra-matte finish stays completely shine-free even during 38°C Delhi heat.",
    "Doesn't sting my eyes at all when sweating during workouts. Huge win!",
    "Layers like a dream under foundation. Works as a mattifying makeup primer.",
    "Cica and niacinamide really soothe sun redness after being outdoors.",
    "Sweat resistant claim is true — wore it for outdoor badminton and no smudging.",
    "Finally a sunscreen that doesn't trigger cystic acne on my oily T-zone.",
    "Light silicone gel feel without feeling suffocating on humid Mumbai days.",
    "The pump tube makes it so hygienic and travel friendly. Never leaks in bag.",
    "Reapplied twice during my Goa vacation and didn't get any sunburn or tan.",
]

_SUN_NEUTRAL = [
    "Decent matte finish but takes about 5 minutes to settle down.",
    "Good sun protection but wish it came in an economical 100g size.",
    "Has a faint silicone texture that takes getting used to.",
    "A bit drying if you have dry skin patches. Must apply moisturizer first.",
    "Slightly expensive at ₹699 for 50g compared to drugstore sunscreens.",
]

_SUN_NEGATIVE = [
    "Pills terribly if you layer it over a thick hyaluronic acid serum.",
    "The pump dispenser gets stuck when the bottle is 30% empty.",
    "Not completely water-resistant — washed off quickly during pool swimming.",
    "Left a slight greasy sheen on my super oily skin after 3 hours.",
    "DermaCare's SPF 50 is ₹50 cheaper and gives a more natural finish.",
    "Received a batch with oil separation — had to shake vigorously every time.",
    "Small tube runs out in 3 weeks if you apply the recommended 2-finger rule.",
]

# ── Niacinamide Serum Templates ───────────────────────────────
_NIAC_POSITIVE = [
    "Faded my stubborn post-acne dark spots in under a month. Super effective!",
    "Controls midday forehead oiliness better than The Ordinary's niacinamide.",
    "The watery texture absorbs in 10 seconds with zero stickiness.",
    "My enlarged nose pores look visibly tighter and cleaner.",
    "Zinc PCA keeps angry pimples from growing. Great formulation balance.",
    "Non-irritating even when used twice daily. Clean and fragrance free.",
    "Pairs perfectly with hyaluronic acid moisturizer in the evening.",
    "Refilled twice already. Best Indian formulated niacinamide serum.",
    "Visible reduction in skin redness and barrier sensitivity.",
]

_NIAC_NEUTRAL = [
    "Works well for oil control but took 8 weeks to see any spot fading.",
    "Good serum but the dropper dispenses a bit too fast.",
    "Average results on deep pigmentation, but excellent for skin texture.",
    "Slight tingling sensation for the first 3 days then settled down.",
]

_NIAC_NEGATIVE = [
    "Caused mild purging breakouts around my jawline for 2 weeks.",
    "The dropper cap arrived loose and 20% of serum leaked in the parcel box.",
    "Felt slightly sticky on humid monsoon days. Not completely weightless.",
    "Didn't do anything for hormonal cystic acne as claimed by influencers.",
    "DermaCare's cica niacinamide is ₹50 cheaper with a calibrated dropper.",
]

# ── Salicylic Cleanser Templates ──────────────────────────────
_SALI_POSITIVE = [
    "Completely cleared my recurring blackheads on nose and chin in 3 weeks.",
    "Gentle foaming that doesn't strip or leave skin feeling squeaky tight.",
    "Sulphate-free formula is refreshing. Tea tree scent is subtle and natural.",
    "Controls breakout frequency significantly when used every morning.",
    "Great pH balance at 5.5. Doesn't compromise my sensitive skin barrier.",
    "Removes excess oil and pollution without needing a second cleanse.",
]

_SALI_NEUTRAL = [
    "Good everyday face wash for acne skin, but doesn't lather very richly.",
    "Needs to be left on the skin for 60 seconds to let salicylic acid work.",
    "Effective on oily areas but slightly drying on cheek areas in winter.",
    "Average acne cleanser. Works similarly to drugstore salicylic washes.",
]

_SALI_NEGATIVE = [
    "The pump dispenser broke after 2 weeks! Very poor packaging quality.",
    "The bottle leaked all over my gym bag because the pump has no twist lock.",
    "High return rate is justified — third time I'm receiving a leaking bottle!",
    "Dried out my skin terribly and caused peeling around the mouth.",
    "DermaCare's face wash has a twist-lock pump and costs ₹50 less.",
    "Smells too medicinal like cough syrup. Not an enjoyable cleansing experience.",
]

# ── Competitor Review Templates ───────────────────────────────
_DC_REVIEWS = [
    "DermaCare's active concentrations are clinical grade and very stable.",
    "Their twist-lock leak-proof pumps are much better than GlowSkin's packaging.",
    "DermaCare is generally ₹50 to ₹100 cheaper across all comparable serums.",
    "Clinical study results posted on their website give high transparency.",
    "The SPF 50 from DermaCare has higher German UV filters. Great protection.",
    "DermaCare retinol uses a hygienic pump instead of GlowSkin's unhygienic jar.",
    "ISO certified labs and 2-year warranty on efficacy build massive trust.",
    "DermaCare customer service replaced a damaged order within 48 hours.",
    "Slightly medicinal packaging look, but performance is unbeatable for price.",
    "Their 10% niacinamide with cica cured my redness faster than GlowSkin.",
]

_PS_REVIEWS = [
    "PureSkin's 100% organic certification is great for clean beauty lovers.",
    "Love their recycled glass and biodegradable packaging initiatives.",
    "Plant-based alternatives are much milder and gentler on sensitive skin.",
    "PureSkin products take longer to show visible results compared to chemical actives.",
    "PureSkin mineral sunscreen has a slight tint that blends naturally on warm skin.",
    "Very premium aesthetic with wooden caps and amber bottles.",
    "Higher price point across all products because of certified organic sourcing.",
    "PureSkin willow bark cleanser is very gentle but doesn't foam much.",
    "Great community and transparent farm-to-bottle sourcing journey.",
]


def _build_review(brand: str, sku: str, text: str, rating: int) -> dict:
    """Build a single realistic review dict with diverse marketplace and geo metadata."""
    days_ago = random.randint(1, 120)
    review_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    marketplace = random.choices(_MARKETPLACES, weights=_MARKETPLACE_WEIGHTS)[0]
    city = random.choice(_CITIES)

    return {
        "brand": brand,
        "sku": sku,
        "rating": rating,
        "review_text": text,
        "marketplace": marketplace,
        "city": city,
        "date": review_date,
        "verified_purchase": random.random() > 0.12,
        "helpful_votes": random.choices([0, 1, 2, 5, 12, 28], weights=[0.5, 0.25, 0.12, 0.08, 0.03, 0.02])[0],
    }


def generate_reviews() -> list[dict]:
    """
    Generate 140-175 reviews per product across 18 products.
    Yields ~2,800+ realistic, diverse reviews with accurate sentiment distributions.
    """
    all_reviews = []
    random.seed(42)  # Reproducible across restarts

    def _generate_for_sku(brand, sku, positive, neutral, negative, target_rating):
        reviews = []
        count = random.randint(145, 175)

        if target_rating >= 4.4:
            dist = {"5": 0.50, "4": 0.28, "3": 0.12, "2": 0.06, "1": 0.04}
        elif target_rating >= 4.2:
            dist = {"5": 0.38, "4": 0.32, "3": 0.15, "2": 0.09, "1": 0.06}
        elif target_rating >= 4.0:
            dist = {"5": 0.28, "4": 0.30, "3": 0.22, "2": 0.12, "1": 0.08}
        else:
            dist = {"5": 0.20, "4": 0.24, "3": 0.22, "2": 0.18, "1": 0.16}

        for _ in range(count):
            r = random.random()
            if r < dist["5"]:
                rating = 5
                pool = positive
            elif r < dist["5"] + dist["4"]:
                rating = 4
                pool = positive + neutral
            elif r < dist["5"] + dist["4"] + dist["3"]:
                rating = 3
                pool = neutral
            elif r < dist["5"] + dist["4"] + dist["3"] + dist["2"]:
                rating = 2
                pool = negative + neutral
            else:
                rating = 1
                pool = negative

            text = random.choice(pool)
            reviews.append(_build_review(brand, sku, text, rating))

        return reviews

    # 1. GlowSkin Reviews (6 SKUs)
    all_reviews += _generate_for_sku("GlowSkin", "VITC30", _VITC_POSITIVE, _VITC_NEUTRAL, _VITC_NEGATIVE, 4.2)
    all_reviews += _generate_for_sku("GlowSkin", "HYALU50", _MOIST_POSITIVE, _MOIST_NEUTRAL, _MOIST_NEGATIVE, 4.5)
    all_reviews += _generate_for_sku("GlowSkin", "RETA15", _RETINOL_POSITIVE, _RETINOL_NEUTRAL, _RETINOL_NEGATIVE, 3.8)
    all_reviews += _generate_for_sku("GlowSkin", "SUN50", _SUN_POSITIVE, _SUN_NEUTRAL, _SUN_NEGATIVE, 4.3)
    all_reviews += _generate_for_sku("GlowSkin", "NIAC10", _NIAC_POSITIVE, _NIAC_NEUTRAL, _NIAC_NEGATIVE, 4.4)
    all_reviews += _generate_for_sku("GlowSkin", "SALI100", _SALI_POSITIVE, _SALI_NEUTRAL, _SALI_NEGATIVE, 4.1)

    # 2. DermaCare Reviews (6 SKUs)
    all_reviews += _generate_for_sku("DermaCare", "DC-VITC25", _DC_REVIEWS[:5] + _VITC_POSITIVE[:10], _VITC_NEUTRAL, _VITC_NEGATIVE[:5], 4.4)
    all_reviews += _generate_for_sku("DermaCare", "DC-MOIST60", _DC_REVIEWS[1:6] + _MOIST_POSITIVE[:10], _MOIST_NEUTRAL, _MOIST_NEGATIVE[:4], 4.3)
    all_reviews += _generate_for_sku("DermaCare", "DC-RETIN20", _DC_REVIEWS[5:9] + _RETINOL_POSITIVE[:10], _RETINOL_NEUTRAL, _RETINOL_NEGATIVE[:5], 4.1)
    all_reviews += _generate_for_sku("DermaCare", "DC-SUN50", _DC_REVIEWS[4:8] + _SUN_POSITIVE[:10], _SUN_NEUTRAL, _SUN_NEGATIVE[:4], 4.5)
    all_reviews += _generate_for_sku("DermaCare", "DC-NIAC10", _DC_REVIEWS[8:10] + _NIAC_POSITIVE[:10], _NIAC_NEUTRAL, _NIAC_NEGATIVE[:4], 4.3)
    all_reviews += _generate_for_sku("DermaCare", "DC-SALI100", _DC_REVIEWS[1:4] + _SALI_POSITIVE[:10], _SALI_NEUTRAL, _SALI_NEGATIVE[:4], 4.4)

    # 3. PureSkin Reviews (6 SKUs)
    all_reviews += _generate_for_sku("PureSkin", "PS-VITCR30", _PS_REVIEWS[:5] + _VITC_POSITIVE[:8], _VITC_NEUTRAL, _VITC_NEGATIVE[:6], 4.0)
    all_reviews += _generate_for_sku("PureSkin", "PS-HYDRA45", _PS_REVIEWS[1:6] + _MOIST_POSITIVE[:8], _MOIST_NEUTRAL, _MOIST_NEGATIVE[:5], 4.2)
    all_reviews += _generate_for_sku("PureSkin", "PS-RETSERUM", _PS_REVIEWS[3:7] + _RETINOL_POSITIVE[:8], _RETINOL_NEUTRAL, _RETINOL_NEGATIVE[:6], 3.9)
    all_reviews += _generate_for_sku("PureSkin", "PS-SUN50", _PS_REVIEWS[4:8] + _SUN_POSITIVE[:8], _SUN_NEUTRAL, _SUN_NEGATIVE[:5], 4.1)
    all_reviews += _generate_for_sku("PureSkin", "PS-NIAC10", _PS_REVIEWS[2:7] + _NIAC_POSITIVE[:8], _NIAC_NEUTRAL, _NIAC_NEGATIVE[:5], 4.2)
    all_reviews += _generate_for_sku("PureSkin", "PS-SALI100", _PS_REVIEWS[6:9] + _SALI_POSITIVE[:8], _SALI_NEUTRAL, _SALI_NEGATIVE[:6], 3.9)

    return all_reviews


# ═══════════════════════════════════════════════════════════════
# 3. HELPER LOOKUPS
# ═══════════════════════════════════════════════════════════════

def get_product_by_sku(sku: str) -> dict | None:
    """Look up a product by SKU."""
    for p in ALL_PRODUCTS:
        if p["sku"].upper() == sku.upper():
            return p
    return None


def get_brand_products(brand: str) -> list[dict]:
    """Get all products for a brand."""
    return [p for p in ALL_PRODUCTS if p["brand"].lower() == brand.lower()]


def get_glowskin_skus() -> list[str]:
    """Return GlowSkin SKU codes."""
    return [p["sku"] for p in GLOWSKIN_PRODUCTS]


def get_competitor_features() -> list[dict]:
    """Return competitor feature descriptions for vector embedding."""
    features = []
    for product in DERMACARE_PRODUCTS + PURESKIN_PRODUCTS:
        features.append({
            "brand": product["brand"],
            "sku": product["sku"],
            "name": product["name"],
            "price": product["price"],
            "rating": product["rating"],
            "category": product["category"],
            "features_text": f"{product['brand']} {product['name']} (Category: {product['category']}) — Features: {', '.join(product['features'])}. Price: ₹{product['price']}. Rating: {product['rating']}★",
        })
    return features
