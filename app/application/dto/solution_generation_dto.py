"""
DTOs для генерации решений (ApplicationSolution)
"""
from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class SolutionDocItemDTO:
    """DTO для документа с замечаниями"""
    title: str
    comment: str
    deadline: str


@dataclass
class SolutionArticleDTO:
    """DTO для статьи (категория документов) с невыполненными требованиями"""
    title: str
    docs: List[SolutionDocItemDTO]


@dataclass
class SolutionCriteriaDTO:
    """DTO для критерия (выполненность требований)"""
    title: str
    description: str
    status: bool


@dataclass
class SolutionDataDTO:
    """DTO для данных решения по заявке"""
    meeting_date: str
    meeting_place: str
    department_name: str
    control_position: str
    control_name: str
    experts: List[str]
    club_fullname: str
    club_shortname: str
    license: str
    season: str
    criteria: List[SolutionCriteriaDTO]
    documents: List[SolutionArticleDTO]
    secretary_name: str
    summary: str
    conclusion: Dict[int, str]
    logo_base64: str
