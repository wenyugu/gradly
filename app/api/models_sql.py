import enum

from typing import List


class DegreeType(enum.Enum):
    associates = 'associate'
    bachelors = 'bachelor'
    masters = 'master'
    phd = 'phd'


class JobType(enum.Enum):
    intern = 'intern'
    research = 'research'
    co_op = 'co-op'
    part_time = 'part-time'
    full_time = 'full-time'


class Industry(enum.Enum):
    accounting                            = 'Accounting'
    airlines_aviation                     = 'Airlines/Aviation'
    alternative_dispute_resolution        = 'Alternative Dispute Resolution'
    alternative_medicine                  = 'Alternative Medicine'
    animation                             = 'Animation'
    apparel_fashion                       = 'Apparel & Fashion'
    architecture_planning                 = 'Architecture & Planning'
    arts_and_crafts                       = 'Arts and Crafts'
    automotive                            = 'Automotive'
    aviation_aerospace                    = 'Aviation & Aerospace'
    banking                               = 'Banking'
    biotechnology                         = 'Biotechnology'
    broadcast_media                       = 'Broadcast Media'
    building_materials                    = 'Building Materials'
    business_supplies_and_equipment       = 'Business Supplies and Equipment'
    capital_markets                       = 'Capital Markets'
    chemicals                             = 'Chemicals'
    civic_social_organization             = 'Civic & Social Organization'
    civil_engineering                     = 'Civil Engineering'
    commercial_real_estate                = 'Commercial Real Estate'
    computer_network_security             = 'Computer & Network Security'
    computer_games                        = 'Computer Games'
    computer_hardware                     = 'Computer Hardware'
    computer_networking                   = 'Computer Networking'
    computer_software                     = 'Computer Software'
    construction                          = 'Construction'
    consumer_electronics                  = 'Consumer Electronics'
    consumer_goods                        = 'Consumer Goods'
    consumer_services                     = 'Consumer Services'
    cosmetics                             = 'Cosmetics'
    dairy                                 = 'Dairy'
    defense_space                         = 'Defense & Space'
    design                                = 'Design'
    education_management                  = 'Education Management'
    e_learning                            = 'E-Learning'
    electrical_electronic_manufacturing   = 'Electrical/Electronic Manufacturing'
    entertainment                         = 'Entertainment'
    environmental_services                = 'Environmental Services'
    events_services                       = 'Events Services'
    executive_office                      = 'Executive Office'
    facilities_services                   = 'Facilities Services'
    farming                               = 'Farming'
    financial_services                    = 'Financial Services'
    fine_art                              = 'Fine Art'
    fishery                               = 'Fishery'
    food_beverages                        = 'Food & Beverages'
    food_production                       = 'Food Production'
    fund_raising                          = 'Fund-Raising'
    furniture                             = 'Furniture'
    gambling_casinos                      = 'Gambling & Casinos'
    glass_ceramics_concrete               = 'Glass, Ceramics & Concrete'
    government_administration             = 'Government Administration'
    government_relations                  = 'Government Relations'
    graphic_design                        = 'Graphic Design'
    health_wellness_and_fitness           = 'Health, Wellness and Fitness'
    higher_education                      = 'Higher Education'
    hospital_health_care                  = 'Hospital & Health Care'
    hospitality                           = 'Hospitality'
    human_resources                       = 'Human Resources'
    import_and_export                     = 'Import and Export'
    individual_family_services            = 'Individual & Family Services'
    industrial_automation                 = 'Industrial Automation'
    information_services                  = 'Information Services'
    information_technology_and_services   = 'Information Technology and Services'
    insurance                             = 'Insurance'
    international_affairs                 = 'International Affairs'
    international_trade_and_development   = 'International Trade and Development'
    internet                              = 'Internet'
    investment_banking                    = 'Investment Banking'
    investment_management                 = 'Investment Management'
    judiciary                             = 'Judiciary'
    law_enforcement                       = 'Law Enforcement'
    law_practice                          = 'Law Practice'
    legal_services                        = 'Legal Services'
    legislative_office                    = 'Legislative Office'
    leisure_travel_tourism                = 'Leisure, Travel & Tourism'
    libraries                             = 'Libraries'
    logistics_and_supply_chain            = 'Logistics and Supply Chain'
    luxury_goods_jewelry                  = 'Luxury Goods & Jewelry'
    machinery                             = 'Machinery'
    management_consulting                 = 'Management Consulting'
    maritime                              = 'Maritime'
    market_research                       = 'Market Research'
    marketing_and_advertising             = 'Marketing and Advertising'
    mechanical_or_industrial_engineering  = 'Mechanical or Industrial Engineering'
    media_production                      = 'Media Production'
    medical_devices                       = 'Medical Devices'
    medical_practice                      = 'Medical Practice'
    mental_health_care                    = 'Mental Health Care'
    military                              = 'Military'
    mining_metals                         = 'Mining & Metals'
    motion_pictures_and_film              = 'Motion Pictures and Film'
    museums_and_institutions              = 'Museums and Institutions'
    music                                 = 'Music'
    nanotechnology                        = 'Nanotechnology'
    newspapers                            = 'Newspapers'
    non_profit_organization_management    = 'Non-Profit Organization Management'
    oil_energy                            = 'Oil & Energy'
    online_media                          = 'Online Media'
    outsourcing_offshoring                = 'Outsourcing/Offshoring'
    package_freight_delivery              = 'Package/Freight Delivery'
    packaging_and_containers              = 'Packaging and Containers'
    paper_forest_products                 = 'Paper & Forest Products'
    performing_arts                       = 'Performing Arts'
    pharmaceuticals                       = 'Pharmaceuticals'
    philanthropy                          = 'Philanthropy'
    photography                           = 'Photography'
    plastics                              = 'Plastics'
    political_organization                = 'Political Organization'
    primary_secondary_education           = 'Primary/Secondary Education'
    printing                              = 'Printing'
    professional_training_coaching        = 'Professional Training & Coaching'
    program_development                   = 'Program Development'
    public_policy                         = 'Public Policy'
    public_relations_and_communications   = 'Public Relations and Communications'
    public_safety                         = 'Public Safety'
    publishing                            = 'Publishing'
    railroad_manufacture                  = 'Railroad Manufacture'
    ranching                              = 'Ranching'
    real_estate                           = 'Real Estate'
    recreational_facilities_and_services  = 'Recreational Facilities and Services'
    religious_institutions                = 'Religious Institutions'
    renewables_environment                = 'Renewables & Environment'
    research                              = 'Research'
    restaurants                           = 'Restaurants'
    retail                                = 'Retail'
    security_and_investigations           = 'Security and Investigations'
    semiconductors                        = 'Semiconductors'
    shipbuilding                          = 'Shipbuilding'
    sporting_goods                        = 'Sporting Goods'
    sports                                = 'Sports'
    staffing_and_recruiting               = 'Staffing and Recruiting'
    supermarkets                          = 'Supermarkets'
    telecommunications                    = 'Telecommunications'
    textiles                              = 'Textiles'
    think_tanks                           = 'Think Tanks'
    tobacco                               = 'Tobacco'
    translation_and_localization          = 'Translation and Localization'
    transportation_trucking_railroad      = 'Transportation/Trucking/Railroad'
    utilities                             = 'Utilities'
    venture_capital_private_equity        = 'Venture Capital & Private Equity'
    veterinary                            = 'Veterinary'
    warehousing                           = 'Warehousing'
    wholesale                             = 'Wholesale'
    wine_and_spirits                      = 'Wine and Spirits'
    wireless                              = 'Wireless'
    writing_and_editing                   = 'Writing and Editing'


# @dataclass
# class User:
#     id: int  # primary key
#     skills: List[str] = None
#     # graduated: collection of 'graduate' entries
#     # courses: collection of 'course' entries, backed by 'enrollments' table
#     # experience: collection of 'experience' entries
#
#
# @dataclass
# class University:
#     name: int  # primary key
#     # courses: collection of 'course' entries
#     # alumni: collection of 'graduate' entries
#
#
# @dataclass
# class Course:
#     id: int  # primary key
#     university: str  # foreign key for 'university.name'
#     courseTitle: str  # not null
#     courseNumber: str  # not null
#
#
# @dataclass
# class Employer:
#     name: str  # primary key
#     # positions: collection of 'position' entries
#
#
# @dataclass
# class Position:
#     id: int  # primary key
#     employerName: str  # foreign key for 'employer.name'
#     jobTitle: str  # not null
#     # workers: collection of 'experience' entries
#
#
# @dataclass
# class Graduate:
#     userID: int  # primary key, foreign key for 'user.id'
#     university: str  # primary key, foreign key for 'university.name'
#     gradDate: int  # primary key
#     degree: DegreeType = None
#     major: str = None
#     gpa: float = None
#
#
# @dataclass
# class Experience:
#     userID: int  # primary key, foreign key for 'user.id'
#     positionID: int  # primary key, foreign key for 'position.id'
#     salary: int
#     type: JobType
#     rating: int  # between 0 and 10
#     industry: Industry
#
#
# @dataclass
# class Enrollment:
#     userID: int  # primary key, foreign key for 'user.id'
#     courseID: int  # primary key, foreign key for 'course.id'
