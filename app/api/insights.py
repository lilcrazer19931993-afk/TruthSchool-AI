from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import EinsteinInsight, DifficultyLevel
from app.schemas import EinsteinInsightResponse
from datetime import datetime

router = APIRouter()

# Einstein Insights Database
EINSTEIN_INSIGHTS = [
    {
        "topic": "Theory of Relativity",
        "insight": "Space and time are interwoven into a single continuum known as spacetime. The curvature of spacetime is caused by the distribution of mass and energy.",
        "quotes": [
            "Since the mathematicians have invaded the theory of relativity, I do not understand it myself.",
            "I never set out to prove relativity right. I set out to understand the universe."
        ],
        "historical_anecdotes": [
            "Developed Special Relativity in 1905 while working as a patent clerk in Bern, Switzerland",
            "General Relativity was refined during his time in Berlin, 1911-1933"
        ],
        "modern_applications": [
            "GPS satellite systems rely on relativity corrections",
            "Nuclear energy production (E=mc²)",
            "Understanding black holes and neutron stars"
        ],
        "difficulty": "advanced"
    },
    {
        "topic": "Photoelectric Effect",
        "insight": "Light consists of particles (photons) with energy proportional to their frequency. When light hits a material, it can eject electrons.",
        "quotes": [
            "The more success the quantum theory has, the sillier it looks.",
            "God does not play dice with the universe."
        ],
        "historical_anecdotes": [
            "This work won me the Nobel Prize in Physics in 1921",
            "Explained phenomena that classical physics couldn't"
        ],
        "modern_applications": [
            "Solar panels and photovoltaic cells",
            "Image sensors in digital cameras",
            "Photodiodes and phototransistors"
        ],
        "difficulty": "intermediate"
    },
    {
        "topic": "E=mc²: Mass-Energy Equivalence",
        "insight": "Energy and mass are interchangeable. A small amount of mass can be converted into enormous amounts of energy, as shown by this groundbreaking equation.",
        "quotes": [
            "Energy is eternal delight.",
            "The splitting of the atom represents the greatest scientific event of the age."
        ],
        "historical_anecdotes": [
            "Derived from the Special Theory of Relativity",
            "Explains the energy source of the sun and stars",
            "Foundation for understanding nuclear reactions"
        ],
        "modern_applications": [
            "Nuclear power generation",
            "Atomic bombs and nuclear weapons",
            "Medical imaging (PET scans)",
            "Understanding stellar processes"
        ],
        "difficulty": "intermediate"
    },
    {
        "topic": "Quantum Mechanics",
        "insight": "At the atomic scale, particles behave differently than macroscopic objects. Probability and uncertainty are fundamental to reality at quantum scales.",
        "quotes": [
            "God does not play dice.",
            "Quantum mechanics is certainly imposing."
        ],
        "historical_anecdotes": [
            "Contributed to the quantum revolution of the 1920s",
            "Had philosophical disagreements with Niels Bohr",
            "Published the EPR paradox paper in 1935"
        ],
        "modern_applications": [
            "Semiconductors and transistors",
            "Laser technology",
            "Quantum computing",
            "Atomic structure understanding"
        ],
        "difficulty": "expert"
    },
    {
        "topic": "Imagination and Creativity",
        "insight": "Imagination is the foundation of scientific discovery. It allows us to envision possibilities beyond current understanding and drives innovation.",
        "quotes": [
            "Imagination is more important than knowledge. Knowledge is limited; imagination encircles the world.",
            "Life is like riding a bicycle. To keep your balance, you must keep moving.",
            "The true sign of intelligence is not knowledge but imagination."
        ],
        "historical_anecdotes": [
            "Used thought experiments extensively in developing relativity",
            "Imagined riding on a beam of light as a young person",
            "Visualized falling elevators and speeding trains to understand gravity"
        ],
        "modern_applications": [
            "Scientific method and hypothesis formation",
            "Innovation and entrepreneurship",
            "Problem-solving in all fields",
            "Artistic and scientific creativity"
        ],
        "difficulty": "beginner"
    },
    {
        "topic": "Curiosity and Questioning",
        "insight": "The drive to ask questions and seek understanding is the engine of scientific progress. Never stop wondering about how the world works.",
        "quotes": [
            "The important thing is not to stop questioning. Curiosity has its own reason for existing.",
            "I have no special talents. I am only passionately curious.",
            "Wonder is the beginning of wisdom."
        ],
        "historical_anecdotes": [
            "Asked fundamental questions that challenged accepted wisdom",
            "Remained curious about nature throughout his life",
            "Encouraged others to think independently"
        ],
        "modern_applications": [
            "Scientific research and discovery",
            "Educational approaches",
            "Innovation and technology development",
            "Personal growth and learning"
        ],
        "difficulty": "beginner"
    }
]

@router.get("/", response_model=List[EinsteinInsightResponse])
def get_all_insights(
    difficulty: str = None,
    skip: int = 0,
    limit: int = 100
):
    """Get all Einstein insights"""
    insights = EINSTEIN_INSIGHTS
    
    if difficulty:
        insights = [i for i in insights if i.get("difficulty") == difficulty]
    
    return [
        {
            "id": i,
            "topic": insights[i]["topic"],
            "insight": insights[i]["insight"],
            "quotes": insights[i].get("quotes"),
            "historical_anecdotes": insights[i].get("historical_anecdotes"),
            "modern_applications": insights[i].get("modern_applications"),
            "difficulty": insights[i].get("difficulty", "intermediate"),
            "created_at": datetime.utcnow()
        }
        for i in range(min(skip, len(insights)), min(skip + limit, len(insights)))
    ]

@router.get("/{topic}", response_model=EinsteinInsightResponse)
def get_insight_by_topic(topic: str):
    """Get insight by specific topic"""
    for insight in EINSTEIN_INSIGHTS:
        if insight["topic"].lower().replace(" ", "_") == topic.lower().replace(" ", "_"):
            return {
                "id": EINSTEIN_INSIGHTS.index(insight),
                "topic": insight["topic"],
                "insight": insight["insight"],
                "quotes": insight.get("quotes"),
                "historical_anecdotes": insight.get("historical_anecdotes"),
                "modern_applications": insight.get("modern_applications"),
                "difficulty": insight.get("difficulty", "intermediate"),
                "created_at": datetime.utcnow()
            }
    
    raise HTTPException(status_code=404, detail="Insight topic not found")

@router.get("/search/{keyword}")
def search_insights(keyword: str):
    """Search Einstein insights by keyword"""
    keyword_lower = keyword.lower()
    results = []
    
    for i, insight in enumerate(EINSTEIN_INSIGHTS):
        if (keyword_lower in insight["topic"].lower() or
            keyword_lower in insight["insight"].lower() or
            any(keyword_lower in quote.lower() for quote in insight.get("quotes", []))):
            results.append({
                "id": i,
                "topic": insight["topic"],
                "insight": insight["insight"],
                "difficulty": insight.get("difficulty", "intermediate"),
                "match_score": 100 if keyword_lower in insight["topic"].lower() else 75
            })
    
    return {"total": len(results), "results": results}

@router.get("/random/insight")
def get_random_insight():
    """Get a random Einstein insight"""
    import random
    insight = random.choice(EINSTEIN_INSIGHTS)
    idx = EINSTEIN_INSIGHTS.index(insight)
    
    return {
        "id": idx,
        "topic": insight["topic"],
        "insight": insight["insight"],
        "quotes": insight.get("quotes"),
        "historical_anecdotes": insight.get("historical_anecdotes"),
        "modern_applications": insight.get("modern_applications"),
        "difficulty": insight.get("difficulty", "intermediate"),
        "created_at": datetime.utcnow()
    }

@router.get("/daily/wisdom")
def get_daily_wisdom():
    """Get daily wisdom from Einstein"""
    import random
    from datetime import date
    
    random.seed(int(date.today().strftime("%Y%m%d")))
    insight = random.choice(EINSTEIN_INSIGHTS)
    quote = random.choice(insight.get("quotes", ["Imagination is more important than knowledge."]))
    
    return {
        "date": date.today().isoformat(),
        "topic": insight["topic"],
        "quote": quote,
        "thought_for_the_day": insight["insight"],
        "application_tip": random.choice(insight.get("modern_applications", []))
    }

@router.get("/difficulty/{level}", response_model=List[EinsteinInsightResponse])
def get_insights_by_difficulty(level: str):
    """Get insights by difficulty level"""
    insights = [i for i in EINSTEIN_INSIGHTS if i.get("difficulty", "intermediate") == level.lower()]
    
    if not insights:
        raise HTTPException(status_code=404, detail=f"No insights found for difficulty level: {level}")
    
    return [
        {
            "id": EINSTEIN_INSIGHTS.index(i),
            "topic": i["topic"],
            "insight": i["insight"],
            "quotes": i.get("quotes"),
            "historical_anecdotes": i.get("historical_anecdotes"),
            "modern_applications": i.get("modern_applications"),
            "difficulty": i.get("difficulty", "intermediate"),
            "created_at": datetime.utcnow()
        }
        for i in insights
    ]
