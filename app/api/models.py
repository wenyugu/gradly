import enum
from api import db


class CompanySize(enum.Enum):
    micro = '< 10'
    small = '< 250'
    medium = '< 500'
    large = '< 1000'
    enterprise = '1000+'


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


enrollment = db.Table('enrollment',
                      db.Column('userID', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('courseID', db.Integer, db.ForeignKey('course.id'), primary_key=True),
                      # db.Column('university', db.String(255), db.ForeignKey('university.name'), primary_key=True),
                      )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skills = db.Column(db.Text)
    graduated = db.relationship('Graduate', cascade='delete')
    courses = db.relationship('Course', secondary=enrollment, backref='students')
    experience = db.relationship('Experience', cascade='delete')

    def __repr__(self):
        return '<User {}>'.format(self.userID)


class University(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    courses = db.relationship('Course', backref='offered_at', lazy=True)
    alumni = db.relationship('Graduate', cascade='delete')

    def __repr__(self):
        return '<University {}>'.format(self.name)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    universityName = db.Column(db.String(255), db.ForeignKey('university.name'))
    courseTitle = db.Column(db.String(255), nullable=False, default='')
    courseNumber = db.Column(db.String(10), nullable=False, default='')
    # offered_at: backref to University
    # students: backref to User

    # focusArea = db.Column(db.String(255))   # TODO: perhaps ENUM would be better?

    def __repr__(self):
        return '<Course {} at {}>'.format(self.courseTitle, self.university)


class Employer(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    positions = db.relationship('Position', backref='company', lazy=True)

    # industry = db.Column(db.String(255))    # TODO: perhaps ENUM would be better?
    # size = db.Column(
    #     db.Enum(CompanySize, values_callable=lambda x: [e.value for e in x])
    # )

    def __repr__(self):
        return '<Employer {}>'.format(self.name)


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employerName = db.Column(db.String(255), db.ForeignKey('employer.name'))
    jobTitle = db.Column(db.String(50), nullable=False)
    workers = db.relationship('Experience', cascade='delete')
    # company: backref to Employer

    # focusArea = db.Column(db.String(255))
    # minSalary = db.Column(db.Integer)     # this is something the employer would have to provide
    # maxSalary = db.Column(db.Integer)     # or be inferred from experience entries. Probably unnecessary

    def __repr__(self):
        return '<Job: {}>'.format(self.jobTitle)


class Graduate(db.Model):
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    university = db.Column(db.String(255), db.ForeignKey('university.name'), primary_key=True)
    gradDate = db.Column(db.Integer, primary_key=True)  # alternatively type db.Date
    degree = db.Column(db.Enum(DegreeType))
    major = db.Column(db.String(255))
    gpa = db.Column(db.Numeric(3, 2))

    def __repr__(self):
        return '<Graduate: {} from {} on {}>'.format(self.userID, self.university, self.gradDate)


class Experience(db.Model):
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    positionID = db.Column(db.Integer, db.ForeignKey('position.id'), primary_key=True)
    salary = db.Column(db.Integer)
    type = db.Column(db.Enum(JobType))
    rating = db.Column(db.SmallInteger)
    industry = db.Column(db.Enum(Industry, values_callable=lambda x: [e.value for e in x]))

    # db.Column('startDate', db.Date)
    # db.Column('location', db.String(255))

    def __repr__(self):
        return '<Experience: {}>'.format(self.positionID)
