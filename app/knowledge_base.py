DISEASE_INFO = {
    "background_other": {
        "disease_name": "Non-Plant / Background Object",
        "symptoms": "The uploaded image does not appear to contain a recognized leaf.",
        "immediate_action": "N/A",
        "prevention": "Ensure the leaf is clearly centered and well-lit against a neutral background."
    },
    "pepper_bacterial_spot": {
        "disease_name": "Pepper Bacterial Spot (Xanthomonas spp.)",
        "symptoms": "Small, water-soaked dark spots on leaves that turn brown with yellow halos, leading to leaf drop.",
        "immediate_action": "Prune and destroy infected leaves immediately. Avoid touching healthy plants after handling infected ones.",
        "prevention": "Use certified disease-free seeds, apply copper-based bactericides early in the season, and avoid overhead sprinkler irrigation."
    },
    "pepper_healthy": {
        "disease_name": "Healthy Pepper Leaf",
        "symptoms": "No signs of disease or pest infestation. Vibrant green foliage.",
        "immediate_action": "None required. Maintain current watering and nutrient management schedules.",
        "prevention": "Inspect plants weekly for early signs of pests or spotting and maintain adequate row spacing."
    },
    "potato_early_blight": {
        "disease_name": "Potato Early Blight (Alternaria solani)",
        "symptoms": "Dark brown/black spots with concentric rings ('target board' pattern) on older leaves, causing yellowing and dieback.",
        "immediate_action": "Remove heavily affected lower leaves. Apply approved fungicides such as chlorothalonil or mancozeb.",
        "prevention": "Practice a 2–3 year crop rotation, maintain balanced soil nitrogen levels, and irrigate early in the morning so leaves dry quickly."
    },
    "potato_healthy": {
        "disease_name": "Healthy Potato Leaf",
        "symptoms": "Clean, healthy green foliage with no discoloration or lesions.",
        "immediate_action": "None required.",
        "prevention": "Ensure good soil drainage, avoid over-fertilizing with nitrogen, and monitor for flea beetles or aphids."
    },
    "potato_late_blight": {
        "disease_name": "Potato Late Blight (Phytophthora infestans)",
        "symptoms": "Large, dark green to purplish-black water-soaked lesions that spread rapidly under cool, wet conditions; white fuzzy growth under leaf margins.",
        "immediate_action": "Immediately prune infected stems and dispose of them in sealed bags (do not compost). Apply systemic fungicides like copper hydroxide or metalaxyl.",
        "prevention": "Plant resistant cultivars, destroy volunteer potato plants, avoid excessive leaf wetness, and ensure proper hilling."
    },
    "tomato_early_blight": {
        "disease_name": "Tomato Early Blight (Alternaria solani)",
        "symptoms": "Concentric ring brown spots appearing first on lower leaves, surrounded by yellow tissue.",
        "immediate_action": "Strip off infected lower leaves up to the first fruit cluster. Treat foliage with bio-fungicides or copper sprays.",
        "prevention": "Mulch the soil base to prevent fungal spores from splashing up from the soil during rain; maintain wide spacing for airflow."
    },
    "tomato_healthy": {
        "disease_name": "Healthy Tomato Leaf",
        "symptoms": "Healthy green leaf surface with no spotting, curling, or chlorosis.",
        "immediate_action": "None required.",
        "prevention": "Prune lower suckers for ventilation, stake plants off the soil, and maintain consistent soil moisture."
    },
    "tomato_late_blight": {
        "disease_name": "Tomato Late Blight (Phytophthora infestans)",
        "symptoms": "Irregular pale green to dark brown greasy-looking spots with pale yellow borders; rapid defoliation in humid weather.",
        "immediate_action": "Isolate infected plants. Remove infected branches with disinfected shears and apply copper-based organic fungicides.",
        "prevention": "Avoid working in the garden when foliage is wet. Choose resistant varieties and ensure high sunlight exposure."
    },
    "tomato_septoria_leaf_spot": {
        "disease_name": "Tomato Septoria Leaf Spot (Septoria lycopersici)",
        "symptoms": "Numerous small circular spots with gray-white centers and dark brown margins, often containing tiny black specks.",
        "immediate_action": "Prune affected leaves at ground level. Wash tools with 70% rubbing alcohol between cuts.",
        "prevention": "Keep foliage dry using drip lines or soak hoses, rotate crops every 3 years, and keep the soil covered with clean straw mulch."
    }
}

def get_disease_advice(class_name: str) -> dict:
    return DISEASE_INFO.get(class_name, {
        "disease_name": "Unknown Condition",
        "symptoms": "Information not available for this class.",
        "immediate_action": "Consult a local agricultural extension worker.",
        "prevention": "Practice good crop hygiene."
    })