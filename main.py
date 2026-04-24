# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 18:22:45 2026

@author: jobin
"""

import nest_asyncio
nest_asyncio.apply()

import random
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="FitBot Editorial Engine V10")

class UserData(BaseModel):
    shoulders: float
    chest: float
    waist: float
    hips: float
    gender: str
    style_pref: str

class SurveyData(BaseModel):
    gender: str
    build: str
    waist_shape: str
    style_pref: str

# --- THE NIFT VETTED EDITORIAL DIRECTORY ---
# Each outfit is selected for its technical ability to balance body ratios.
WARDROBE = {
    "Inverted Triangle": { # Broad shoulders -> Needs volume at hips
        "Male": {
            "Minimalist": [{"top": "Soft Knit Polo", "bottom": "Wide-leg Tailored Trousers", "t": "https://images.unsplash.com/photo-1617137968427-85924c800a22?w=600", "b": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=600"}],
            "Streetwear": [{"top": "Oversized Denim Jacket", "bottom": "Extreme Wide Cargoes", "t": "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=600", "b": "https://images.unsplash.com/photo-1620794341491-76be6eeb6946?w=600"}],
            "Formal": [{"top": "Slim-Fit Double Breasted Blazer", "bottom": "Straight Wool Slacks", "t": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=600", "b": "https://images.unsplash.com/photo-1598136490941-30d885318abd?w=600"}]
        },
        "Female": {
            "Formal": [{"top": "Halter Style Bodysuit", "bottom": "Full Pleated A-line Skirt", "t": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=600", "b": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=600"}],
            "Streetwear": [{"top": "Deep V-neck Tank", "bottom": "High-waist Baggy Denim", "t": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600", "b": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=600"}]
        }
    },
    "Pear": { # Broad hips -> Needs volume at shoulders
        "Male": {
            "Minimalist": [{"top": "Padded Shoulder Harrington", "bottom": "Dark Straight Chinos", "t": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600", "b": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=600"}],
            "Formal": [{"top": "Broad Peak Lapel Suit Jacket", "bottom": "Straight Dress Pants", "t": "https://images.unsplash.com/photo-1534030347209-467a5b0ad3e6?w=600", "b": "https://images.unsplash.com/photo-1598136490941-30d885318abd?w=600"}]
        },
        "Female": {
            "Minimalist": [{"top": "Boat-neck Striped Sweater", "bottom": "Vertical Stripe Slacks", "t": "https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=600", "b": "https://images.unsplash.com/photo-1509551383277-7507e541adbb?w=600"}],
            "Formal": [{"top": "Structured Shoulder Cape Blouse", "bottom": "Tailored High-waist Palazzo", "t": "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=600", "b": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=600"}]
        }
    },
    "Rectangle": { # Balanced but straight -> Needs focal points
        "Female": {
            "Streetwear": [{"top": "Cropped Oversized Bomber", "bottom": "Paper-bag Waist Pants", "t": "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=600", "b": "https://images.unsplash.com/photo-1517423738875-5ce310acd3da?w=600"}],
            "Formal": [{"top": "Peplum Blazer", "bottom": "Tulip Skirt", "t": "https://images.unsplash.com/photo-1548142813-c348350df52b?w=600", "b": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=600"}]
        }
    }
}

def calculate_shape(s, h):
    if h == 0: h = 1
    # Shoulder-to-Hip Ratio
    ratio = s / h
    if ratio > 1.07: return "Inverted Triangle"
    elif ratio < 0.93: return "Pear"
    else: return "Rectangle"

@app.post("/get_outfit/")
async def measurement_logic(user: UserData):
    shape = calculate_shape(user.shoulders, user.hips)
    # Deep dive into vetted directory
    shape_group = WARDROBE.get(shape, WARDROBE["Rectangle"])
    gender_group = shape_group.get(user.gender, shape_group.get("Male", shape_group["Female"]))
    options = gender_group.get(user.style_pref, list(gender_group.values())[0])
    
    res = random.choice(options)
    return {"shape": shape, "top": res["top"], "bottom": res["bottom"], "t_url": res["t"], "b_url": res["b"]}

@app.post("/get_survey_style/")
async def survey_logic(data: SurveyData):
    s, h = (20, 20)
    if data.build == "Bottom Heavy": s, h = 15, 20
    elif data.build == "Top Heavy": s, h = 20, 15
    shape = calculate_shape(s, h)
    shape_group = WARDROBE.get(shape, WARDROBE["Rectangle"])
    gender_group = shape_group.get(data.gender, shape_group.get("Female", shape_group["Male"]))
    options = gender_group.get(data.style_pref, list(gender_group.values())[0])
    
    res = random.choice(options)
    return {"shape": shape, "top": res["top"], "bottom": res["bottom"], "t_url": res["t"], "b_url": res["b"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)