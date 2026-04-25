# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 18:22:45 2026

@author: jobin
"""

import nest_asyncio
nest_asyncio.apply()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import uvicorn

app = FastAPI(title="FitBot NIFT Backend")

# --- ENABLE CROSS-ORIGIN COMMUNICATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserData(BaseModel):
    shoulders: float
    hips: float
    gender: str = "Female"
    style_pref: str = "Streetwear"

# --- PROFESSIONAL WARDROBE DATABASE ---
WARDROBE = {
    "Inverted Triangle": {
        "Male": [{"top": "Soft Knit Polo", "bottom": "Wide-leg Tailored Trousers", "t": "https://images.unsplash.com/photo-1617137968427-85924c800a22?w=600", "b": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=600"}],
        "Female": [{"top": "Halter Style Bodysuit", "bottom": "Full Pleated A-line Skirt", "t": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=600", "b": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=600"}]
    },
    "Pear": {
        "Male": [{"top": "Padded Shoulder Harrington", "bottom": "Dark Straight Chinos", "t": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600", "b": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=600"}],
        "Female": [{"top": "Structured Shoulder Blouse", "bottom": "High-waist Palazzo", "t": "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=600", "b": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=600"}]
    }
}

@app.post("/get_outfit/")
async def get_outfit(user: UserData):
    # Anthropometric Calculation
    ratio = user.shoulders / (user.hips if user.hips > 0 else 1)
    
    if ratio > 1.07: shape = "Inverted Triangle"
    elif ratio < 0.93: shape = "Pear"
    else: shape = "Rectangle"
    
    # Selection Logic
    group = WARDROBE.get(shape, WARDROBE["Inverted Triangle"])
    gender_group = group.get(user.gender, group["Female"])
    res = random.choice(gender_group)
    
    return {
        "shape": shape,
        "top": res["top"],
        "bottom": res["bottom"],
        "t_url": res["t"],
        "b_url": res["b"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)