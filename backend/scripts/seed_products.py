"""
Seed Database with Sample Products

Quick product seeding for POC demo.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.product import Product
from app.config import settings


def seed_products():
    """Seed database with sample products."""
    
    # Create engine and session
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # Sample products
    products = [
        Product(
            id="nike-air-max-90-white",
            gtin="00883419552502",
            mpn="CW2288-111",
            title="Nike Air Max 90",
            description="Nothing as fly, nothing as comfortable, nothing as proven. The Nike Air Max 90 stays true to its OG running roots with the iconic Waffle sole, stitched overlays and classic TPU accents.",
            brand="Nike",
            category="Shoes > Running > Sneakers",
            price=Decimal("120.00"),
            currency="USD",
            images=[
                "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/abc123.jpg"
            ],
            availability="in_stock",
            variants=[
                {"size": "8", "size_system": "US", "gtin": "00883419552502"},
                {"size": "9", "size_system": "US", "gtin": "00883419552503"},
                {"size": "10", "size_system": "US", "gtin": "00883419552504"}
            ],
            product_metadata={"gender": "unisex", "color": "White", "popularity_score": 90}
        ),
        Product(
            id="nike-air-max-270-black",
            gtin="00883419552510",
            mpn="AH8050-002",
            title="Nike Air Max 270",
            description="The Nike Air Max 270 features Nike's biggest heel Air unit yet for a super-soft ride that feels as impossible as it looks.",
            brand="Nike",
            category="Shoes > Lifestyle > Sneakers",
            price=Decimal("150.00"),
            availability="in_stock"
        ),
        Product(
            id="nike-pegasus-40",
            gtin="00883419552520",
            mpn="DV3853-100",
            title="Nike Pegasus 40",
            description="A springy and responsive ride for your daily runs. Responsive cushioning provides a balanced feel for all your miles.",
            brand="Nike",
            category="Shoes > Running > Road Running",
            price=Decimal("140.00"),
            availability="in_stock"
        ),
        Product(
            id="nike-dunk-low-retro",
            gtin="00883419552530",
            mpn="DD1391-100",
            title="Nike Dunk Low Retro",
            description="Created for the hardwood but taken to the streets, the '80s basketball icon returns with classic details and throwback hoops flair.",
            brand="Nike",
            category="Shoes > Lifestyle > Sneakers",
            price=Decimal("110.00"),
            availability="in_stock"
        ),
        Product(
            id="nike-air-force-1-07",
            gtin="00883419552540",
            mpn="CW2288-111",
            title="Nike Air Force 1 '07",
            description="The radiance lives on in the Nike Air Force 1 '07, the basketball original that puts a fresh spin on what you know best.",
            brand="Nike",
            category="Shoes > Lifestyle > Sneakers",
            price=Decimal("115.00"),
            availability="in_stock"
        ),
        Product(
            id="nike-dri-fit-training-shirt",
            gtin="00883419552550",
            mpn="BV6708-010",
            title="Nike Dri-FIT Training Shirt",
            description="Nike Dri-FIT technology moves sweat away from your skin for quicker evaporation, helping you stay dry and comfortable.",
            brand="Nike",
            category="Apparel > Training > Shirts",
            price=Decimal("35.00"),
            availability="in_stock"
        ),
        Product(
            id="nike-sportswear-tech-fleece",
            gtin="00883419552560",
            mpn="CU4489-063",
            title="Nike Sportswear Tech Fleece Hoodie",
            description="Smooth on the outside, brushed soft on the inside, our premium Tech Fleece is a lightweight layer built for warmth.",
            brand="Nike Sportswear",
            category="Apparel > Lifestyle > Hoodies",
            price=Decimal("130.00"),
            availability="in_stock"
        ),
        Product(
            id="nike-pro-365-leggings",
            gtin="00883419552570",
            mpn="DD0252-010",
            title="Nike Pro 365 Women's High-Waisted Leggings",
            description="Made with stretchy, sweat-wicking fabric, the Nike Pro 365 Leggings feel soft and supportive for all your workout needs.",
            brand="Nike",
            category="Apparel > Training > Leggings",
            price=Decimal("50.00"),
            availability="in_stock"
        ),
        Product(
            id="nike-react-infinity-run-4",
            gtin="00883419552580",
            mpn="DR2665-101",
            title="Nike React Infinity Run Flyknit 4",
            description="Designed to help reduce injury and keep you on the run, the Nike React Infinity Run 4 continues to provide a soft and stable ride.",
            brand="Nike",
            category="Shoes > Running > Road Running",
            price=Decimal("160.00"),
            availability="in_stock"
        ),
        Product(
            id="nike-metcon-9",
            gtin="00883419552590",
            mpn="DZ2617-010",
            title="Nike Metcon 9",
            description="Take your training to the next level with the Nike Metcon 9, featuring even more stability and durability for your toughest workouts.",
            brand="Nike",
            category="Shoes > Training > Cross Training",
            price=Decimal("150.00"),
            availability="in_stock"
        ),
    ]
    
    # Add products to database
    for product in products:
        # Check if product already exists
        existing = db.query(Product).filter(Product.id == product.id).first()
        if not existing:
            db.add(product)
            print(f"✅ Added: {product.title}")
        else:
            print(f"⏭️  Skipped (exists): {product.title}")
    
    db.commit()
    print(f"\n✅ Seeding complete! {len(products)} products processed.")
    db.close()


if __name__ == "__main__":
    print("🌱 Seeding database with Nike products...\n")
    seed_products()

