from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass
from enum import Enum
import asyncio
import base64
import logging
import copy

# ==================== CORE DATA STRUCTURES ====================

@dataclass
class Observation:
    """Structured observation data"""
    timestamp: float
    source: str # 'web' or 'role'
    metadata: Optional[Dict[str, Any]] = None # other metadata
    image: Optional[Union[List[str], str]] = None # base64 encoded image,
    text: Optional[Union[List[str], str]] = None # text content

@dataclass
class Action:
    """Structured action data"""
    content: str
    confidence: float
    source: str  # 'web' or 'role'
    time: float # timestamp in seconds

@dataclass
class Memory:
    """Memory storage for agents"""
    short_term: List[Dict[str, Any]]
    long_term: Dict[str, Any]
    context: Dict[str, Any]
    
    
@dataclass
class Message:
    """Message data"""
    name: str
    content: List[Dict[str, Any]]
    time: float # timestamp in seconds
    


    
    




class PromptingStrategy(Enum):
    """Available prompting strategies"""
    REACT = "react"
    DECOMPOSITION = "decomposition"
    PLANNING = "planning"
    SELF_REFLECTION = "self_reflection"
    DIRECT = "direct"