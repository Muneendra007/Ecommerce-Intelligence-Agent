"""
Simulated Amazon Marketplace Dataset for GlowSkin D2C Skincare Brand.

Contains:
- Brand: GlowSkin with 3 SKUs
- Competitors: DermaCare (3 SKUs), PureSkin (3 SKUs)
- 80-100 reviews per product
- Monthly sales data (last 3 months)
- Feature lists and pricing
"""

from __future__ import annotations
import random
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════
# PRODUCTS
# ═══════════════════════════════════════════════════════════════

GLOWSKIN_PRODUCTS = [
    {
        "sku": "VITC30",
        "name": "GlowSkin Vitamin C Serum 30ml",
        "brand": "GlowSkin",
        "price": 899,
        "rating": 4.2,
        "marketplace": "Amazon",
        "category": "Skincare",
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
        "category": "Skincare",
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
        "category": "Skincare",
        "features": [
            "0.5% Encapsulated Retinol",
            "Niacinamide + Peptide complex",
            "Night repair formula",
            "Anti-wrinkle and firming",
            "15ml jar packaging",
            "Dermatologist recommended",
        ],
        "sales_data": [
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
]

DERMACARE_PRODUCTS = [
    {
        "sku": "DC-VITC25",
        "name": "DermaCare Vitamin C Glow Serum 25ml",
        "brand": "DermaCare",
        "price": 799,
        "rating": 4.4,
        "marketplace": "Amazon",
        "category": "Skincare",
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
        "category": "Skincare",
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
        "category": "Skincare",
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
]

PURESKIN_PRODUCTS = [
    {
        "sku": "PS-VITCR30",
        "name": "PureSkin Vitamin C Radiance Drops 30ml",
        "brand": "PureSkin",
        "price": 949,
        "rating": 4.0,
        "marketplace": "Amazon",
        "category": "Skincare",
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
        "marketplace": "Amazon",
        "category": "Skincare",
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
        "category": "Skincare",
        "features": [
            "0.3% Pure Retinol",
            "Rosehip oil base",
            "Night use only",
            "20ml dropper bottle",
            "Vegan formula",
        ],
    },
]

ALL_PRODUCTS = GLOWSKIN_PRODUCTS + DERMACARE_PRODUCTS + PURESKIN_PRODUCTS


# ═══════════════════════════════════════════════════════════════
# REVIEWS — 80-100 per product
# ═══════════════════════════════════════════════════════════════

# Review templates organized by sentiment and product type

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
    "My husband also started using this after seeing my results!",
    "The product does what it claims. Honest and effective formulation.",
    # ── Additional diverse reviews ──
    "As a 45-year-old with mature skin, this serum has genuinely reversed some sun damage.",
    "Customer service was phenomenal — they replaced a damaged bottle within 3 days.",
    "I compared this side-by-side with DermaCare's serum and GlowSkin wins on texture.",
    "Wedding prep essential! My bridal glow was 100% thanks to this serum.",
    "Survived monsoon season without oxidizing. Impressive stability.",
    "Applied it before my Haldi ceremony and my skin was glowing in all photos.",
    "I'm a dermatology resident and I recommend this to my patients for brightening.",
    "The pH level is well-balanced — I tested it with strips. Around 3.5 which is ideal.",
    "Pairs beautifully with a niacinamide toner. No irritation at all.",
    "Bought this after seeing a YouTube dermatologist review it. Not disappointed!",
    "My pigmentation from PCOD has visibly reduced after 8 weeks.",
    "Works great under mineral sunscreen. No pilling or white cast issues.",
    "My mom (60+) uses this and her age spots have lightened considerably.",
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
    "Good for beginners but advanced users might want higher concentration.",
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
    "Didn't work for my dark circles at all despite the claims.",
    "My skin felt dry and tight after application. Expected more hydration.",
    "The product leaked inside the package. Messy delivery experience.",
    "Customer service was unhelpful when I reported the quality issue.",
    # ── Additional diverse negative reviews ──
    "DermaCare's serum is cheaper AND more effective. Switching permanently.",
    "The batch I received had a manufacturing date from 8 months ago. Too old for vitamin C.",
    "Stings terribly on active acne. Should come with a stronger warning.",
    "My cousin got the same product but the color was completely different. QC issue?",
    "After price hike to ₹899, the value proposition has completely died.",
    "Instagram influencers hyped this but real results are mediocre at best.",
    "The dropper sucks up air bubbles. Hard to get a clean dose.",
    "Tried it during summer in Chennai — the heat destroyed it in 10 days.",
    "No improvement in my melasma even after 3 months of regular use.",
    "Refund process took 3 weeks. Amazon seller support was terrible.",
    "Compared to The Ordinary's vitamin C, this is overpriced for Indian market.",
    "My teenage daughter got cystic acne from this. Had to visit dermatologist.",
]

_MOIST_POSITIVE = [
    "Best moisturizer I've ever used! My skin stays hydrated all day.",
    "The airless pump is genius. No contamination and perfect dispensing.",
    "Completely transformed my dry, flaky skin in winter. Life saver!",
    "Fragrance-free is a huge plus for my sensitive, eczema-prone skin.",
    "72-hour hydration claim is actually true. Tested it over a weekend.",
    "The ceramide complex makes a noticeable difference in skin barrier.",
    "Lightweight yet deeply moisturizing. Perfect under makeup.",
    "My skin texture has improved dramatically. Smoother and plumper.",
    "Vegan and cruelty-free — aligns with my values. Thank you GlowSkin!",
    "Non-comedogenic formula works great for my acne-prone skin.",
    "The 50ml bottle lasts almost 2 months with daily use. Great value.",
    "Perfect for winter skincare routine. Locks in moisture beautifully.",
    "Clinically tested claim gives me confidence in the product.",
    "My dermatologist approved this for my rosacea-prone skin.",
    "It layers perfectly with my vitamin C serum in the morning.",
    "The triple hyaluronic acid technology is superior to single-weight alternatives.",
    "No white cast or pilling under sunscreen. Smooth base for SPF.",
    "My skin has never looked this healthy. Radiant and supple!",
    "Great for mature skin. My fine lines look less prominent.",
    "The packaging is premium and travel-friendly. Well designed.",
    "My whole family uses this now. Works for all age groups.",
    "Excellent absorption rate. No greasiness at all.",
    "The pump dispenses the perfect amount every time.",
    "Worth every rupee. Planning to try other GlowSkin products too.",
    "My friend is a cosmetician and she recommended this. She was right!",
]

_MOIST_NEUTRAL = [
    "Good moisturizer but the price is a bit high for the quantity.",
    "Does the job but I've seen similar results from cheaper alternatives.",
    "Packaging is nice but the pump mechanism could be smoother.",
    "Hydrates well but doesn't do much for anti-aging as claimed.",
    "Decent product for the price range. Nothing exceptional though.",
    "Took about 3 weeks to see results. Expected faster improvement.",
    "Works better in winter than summer. Too heavy for humid climate.",
    "The texture is a bit thick for morning use. Better as night cream.",
]

_MOIST_NEGATIVE = [
    "Made my skin feel greasy and clogged my pores within a week.",
    "Developed small bumps after using for 10 days. Had to discontinue.",
    "The 50ml feels inadequate for the price. Should be at least 75ml.",
    "Product smells slightly off. Not sure if it's natural or a defect.",
    "Didn't hydrate my extremely dry skin as much as advertised.",
    "The pump stopped working after 2 weeks. Had to pry it open.",
    "Caused white heads on my forehead. Not suitable for oily skin despite claims.",
    "Received a product that was manufactured over a year ago. Worried about freshness.",
]

_RETINOL_POSITIVE = [
    "My wrinkles have visibly reduced after 6 weeks of consistent use.",
    "The encapsulated retinol is gentle enough for retinol beginners.",
    "Night repair formula actually works. My skin looks refreshed every morning.",
    "Love the combination with niacinamide. Reduces irritation potential.",
    "The jar packaging is elegant and the product feels luxurious.",
    "My skin texture has completely changed. From rough to smooth.",
    "Perfect starter retinol. No peeling or excessive dryness.",
    "The peptide complex adds extra anti-aging benefits. Multi-functional.",
    "My fine lines around forehead have diminished noticeably.",
    "Dermatologist recommended this specific product. Very effective.",
    "Absorbed quickly and didn't stain my pillow. Clean formula.",
    "After 3 months, my skin age assessment improved by 5 years!",
    "The 0.5% concentration is medically sound for daily use. Well formulated.",
    "My acne scars have started fading. Dual benefit with retinol.",
]

_RETINOL_NEUTRAL = [
    "Decent retinol cream but the 15ml is gone too quickly.",
    "Results are there but very gradual. Need patience with this one.",
    "The jar packaging is not the most hygienic. A pump would be better.",
    "Good product but the price per ml is very high compared to competitors.",
    "Works for wrinkles but didn't help with my pigmentation issues.",
    "Average retinol product. Expected more given the premium pricing.",
    "The texture is a bit heavy for Indian summers. Better for winter use.",
    "Seen some improvement in skin firmness but fine lines persist.",
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
    "The retinol percentage feels lower than claimed. Minimal efficacy.",
    "15ml runs out in 2-3 weeks with recommended amount. Expensive habit.",
    "Made my skin extremely photosensitive. Got sunburn despite using SPF 50.",
    "Product arrived without a seal. Concerned about contamination.",
    "The niacinamide and retinol combination caused flushing on my skin.",
    "Customer service didn't acknowledge my skin reaction complaint.",
    "Expected clinical-grade results at this price point but was disappointed.",
    "My friend had great results but it absolutely wrecked my skin barrier.",
]

# Competitor reviews — expanded for richer gap analysis

_DC_VITC_REVIEWS = [
    "DermaCare's vitamin C is incredibly stable. No oxidation even after 2 months.",
    "The SPF booster technology is unique. Enhances my sunscreen effectiveness.",
    "ISO certified quality gives me peace of mind. You can feel the difference.",
    "Ferulic acid + Vitamin E combination is science-backed. Great formulation.",
    "Quick absorption is the best feature. No waiting time before makeup.",
    "25ml is slightly less but the higher concentration compensates.",
    "Best stabilized vitamin C in Indian market. No yellowing at all.",
    "The 2-year efficacy warranty is bold and confidence-inspiring.",
    "Works slightly better than GlowSkin's serum in my experience.",
    "Love the dropper precision. Each drop spreads evenly.",
    "Price point is attractive at ₹799. Good entry-level vitamin C.",
    "My dermatologist switched me from GlowSkin to this and I agree.",
    "Slightly drying for very dry skin types. Best for oily/combo.",
    "The texture is thinner than expected. Not as luxurious feeling.",
    "Customer support was responsive when I had a query about ingredients.",
    "Switched from GlowSkin after their price hike. DermaCare is better value.",
    "The Ethyl Ascorbic Acid form is more stable than L-Ascorbic in tropical climate.",
    "Free shipping above ₹500 is a nice touch. GlowSkin charges extra.",
    "Their Instagram has before-after photos from real users. Builds trust.",
    "Comes with a detailed ingredient card. Educational and transparent.",
]

_DC_MOIST_REVIEWS = [
    "Aquaporin technology sounds fancy and actually delivers results.",
    "Oil-free gel cream is perfect for acne-prone Indian skin.",
    "48-hour claim fell short. Needed reapplication by end of day.",
    "The 60ml tube offers better value than many competitors.",
    "Lightweight formula works great under makeup. No pilling.",
    "Aloe vera addition gives a cooling effect. Very soothing.",
    "Missing ceramides compared to GlowSkin. Barrier repair isn't as strong.",
    "Good mid-range moisturizer. Does the job without anything special.",
    "The tube packaging is travel-friendly but not very premium.",
    "Recommended for oily skin. Dry skin folks need something richer.",
    "Their loyalty program gives 10% off on 3rd purchase. Smart retention.",
    "Gel texture is perfect for Bangalore/Mumbai humid weather.",
    "DermaCare ran a Diwali combo deal — moisturizer + serum for ₹1,599. Great deal.",
    "Packaging is minimalist. Less wasteful than GlowSkin's box-in-box.",
]

_DC_RETINOL_REVIEWS = [
    "The 1% retinol is potent. Started with every-other-night application.",
    "Bakuchiol + Squalane makes it gentler than pure retinol alternatives.",
    "Clinical study results are posted on their website. Transparent brand.",
    "20ml for ₹1,399 is fair pricing. Better value than GlowSkin's retinol.",
    "Gradual release technology minimizes irritation. Smart formulation.",
    "Money-back guarantee gave me confidence to try it. No regrets.",
    "Pump bottle is more hygienic than jar. Better packaging design.",
    "My wrinkles improved faster than with GlowSkin's retinol cream.",
    "The squalane prevents the dryness that retinol usually causes.",
    "Suitable for mature skin as advertised. My mother loves it too.",
    "Their dermatologist helpline is free. Called before starting retinol and got great advice.",
    "DermaCare offers a starter kit with low-dose retinol. Wish GlowSkin had that.",
    "Returns are hassle-free. Got full refund when it didn't suit me.",
    "They have a retinol sandwich guide on their website. Helpful for beginners.",
]

_PS_REVIEWS = [
    "PureSkin's organic approach is refreshing but results are slower.",
    "Love that they use recycled packaging. Eco-conscious brand.",
    "Turmeric extract in vitamin C is unique but can stain lighter skin.",
    "Plant-based HA isn't as effective as synthetic forms in my experience.",
    "The brand ethics are amazing. Wish the products were more effective.",
    "100% organic certified is rare in Indian skincare. Appreciated.",
    "Shea butter makes the moisturizer too heavy for summer use.",
    "PureSkin retinol is very mild. Good for absolute beginners.",
    "Rosehip oil base is lovely but the retinol concentration is low.",
    "Premium pricing for organic ingredients. You pay for the ethos.",
    "Eco-friendly packaging is a standout. Reduces guilt while shopping.",
    "The brand story is compelling but products need to match the narrative.",
    "PureSkin has a subscription model with 15% discount. Convenient.",
    "Their social media community is very active and supportive.",
    "Ingredient sourcing is transparent — they share farm-to-face journey.",
    "Won 'Best Sustainable Beauty Brand' at India Beauty Awards. Credible.",
    "The vegan formula is important to me. Only brand I fully trust on this.",
    "Wish they'd offer larger sizes. 30ml goes too fast.",
]


def _build_review(brand: str, sku: str, text: str, rating: int) -> dict:
    """Build a single review dict."""
    return {
        "brand": brand,
        "sku": sku,
        "rating": rating,
        "review_text": text,
        "marketplace": "Amazon",
        "date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
        "verified_purchase": random.random() > 0.15,
    }


def generate_reviews() -> list[dict]:
    """
    Generate 80-100 reviews per product.
    Reviews are drawn from curated templates with realistic rating distributions.
    """
    all_reviews = []
    random.seed(42)  # Reproducible

    def _generate_for_sku(brand, sku, positive, neutral, negative, target_rating):
        """Generate reviews matching a target average rating."""
        reviews = []
        count = random.randint(85, 100)

        # Calculate distribution to match target rating
        if target_rating >= 4.3:
            dist = {"5": 0.40, "4": 0.30, "3": 0.15, "2": 0.10, "1": 0.05}
        elif target_rating >= 4.0:
            dist = {"5": 0.30, "4": 0.30, "3": 0.20, "2": 0.12, "1": 0.08}
        elif target_rating >= 3.8:
            dist = {"5": 0.22, "4": 0.25, "3": 0.23, "2": 0.18, "1": 0.12}
        else:
            dist = {"5": 0.18, "4": 0.22, "3": 0.25, "2": 0.20, "1": 0.15}

        for i in range(count):
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

    # GlowSkin reviews
    all_reviews += _generate_for_sku("GlowSkin", "VITC30", _VITC_POSITIVE, _VITC_NEUTRAL, _VITC_NEGATIVE, 4.2)
    all_reviews += _generate_for_sku("GlowSkin", "HYALU50", _MOIST_POSITIVE, _MOIST_NEUTRAL, _MOIST_NEGATIVE, 4.5)
    all_reviews += _generate_for_sku("GlowSkin", "RETA15", _RETINOL_POSITIVE, _RETINOL_NEUTRAL, _RETINOL_NEGATIVE, 3.8)

    # DermaCare reviews
    all_reviews += _generate_for_sku("DermaCare", "DC-VITC25", _DC_VITC_REVIEWS, _DC_VITC_REVIEWS[8:], _DC_VITC_REVIEWS[12:], 4.4)
    all_reviews += _generate_for_sku("DermaCare", "DC-MOIST60", _DC_MOIST_REVIEWS, _DC_MOIST_REVIEWS[5:], _DC_MOIST_REVIEWS[6:], 4.3)
    all_reviews += _generate_for_sku("DermaCare", "DC-RETIN20", _DC_RETINOL_REVIEWS, _DC_RETINOL_REVIEWS[5:], _DC_RETINOL_REVIEWS[7:], 4.1)

    # PureSkin reviews
    all_reviews += _generate_for_sku("PureSkin", "PS-VITCR30", _PS_REVIEWS, _PS_REVIEWS[4:], _PS_REVIEWS[6:], 4.0)
    all_reviews += _generate_for_sku("PureSkin", "PS-HYDRA45", _PS_REVIEWS[:6], _PS_REVIEWS[4:8], _PS_REVIEWS[6:], 4.2)
    all_reviews += _generate_for_sku("PureSkin", "PS-RETSERUM", _PS_REVIEWS[:4], _PS_REVIEWS[4:8], _PS_REVIEWS[6:], 3.9)

    return all_reviews


def get_product_by_sku(sku: str) -> dict | None:
    """Look up a product by SKU."""
    for p in ALL_PRODUCTS:
        if p["sku"] == sku:
            return p
    return None


def get_brand_products(brand: str) -> list[dict]:
    """Get all products for a brand."""
    return [p for p in ALL_PRODUCTS if p["brand"] == brand]


def get_glowskin_skus() -> list[str]:
    """Return GlowSkin SKU codes."""
    return [p["sku"] for p in GLOWSKIN_PRODUCTS]


def get_competitor_features() -> list[dict]:
    """Return competitor feature descriptions for embedding."""
    features = []
    for product in DERMACARE_PRODUCTS + PURESKIN_PRODUCTS:
        features.append({
            "brand": product["brand"],
            "sku": product["sku"],
            "name": product["name"],
            "price": product["price"],
            "rating": product["rating"],
            "features_text": f"{product['name']} — Features: {', '.join(product['features'])}. Price: ₹{product['price']}. Rating: {product['rating']}★",
        })
    return features
