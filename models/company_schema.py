"""
Pydantic models for company data schema.
Defines the structure for all 163 parameters with proper data types.
"""

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime


class CompanyData(BaseModel):

    
    
    # Company Basics (1-8)
    name: str = Field(..., description="Full legal/official name of the company")
    short_name: Optional[str] = Field(None, description="Commonly used short/abbreviated name")
    logo_url: Optional[str] = Field(None, description="Representative logo URL")
    category: str = Field(..., description="Business classification (Startup, MSME, SMB, etc.)")
    incorporation_year: int = Field(..., description="Year the company was legally incorporated")
    overview_text: str = Field(..., description="High-level summary of what the company does")
    nature_of_company: str = Field(..., description="Ownership structure (Private, Public, etc.)")
    headquarters_address: str = Field(..., description="Primary headquarters address")
    
    # Geographic Presence (9-11)
    operating_countries: Optional[Union[int, str, List[str]]] = Field(None, description="List of countries where company operates")
    office_count: Optional[int] = Field(None, description="Number of additional offices excluding HQ")
    office_locations: Optional[Union[str, List[str]]] = Field(None, description="Specific addresses of all offices")
    
    # People & Talent (12-15)
    employee_size: Union[int, str] = Field(..., description="Total headcount/employee size")
    vision_statement: Optional[str] = Field(None, description="Company's vision statement")
    mission_statement: Optional[str] = Field(None, description="Company's mission statement")
    core_values: Optional[Union[str, List[str]]] = Field(None, description="Company's core values")
    
    # Company Info (16-22)
    history_timeline: Optional[Union[str, List[Dict]]] = Field(None, description="Key milestones in company history")
    recent_news: Optional[Union[str, List[Dict]]] = Field(None, description="Recent news and announcements")
    website_url: Optional[str] = Field(None, description="Official company website")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn company page")
    twitter_handle: Optional[str] = Field(None, description="Twitter/X handle")
    facebook_url: Optional[str] = Field(None, description="Facebook page URL")
    instagram_url: Optional[str] = Field(None, description="Instagram profile URL")
    
    # Contact & Legal (23-31)
    primary_contact_email: Optional[str] = Field(None, description="Primary contact email")
    primary_phone_number: Optional[str] = Field(None, description="Primary phone number")
    regulatory_status: Optional[str] = Field(None, description="Regulatory compliance status")
    legal_issues: Optional[str] = Field(None, description="Ongoing legal issues or controversies")
    esg_ratings: Optional[Union[str, Dict]] = Field(None, description="ESG ratings and scores")
    supply_chain_dependencies: Optional[Union[str, List[str]]] = Field(None, description="Key supply chain dependencies")
    geopolitical_risks: Optional[Union[str, List[str]]] = Field(None, description="Geopolitical risk exposure")
    macro_risks: Optional[Union[str, List[str]]] = Field(None, description="Macroeconomic risk factors")
    carbon_footprint: Optional[Union[int, float, str]] = Field(None, description="Carbon footprint metrics")
    
    # Marketing & Brand (32-40)
    ethical_sourcing: Optional[Union[bool, str]] = Field(None, description="Ethical sourcing practices")
    marketing_video_url: Optional[str] = Field(None, description="Marketing video URL")
    customer_testimonials: Optional[Union[str, List[Dict]]] = Field(None, description="Customer testimonials")
    website_quality: Optional[str] = Field(None, description="Website quality assessment")
    website_rating: Optional[Union[float, str]] = Field(None, description="Website rating score")
    website_traffic_rank: Optional[Union[int, str]] = Field(None, description="Website traffic ranking")
    social_media_followers: Optional[Union[int, str]] = Field(None, description="Social media follower counts")
    glassdoor_rating: Optional[Union[float, str]] = Field(None, description="Glassdoor rating")
    indeed_rating: Optional[Union[float, str]] = Field(None, description="Indeed rating")
    
    # Recognition & Positioning (41-48)
    google_rating: Optional[Union[float, str]] = Field(None, description="Google rating")
    awards_recognitions: Optional[Union[str, List[str], List[Dict]]] = Field(None, description="Awards and recognitions")
    brand_sentiment_score: Optional[Union[int, float, str]] = Field(None, description="Brand sentiment score")
    event_participation: Optional[Union[str, List[str]]] = Field(None, description="Event participation history")
    pain_points_addressed: Union[str, List[str]] = Field(..., description="Customer pain points being addressed")
    focus_sectors: Union[str, List[str]] = Field(..., description="Target industries/sectors")
    offerings_description: str = Field(..., description="Core products, services, offerings")
    top_customers: Optional[Union[str, List[str]]] = Field(None, description="Top customers/clients")
    
    # Value Proposition & Competition (49-57)
    core_value_proposition: Optional[str] = Field(None, description="Core value proposition")
    unique_differentiators: Optional[Union[str, List[str]]] = Field(None, description="Unique differentiators")
    competitive_advantages: Optional[Union[str, List[str]]] = Field(None, description="Competitive advantages")
    weaknesses_gaps: Optional[Union[str, List[str]]] = Field(None, description="Weaknesses and gaps")
    key_challenges_needs: Optional[Union[str, List[str]]] = Field(None, description="Key challenges and needs")
    key_competitors: Optional[Union[str, List[str]]] = Field(None, description="Key competitors")
    market_share_percentage: Optional[Union[int, float, str]] = Field(None, description="Market share percentage")
    sales_motion: Optional[str] = Field(None, description="Sales motion and strategy")
    customer_concentration_risk: Optional[str] = Field(None, description="Customer concentration risk")
    
    # Strategy & Roadmap (58-68)
    exit_strategy_history: Optional[str] = Field(None, description="Exit strategy history")
    benchmark_vs_peers: Optional[Union[str, Dict]] = Field(None, description="Benchmark vs peers")
    future_projections: Optional[Union[str, Dict]] = Field(None, description="Future projections")
    strategic_priorities: Optional[Union[str, List[str]]] = Field(None, description="Strategic priorities")
    industry_associations: Optional[Union[str, List[str]]] = Field(None, description="Industry associations")
    case_studies: Optional[Union[str, List[Dict]]] = Field(None, description="Case studies")
    go_to_market_strategy: Optional[str] = Field(None, description="Go-to-market strategy")
    innovation_roadmap: Optional[Union[str, List[str], Dict]] = Field(None, description="Innovation roadmap")
    product_pipeline: Optional[Union[str, List[str], List[Dict]]] = Field(None, description="Product pipeline")
    tam: Optional[Union[int, float, str]] = Field(None, description="Total Addressable Market")
    sam: Optional[Union[int, float, str]] = Field(None, description="Serviceable Addressable Market")
    
    
    # Market & Operations (69-76)
    som: Optional[Union[int, float, str]] = Field(None, description="Serviceable Obtainable Market")
    leave_policy: Optional[str] = Field(None, description="Leave policy details")
    health_support: Optional[Union[bool, str]] = Field(None, description="Health support programs")
    fixed_vs_variable_pay: Optional[str] = Field(None, description="Fixed vs variable pay ratio")
    bonus_predictability: Optional[str] = Field(None, description="Bonus predictability")
    esops_incentives: Optional[Union[bool, str]] = Field(None, description="ESOPs and long-term incentives")
    family_health_insurance: Optional[Union[bool, str]] = Field(None, description="Family health insurance coverage")
    relocation_support: Optional[Union[bool, str]] = Field(None, description="Relocation support")
    
    # HR & Culture (77-89)
    lifestyle_benefits: Optional[Union[str, List[str]]] = Field(None, description="Lifestyle and wellness benefits")
    hiring_velocity: Optional[str] = Field(None, description="Current hiring velocity")
    employee_turnover: Optional[Union[int, float, str]] = Field(None, description="Annual employee turnover rate")
    avg_retention_tenure: Optional[Union[int, float, str]] = Field(None, description="Average retention tenure")
    diversity_metrics: Optional[Union[str, Dict]] = Field(None, description="Diversity metrics")
    work_culture_summary: Optional[str] = Field(None, description="Work culture summary")
    manager_quality: Optional[str] = Field(None, description="Manager quality assessment")
    psychological_safety: Optional[str] = Field(None, description="Psychological safety score")
    feedback_culture: Optional[str] = Field(None, description="Feedback culture")
    diversity_inclusion_score: Optional[Union[int, float, str]] = Field(None, description="Diversity & inclusion score")
    ethical_standards: Optional[str] = Field(None, description="Ethical standards")
    burnout_risk: Optional[str] = Field(None, description="Burnout risk assessment")
    layoff_history: Optional[str] = Field(None, description="Layoff history")
    
    # Values & Mission (90-93)
    mission_clarity: Optional[str] = Field(None, description="Mission clarity score")
    sustainability_csr: Optional[str] = Field(None, description="Sustainability and CSR initiatives")
    crisis_behavior: Optional[str] = Field(None, description="Crisis behavior and response")
    
    # Financial Metrics (94-107)
    annual_revenue: Optional[Union[int, float, str]] = Field(None, description="Annual revenue")
    annual_profit: Optional[Union[int, float, str]] = Field(None, description="Annual profit")
    revenue_mix: Optional[Union[str, Dict]] = Field(None, description="Revenue mix breakdown")
    valuation: Optional[Union[int, float, str]] = Field(None, description="Company valuation")
    yoy_growth_rate: Optional[Union[int, float, str]] = Field(None, description="Year-over-year growth rate")
    profitability_status: Optional[str] = Field(None, description="Profitability status")
    key_investors: Optional[Union[str, List[str]]] = Field(None, description="Key investors")
    recent_funding_rounds: Optional[Union[str, List[Dict]]] = Field(None, description="Recent funding rounds")
    total_capital_raised: Optional[Union[int, float, str]] = Field(None, description="Total capital raised")
    customer_acquisition_cost: Optional[Union[int, float, str]] = Field(None, description="Customer acquisition cost")
    customer_lifetime_value: Optional[Union[int, float, str]] = Field(None, description="Customer lifetime value")
    cac_ltv_ratio: Optional[Union[float, str]] = Field(None, description="CAC:LTV ratio")
    churn_rate: Optional[Union[int, float, str]] = Field(None, description="Customer churn rate")
    net_promoter_score: Optional[Union[int, float, str]] = Field(None, description="Net Promoter Score")
    
    # Financial Health (108-111)
    burn_rate: Optional[Union[int, float, str]] = Field(None, description="Monthly burn rate")
    runway_months: Optional[Union[int, float, str]] = Field(None, description="Runway in months")
    burn_multiplier: Optional[Union[int, float, str]] = Field(None, description="Burn multiplier")
    
    # Work Environment (112-125)
    remote_policy_details: Optional[str] = Field(None, description="Remote work policy details")
    typical_hours: Optional[Union[int, str]] = Field(None, description="Typical working hours")
    overtime_expectations: Optional[str] = Field(None, description="Overtime expectations")
    weekend_work: Optional[str] = Field(None, description="Weekend work requirements")
    flexibility_level: Optional[str] = Field(None, description="Work flexibility level")
    location_centrality: Optional[str] = Field(None, description="Office location centrality")
    public_transport_access: Optional[str] = Field(None, description="Public transport access")
    cab_policy: Optional[str] = Field(None, description="Cab/transportation policy")
    airport_commute_time: Optional[Union[int, str]] = Field(None, description="Airport commute time")
    office_zone_type: Optional[str] = Field(None, description="Office zone type")
    area_safety: Optional[str] = Field(None, description="Area safety assessment")
    safety_policies: Optional[str] = Field(None, description="Safety policies")
    infrastructure_safety: Optional[str] = Field(None, description="Infrastructure safety")
    emergency_preparedness: Optional[str] = Field(None, description="Emergency preparedness")
    
    # Leadership (126-133)
    ceo_name: Optional[str] = Field(None, description="CEO name")
    ceo_linkedin_url: Optional[str] = Field(None, description="CEO LinkedIn URL")
    key_leaders: Optional[Union[str, List[str], List[Dict]]] = Field(None, description="Key leaders")
    warm_intro_pathways: Optional[Union[str, List[str]]] = Field(None, description="Warm intro pathways")
    decision_maker_access: Optional[str] = Field(None, description="Decision maker access")
    contact_person_name: Optional[str] = Field(None, description="Contact person name")
    contact_person_title: Optional[str] = Field(None, description="Contact person title")
    contact_person_email: Optional[str] = Field(None, description="Contact person email")
    
    # Governance (134-143)
    contact_person_phone: Optional[str] = Field(None, description="Contact person phone")
    board_members: Optional[Union[str, List[str], List[Dict]]] = Field(None, description="Board members")
    training_spend: Optional[Union[int, float, str]] = Field(None, description="Training spend")
    onboarding_quality: Optional[str] = Field(None, description="Onboarding quality")
    learning_culture: Optional[str] = Field(None, description="Learning culture")
    exposure_quality: Optional[str] = Field(None, description="Exposure quality")
    mentorship_availability: Optional[str] = Field(None, description="Mentorship availability")
    internal_mobility: Optional[str] = Field(None, description="Internal mobility")
    promotion_clarity: Optional[str] = Field(None, description="Promotion clarity")
    tools_access: Optional[str] = Field(None, description="Tools access")
    
    # Role Quality (144-157)
    role_clarity: Optional[str] = Field(None, description="Role clarity")
    early_ownership: Optional[str] = Field(None, description="Early ownership opportunities")
    work_impact: Optional[str] = Field(None, description="Work impact")
    execution_thinking_balance: Optional[str] = Field(None, description="Execution vs thinking balance")
    automation_level: Optional[str] = Field(None, description="Automation level")
    cross_functional_exposure: Optional[str] = Field(None, description="Cross-functional exposure")
    company_maturity: Optional[str] = Field(None, description="Company maturity stage")
    brand_value: Optional[str] = Field(None, description="Brand value")
    client_quality: Optional[str] = Field(None, description="Client quality")
    exit_opportunities: Optional[str] = Field(None, description="Exit opportunities")
    skill_relevance: Optional[str] = Field(None, description="Skill relevance")
    external_recognition: Optional[str] = Field(None, description="External recognition")
    network_strength: Optional[str] = Field(None, description="Network strength")
    global_exposure: Optional[str] = Field(None, description="Global exposure")
    
    # Technology & Innovation (158-163)
    technology_partners: Optional[Union[str, List[str]]] = Field(None, description="Technology partners")
    intellectual_property: Optional[str] = Field(None, description="Intellectual property")
    r_and_d_investment: Optional[Union[int, float, str]] = Field(None, description="R&D investment")
    ai_ml_adoption_level: Optional[str] = Field(None, description="AI/ML adoption level")
    tech_stack: Optional[Union[str, List[str]]] = Field(None, description="Technology stack")
    cybersecurity_posture: Optional[str] = Field(None, description="Cybersecurity posture")
    partnership_ecosystem: Optional[str] = Field(None, description="Partnership ecosystem")
    tech_adoption_rating: Optional[str] = Field(None, description="Tech adoption rating")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Accenture",
                "category": "Enterprise",
                "incorporation_year": 1989,
                "overview_text": "Global professional services company...",
                "nature_of_company": "Public",
                "headquarters_address": "Dublin, Ireland",
                "employee_size": 700000,
                "focus_sectors": ["Technology", "Consulting", "Digital"],
                "offerings_description": "Strategy, Consulting, Technology Services",
                "pain_points_addressed": ["Digital Transformation", "Cloud Migration"]
            }
        }


class ValidationResult(BaseModel):
    """Result of a single validation check."""
    parameter: str
    is_valid: bool
    error_message: Optional[str] = None
    test_case_id: Optional[str] = None
    severity: str = "high"  # high, medium, low


class CompanyDataWithValidation(BaseModel):
    """Company data with validation results."""
    data: CompanyData
    validation_results: List[ValidationResult] = []
    is_valid: bool = True
    regeneration_count: int = 0
    
    def add_validation_result(self, result: ValidationResult):
        """Add a validation result and update overall validity."""
        self.validation_results.append(result)
        if not result.is_valid:
            self.is_valid = False
    
    def get_failed_parameters(self) -> List[str]:
        """Get list of parameters that failed validation."""
        return [r.parameter for r in self.validation_results if not r.is_valid]