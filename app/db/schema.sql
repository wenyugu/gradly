CREATE TABLE user (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    skills TEXT
);
CREATE TABLE university (
    name VARCHAR(255) NOT NULL COLLATE NOCASE,
    PRIMARY KEY (name)
);
CREATE TABLE position (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "employerName" VARCHAR(255) COLLATE NOCASE,
    "jobTitle" VARCHAR(50) NOT NULL COLLATE NOCASE,
    FOREIGN KEY("employerName") REFERENCES employer (name) ON UPDATE CASCADE
);
CREATE TABLE education (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "userID" INTEGER NOT NULL,
    university VARCHAR(255) NOT NULL COLLATE NOCASE,
    year INTEGER NOT NULL,
    degree VARCHAR(10),
    major VARCHAR(255) COLLATE NOCASE,
    gpa NUMERIC(3, 2),
    FOREIGN KEY(university) REFERENCES university (name) ON UPDATE CASCADE,
    FOREIGN KEY("userID") REFERENCES user (id) ON DELETE CASCADE,
    CONSTRAINT degreetype CHECK (degree IN ('associate', 'bachelor', 'master', 'phd'))
);
CREATE TABLE experience (
    "userID" INTEGER NOT NULL,
    "positionID" INTEGER NOT NULL,
    salary INTEGER,
    type VARCHAR(9),
    rating INTEGER,
    industry VARCHAR(36),
    PRIMARY KEY ("userID", "positionID"),
    FOREIGN KEY("positionID") REFERENCES position (id) ON DELETE CASCADE,
    FOREIGN KEY("userID") REFERENCES user (id) ON DELETE CASCADE,
    CONSTRAINT rating CHECK (rating BETWEEN 0 AND 10),
    CONSTRAINT jobtype CHECK (type IN ('intern', 'research', 'co-op', 'part-time', 'full-time')),
    CONSTRAINT industry CHECK (industry IN ('Accounting', 'Airlines/Aviation', 'Alternative Dispute Resolution', 'Alternative Medicine', 'Animation', 'Apparel & Fashion', 'Architecture & Planning', 'Arts and Crafts', 'Automotive', 'Aviation & Aerospace', 'Banking', 'Biotechnology', 'Broadcast Media', 'Building Materials', 'Business Supplies and Equipment', 'Capital Markets', 'Chemicals', 'Civic & Social Organization', 'Civil Engineering', 'Commercial Real Estate', 'Computer & Network Security', 'Computer Games', 'Computer Hardware', 'Computer Networking', 'Computer Software', 'Construction', 'Consumer Electronics', 'Consumer Goods', 'Consumer Services', 'Cosmetics', 'Dairy', 'Defense & Space', 'Design', 'Education Management', 'E-Learning', 'Electrical/Electronic Manufacturing', 'Entertainment', 'Environmental Services', 'Events Services', 'Executive Office', 'Facilities Services', 'Farming', 'Financial Services', 'Fine Art', 'Fishery', 'Food & Beverages', 'Food Production', 'Fund-Raising', 'Furniture', 'Gambling & Casinos', 'Glass, Ceramics & Concrete', 'Government Administration', 'Government Relations', 'Graphic Design', 'Health, Wellness and Fitness', 'Higher Education', 'Hospital & Health Care', 'Hospitality', 'Human Resources', 'Import and Export', 'Individual & Family Services', 'Industrial Automation', 'Information Services', 'Information Technology and Services', 'Insurance', 'International Affairs', 'International Trade and Development', 'Internet', 'Investment Banking', 'Investment Management', 'Judiciary', 'Law Enforcement', 'Law Practice', 'Legal Services', 'Legislative Office', 'Leisure, Travel & Tourism', 'Libraries', 'Logistics and Supply Chain', 'Luxury Goods & Jewelry', 'Machinery', 'Management Consulting', 'Maritime', 'Market Research', 'Marketing and Advertising', 'Mechanical or Industrial Engineering', 'Media Production', 'Medical Devices', 'Medical Practice', 'Mental Health Care', 'Military', 'Mining & Metals', 'Motion Pictures and Film', 'Museums and Institutions', 'Music', 'Nanotechnology', 'Newspapers', 'Non-Profit Organization Management', 'Oil & Energy', 'Online Media', 'Outsourcing/Offshoring', 'Package/Freight Delivery', 'Packaging and Containers', 'Paper & Forest Products', 'Performing Arts', 'Pharmaceuticals', 'Philanthropy', 'Photography', 'Plastics', 'Political Organization', 'Primary/Secondary Education', 'Printing', 'Professional Training & Coaching', 'Program Development', 'Public Policy', 'Public Relations and Communications', 'Public Safety', 'Publishing', 'Railroad Manufacture', 'Ranching', 'Real Estate', 'Recreational Facilities and Services', 'Religious Institutions', 'Renewables & Environment', 'Research', 'Restaurants', 'Retail', 'Security and Investigations', 'Semiconductors', 'Shipbuilding', 'Sporting Goods', 'Sports', 'Staffing and Recruiting', 'Supermarkets', 'Telecommunications', 'Textiles', 'Think Tanks', 'Tobacco', 'Translation and Localization', 'Transportation/Trucking/Railroad', 'Utilities', 'Venture Capital & Private Equity', 'Veterinary', 'Warehousing', 'Wholesale', 'Wine and Spirits', 'Wireless', 'Writing and Editing'))
);
CREATE TABLE enrollment (
    "educationID" INTEGER NOT NULL,
    "courseID" INTEGER NOT NULL,
    PRIMARY KEY ("educationID", "courseID"),
    FOREIGN KEY("courseID") REFERENCES course (id) ON DELETE CASCADE,
    FOREIGN KEY("educationID") REFERENCES education (id) ON DELETE CASCADE
);
CREATE TABLE employer (
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (name)
);
CREATE TABLE course (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "universityName" VARCHAR(255) COLLATE NOCASE,
    "courseTitle" VARCHAR(255) NOT NULL COLLATE NOCASE,
    "courseNumber" VARCHAR(10) NOT NULL COLLATE NOCASE,
    FOREIGN KEY("universityName") REFERENCES university (name) ON UPDATE CASCADE ON DELETE CASCADE
);
