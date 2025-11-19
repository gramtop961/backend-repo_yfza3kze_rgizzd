"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Web3 Token schema for the Token Forge app
class Token(BaseModel):
    """
    Token blueprints created by users before on-chain deployment
    Collection name: "token"
    """
    name: str = Field(..., description="Token name")
    symbol: str = Field(..., min_length=1, max_length=11, description="Ticker symbol")
    decimals: int = Field(18, ge=0, le=18, description="Number of decimals")
    total_supply: float = Field(..., gt=0, description="Total supply in whole tokens")
    chain: str = Field("ethereum", description="Target chain: ethereum, polygon, bsc, solana, etc.")
    description: Optional[str] = Field(None, description="Short description")
    image_url: Optional[str] = Field(None, description="Logo or image URL")
    website: Optional[str] = Field(None, description="Project website")
    twitter: Optional[str] = Field(None, description="Twitter link")
    telegram: Optional[str] = Field(None, description="Telegram link")
    owner_wallet: Optional[str] = Field(None, description="Creator wallet address")
    features: Optional[List[str]] = Field(default_factory=list, description="Selected features e.g., mintable,burnable,pausable")
    deploy_status: str = Field("draft", description="draft | ready | deployed | failed")
    contract_address: Optional[str] = Field(None, description="On-chain contract address once deployed")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
