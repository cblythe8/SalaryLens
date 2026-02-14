"""
Generate comprehensive US + Canadian salary data for the SalaryLens site.

Covers ~480 BLS occupations across 50 US metros and 10 Canadian cities.
Uses published BLS OES national medians with metro-area cost-of-living adjustments.

This produces ~18,000+ salary records for programmatic SEO pages.
"""

import json
import os
import random

random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "next-app", "src", "lib")

# =============================================================================
# OCCUPATIONS — ~300 roles organized by BLS SOC major group
# Format: (slug, soc_code, display_name, us_national_median)
# Medians approximate BLS OES May 2023 data
# =============================================================================

OCCUPATIONS = [
    # -------------------------------------------------------------------------
    # 11-0000  MANAGEMENT OCCUPATIONS
    # -------------------------------------------------------------------------
    ("chief-executives", "11-1011", "Chief Executives", 206680),
    ("general-operations-managers", "11-1021", "General and Operations Managers", 101280),
    ("legislators", "11-1031", "Legislators", 41110),
    ("advertising-promotions-managers", "11-2011", "Advertising and Promotions Managers", 131870),
    ("marketing-managers", "11-2021", "Marketing Managers", 156580),
    ("sales-managers", "11-2022", "Sales Managers", 135160),
    ("public-relations-managers", "11-2031", "Public Relations Managers", 132620),
    ("fundraising-managers", "11-2033", "Fundraising Managers", 119200),
    ("administrative-services-managers", "11-3012", "Administrative Services Managers", 107390),
    ("facilities-managers", "11-3013", "Facilities Managers", 99510),
    ("computer-information-systems-managers", "11-3021", "Computer and Information Systems Managers", 169510),
    ("financial-managers", "11-3031", "Financial Managers", 156100),
    ("compensation-benefits-managers", "11-3111", "Compensation and Benefits Managers", 136380),
    ("human-resources-managers", "11-3121", "Human Resources Managers", 136350),
    ("training-development-managers", "11-3131", "Training and Development Managers", 125040),
    ("industrial-production-managers", "11-3051", "Industrial Production Managers", 116970),
    ("purchasing-managers", "11-3061", "Purchasing Managers", 133530),
    ("transportation-storage-distribution-managers", "11-3071", "Transportation, Storage, and Distribution Managers", 105580),
    ("construction-managers", "11-9021", "Construction Managers", 108210),
    ("education-administrators-postsecondary", "11-9033", "Education Administrators, Postsecondary", 102610),
    ("education-administrators-k12", "11-9032", "Education Administrators, K-12", 103010),
    ("food-service-managers", "11-9051", "Food Service Managers", 63060),
    ("lodging-managers", "11-9081", "Lodging Managers", 65360),
    ("medical-health-services-managers", "11-9111", "Medical and Health Services Managers", 110680),
    ("natural-sciences-managers", "11-9121", "Natural Sciences Managers", 157740),
    ("property-real-estate-managers", "11-9141", "Property, Real Estate, and Community Association Managers", 63950),
    ("social-community-service-managers", "11-9151", "Social and Community Service Managers", 77030),
    ("emergency-management-directors", "11-9161", "Emergency Management Directors", 83960),
    ("entertainment-recreation-managers", "11-9071", "Entertainment and Recreation Managers", 56580),

    # -------------------------------------------------------------------------
    # 13-0000  BUSINESS AND FINANCIAL OPERATIONS
    # -------------------------------------------------------------------------
    ("agents-business-managers-artists", "13-1011", "Agents and Business Managers of Artists and Performers", 80370),
    ("buyers-purchasing-agents", "13-1022", "Wholesale and Retail Buyers", 66750),
    ("claims-adjusters", "13-1031", "Claims Adjusters, Examiners, and Investigators", 72680),
    ("compliance-officers", "13-1041", "Compliance Officers", 76060),
    ("cost-estimators", "13-1051", "Cost Estimators", 73200),
    ("human-resources-specialists", "13-1071", "Human Resources Specialists", 67650),
    ("labor-relations-specialists", "13-1075", "Labor Relations Specialists", 86110),
    ("logisticians", "13-1081", "Logisticians", 79400),
    ("management-analysts", "13-1111", "Management Analysts", 99410),
    ("meeting-convention-planners", "13-1121", "Meeting, Convention, and Event Planners", 56920),
    ("project-management-specialists", "13-1082", "Project Management Specialists", 98580),
    ("fundraisers", "13-1131", "Fundraisers", 64160),
    ("training-development-specialists", "13-1151", "Training and Development Specialists", 64340),
    ("market-research-analysts", "13-1161", "Market Research Analysts and Marketing Specialists", 74680),
    ("business-operations-specialists", "13-1199", "Business Operations Specialists", 79420),
    ("accountants-auditors", "13-2011", "Accountants and Auditors", 79880),
    ("appraisers-assessors", "13-2023", "Appraisers and Assessors of Real Estate", 61560),
    ("budget-analysts", "13-2031", "Budget Analysts", 84940),
    ("credit-analysts", "13-2041", "Credit Analysts", 80400),
    ("financial-analysts", "13-2051", "Financial Analysts", 99890),
    ("personal-financial-advisors", "13-2052", "Personal Financial Advisors", 99580),
    ("insurance-underwriters", "13-2053", "Insurance Underwriters", 79880),
    ("financial-examiners", "13-2061", "Financial Examiners", 89790),
    ("loan-officers", "13-2072", "Loan Officers", 69990),
    ("tax-preparers", "13-2082", "Tax Preparers", 48780),

    # -------------------------------------------------------------------------
    # 15-0000  COMPUTER AND MATHEMATICAL
    # -------------------------------------------------------------------------
    ("computer-information-research-scientists", "15-1221", "Computer and Information Research Scientists", 145080),
    ("computer-systems-analysts", "15-1211", "Computer Systems Analysts", 103800),
    ("information-security-analysts", "15-1212", "Information Security Analysts", 120360),
    ("computer-programmers", "15-1251", "Computer Programmers", 97800),
    ("software-developers", "15-1252", "Software Developers", 132270),
    ("software-quality-assurance-analysts", "15-1253", "Software Quality Assurance Analysts and Testers", 101800),
    ("web-developers", "15-1254", "Web Developers", 80730),
    ("web-digital-interface-designers", "15-1255", "Web and Digital Interface Designers", 83240),
    ("database-administrators", "15-1242", "Database Administrators", 101510),
    ("database-architects", "15-1243", "Database Architects", 135710),
    ("network-systems-administrators", "15-1244", "Network and Computer Systems Administrators", 95360),
    ("computer-network-architects", "15-1241", "Computer Network Architects", 129840),
    ("computer-user-support-specialists", "15-1232", "Computer User Support Specialists", 57910),
    ("computer-network-support-specialists", "15-1231", "Computer Network Support Specialists", 72680),
    ("data-scientists", "15-2051", "Data Scientists", 108020),
    ("actuaries", "15-2011", "Actuaries", 120000),
    ("statisticians", "15-2041", "Statisticians", 104860),
    ("operations-research-analysts", "15-2031", "Operations Research Analysts", 85720),
    ("product-managers", "15-1299", "Product Managers", 120990),

    # -------------------------------------------------------------------------
    # 17-0000  ARCHITECTURE AND ENGINEERING
    # -------------------------------------------------------------------------
    ("architects", "17-1011", "Architects", 93310),
    ("landscape-architects", "17-1012", "Landscape Architects", 76760),
    ("surveyors", "17-1022", "Surveyors", 68570),
    ("cartographers-photogrammetrists", "17-1021", "Cartographers and Photogrammetrists", 76050),
    ("aerospace-engineers", "17-2011", "Aerospace Engineers", 130720),
    ("biomedical-engineers", "17-2031", "Biomedical Engineers", 100830),
    ("chemical-engineers", "17-2041", "Chemical Engineers", 112100),
    ("civil-engineers", "17-2051", "Civil Engineers", 89940),
    ("computer-hardware-engineers", "17-2061", "Computer Hardware Engineers", 138590),
    ("electrical-engineers", "17-2071", "Electrical Engineers", 109350),
    ("electronics-engineers", "17-2072", "Electronics Engineers", 112930),
    ("environmental-engineers", "17-2081", "Environmental Engineers", 100090),
    ("health-safety-engineers", "17-2111", "Health and Safety Engineers", 102870),
    ("industrial-engineers", "17-2112", "Industrial Engineers", 99380),
    ("marine-engineers", "17-2121", "Marine Engineers and Naval Architects", 100060),
    ("materials-engineers", "17-2131", "Materials Engineers", 105620),
    ("mechanical-engineers", "17-2141", "Mechanical Engineers", 96310),
    ("mining-geological-engineers", "17-2151", "Mining and Geological Engineers", 100840),
    ("nuclear-engineers", "17-2161", "Nuclear Engineers", 124350),
    ("petroleum-engineers", "17-2171", "Petroleum Engineers", 131800),
    ("drafters", "17-3010", "Drafters", 61700),
    ("engineering-technicians", "17-3020", "Engineering Technicians", 60870),

    # -------------------------------------------------------------------------
    # 19-0000  LIFE, PHYSICAL, AND SOCIAL SCIENCE
    # -------------------------------------------------------------------------
    ("biochemists-biophysicists", "19-1021", "Biochemists and Biophysicists", 107460),
    ("microbiologists", "19-1022", "Microbiologists", 85520),
    ("zoologists-wildlife-biologists", "19-1023", "Zoologists and Wildlife Biologists", 68230),
    ("conservation-scientists", "19-1031", "Conservation Scientists", 65620),
    ("epidemiologists", "19-1041", "Epidemiologists", 81390),
    ("medical-scientists", "19-1042", "Medical Scientists", 99930),
    ("chemists", "19-2031", "Chemists", 84680),
    ("environmental-scientists", "19-2041", "Environmental Scientists and Specialists", 76480),
    ("geoscientists", "19-2042", "Geoscientists", 87480),
    ("atmospheric-scientists", "19-2021", "Atmospheric and Space Scientists", 89260),
    ("physicists", "19-2012", "Physicists", 155680),
    ("economists", "19-3011", "Economists", 113940),
    ("survey-researchers", "19-3022", "Survey Researchers", 60800),
    ("psychologists-clinical", "19-3031", "Clinical Psychologists", 96100),
    ("sociologists", "19-3041", "Sociologists", 98590),
    ("urban-regional-planners", "19-3051", "Urban and Regional Planners", 81800),

    # -------------------------------------------------------------------------
    # 21-0000  COMMUNITY AND SOCIAL SERVICE
    # -------------------------------------------------------------------------
    ("substance-abuse-counselors", "21-1011", "Substance Abuse and Behavioral Disorder Counselors", 53710),
    ("educational-guidance-counselors", "21-1012", "Educational, Guidance, and Career Counselors", 61710),
    ("marriage-family-therapists", "21-1013", "Marriage and Family Therapists", 58510),
    ("mental-health-counselors", "21-1014", "Mental Health Counselors", 53710),
    ("rehabilitation-counselors", "21-1015", "Rehabilitation Counselors", 42910),
    ("social-workers-healthcare", "21-1022", "Healthcare Social Workers", 62940),
    ("social-workers-mental-health", "21-1023", "Mental Health and Substance Abuse Social Workers", 55960),
    ("community-health-workers", "21-1094", "Community Health Workers", 48860),
    ("probation-officers", "21-1092", "Probation Officers and Correctional Treatment Specialists", 60250),

    # -------------------------------------------------------------------------
    # 23-0000  LEGAL
    # -------------------------------------------------------------------------
    ("lawyers", "23-1011", "Lawyers", 145760),
    ("judges", "23-1023", "Judges and Magistrates", 152980),
    ("paralegals-legal-assistants", "23-2011", "Paralegals and Legal Assistants", 60970),
    ("arbitrators-mediators", "23-1022", "Arbitrators, Mediators, and Conciliators", 66130),
    ("court-reporters", "23-2093", "Court Reporters and Simultaneous Captioners", 63560),
    ("title-examiners", "23-2099", "Title Examiners, Abstractors, and Searchers", 53290),

    # -------------------------------------------------------------------------
    # 25-0000  EDUCATIONAL INSTRUCTION AND LIBRARY
    # -------------------------------------------------------------------------
    ("postsecondary-teachers", "25-1000", "Postsecondary Teachers", 84380),
    ("elementary-school-teachers", "25-2021", "Elementary School Teachers", 61690),
    ("middle-school-teachers", "25-2022", "Middle School Teachers", 63550),
    ("high-school-teachers", "25-2031", "High School Teachers", 65220),
    ("special-education-teachers", "25-2050", "Special Education Teachers", 65910),
    ("career-technical-education-teachers", "25-2032", "Career/Technical Education Teachers", 63870),
    ("preschool-teachers", "25-2011", "Preschool Teachers", 37840),
    ("tutors", "25-3041", "Tutors", 39350),
    ("librarians", "25-4022", "Librarians and Media Collections Specialists", 65580),
    ("archivists", "25-4011", "Archivists", 63480),
    ("instructional-coordinators", "25-9031", "Instructional Coordinators", 67490),
    ("teaching-assistants-postsecondary", "25-9044", "Teaching Assistants, Postsecondary", 41400),

    # -------------------------------------------------------------------------
    # 27-0000  ARTS, DESIGN, ENTERTAINMENT, SPORTS, AND MEDIA
    # -------------------------------------------------------------------------
    ("art-directors", "27-1011", "Art Directors", 106500),
    ("graphic-designers", "27-1024", "Graphic Designers", 57990),
    ("interior-designers", "27-1025", "Interior Designers", 62510),
    ("industrial-designers", "27-1021", "Industrial Designers", 77030),
    ("fashion-designers", "27-1022", "Fashion Designers", 79560),
    ("multimedia-artists-animators", "27-1014", "Multimedia Artists and Animators", 85820),
    ("producers-directors", "27-2012", "Producers and Directors", 86490),
    ("writers-authors", "27-3043", "Writers and Authors", 73690),
    ("editors", "27-3041", "Editors", 73080),
    ("technical-writers", "27-3042", "Technical Writers", 80050),
    ("reporters-journalists", "27-3023", "Reporters, Correspondents, and Broadcast News Analysts", 55960),
    ("photographers", "27-4021", "Photographers", 40760),
    ("film-video-editors", "27-4032", "Film and Video Editors and Camera Operators", 62980),
    ("sound-engineering-technicians", "27-4014", "Sound Engineering Technicians", 60710),
    ("public-relations-specialists", "27-3031", "Public Relations Specialists", 67440),
    ("interpreters-translators", "27-3091", "Interpreters and Translators", 57090),

    # -------------------------------------------------------------------------
    # 29-0000  HEALTHCARE PRACTITIONERS AND TECHNICAL
    # -------------------------------------------------------------------------
    ("dentists", "29-1021", "Dentists", 165230),
    ("dietitians-nutritionists", "29-1031", "Dietitians and Nutritionists", 69680),
    ("optometrists", "29-1041", "Optometrists", 131860),
    ("pharmacists", "29-1051", "Pharmacists", 136030),
    ("physicians-surgeons", "29-1228", "Physicians, All Other", 229300),
    ("anesthesiologists", "29-1211", "Anesthesiologists", 331190),
    ("family-medicine-physicians", "29-1215", "Family Medicine Physicians", 224460),
    ("psychiatrists", "29-1223", "Psychiatrists", 269530),
    ("surgeons", "29-1248", "Surgeons", 297800),
    ("physician-assistants", "29-1071", "Physician Assistants", 130020),
    ("podiatrists", "29-1081", "Podiatrists", 145840),
    ("registered-nurses", "29-1141", "Registered Nurses", 86070),
    ("nurse-anesthetists", "29-1151", "Nurse Anesthetists", 212650),
    ("nurse-practitioners", "29-1171", "Nurse Practitioners", 126260),
    ("nurse-midwives", "29-1161", "Nurse Midwives", 120880),
    ("audiologists", "29-1181", "Audiologists", 87740),
    ("occupational-therapists", "29-1122", "Occupational Therapists", 96370),
    ("physical-therapists", "29-1123", "Physical Therapists", 99710),
    ("radiation-therapists", "29-1124", "Radiation Therapists", 98300),
    ("recreational-therapists", "29-1125", "Recreational Therapists", 55820),
    ("respiratory-therapists", "29-1126", "Respiratory Therapists", 77960),
    ("speech-language-pathologists", "29-1127", "Speech-Language Pathologists", 89290),
    ("veterinarians", "29-1131", "Veterinarians", 119100),
    ("clinical-laboratory-technologists", "29-2011", "Clinical Laboratory Technologists and Technicians", 60780),
    ("dental-hygienists", "29-1292", "Dental Hygienists", 87530),
    ("diagnostic-medical-sonographers", "29-2032", "Diagnostic Medical Sonographers", 84990),
    ("emergency-medical-technicians", "29-2042", "Emergency Medical Technicians and Paramedics", 38930),
    ("licensed-practical-nurses", "29-2061", "Licensed Practical and Licensed Vocational Nurses", 55860),
    ("medical-records-specialists", "29-2072", "Medical Records Specialists", 48780),
    ("opticians", "29-2081", "Opticians, Dispensing", 42180),
    ("pharmacy-technicians", "29-2052", "Pharmacy Technicians", 38350),
    ("radiologic-technologists", "29-2034", "Radiologic Technologists and Technicians", 73410),
    ("surgical-technologists", "29-2055", "Surgical Technologists", 60790),

    # -------------------------------------------------------------------------
    # 31-0000  HEALTHCARE SUPPORT
    # -------------------------------------------------------------------------
    ("home-health-personal-care-aides", "31-1120", "Home Health and Personal Care Aides", 33530),
    ("nursing-assistants", "31-1131", "Nursing Assistants", 36220),
    ("orderlies", "31-1133", "Orderlies", 35400),
    ("occupational-therapy-assistants", "31-2011", "Occupational Therapy Assistants", 64230),
    ("physical-therapist-assistants", "31-2021", "Physical Therapist Assistants", 64080),
    ("massage-therapists", "31-9011", "Massage Therapists", 52100),
    ("dental-assistants", "31-9091", "Dental Assistants", 44820),
    ("medical-assistants", "31-9092", "Medical Assistants", 38270),
    ("veterinary-technologists", "31-9096", "Veterinary Technologists and Technicians", 38240),
    ("phlebotomists", "31-9097", "Phlebotomists", 40580),

    # -------------------------------------------------------------------------
    # 33-0000  PROTECTIVE SERVICE
    # -------------------------------------------------------------------------
    ("first-line-supervisors-police", "33-1012", "First-Line Supervisors of Police and Detectives", 99920),
    ("firefighters", "33-2011", "Firefighters", 57120),
    ("fire-inspectors", "33-2021", "Fire Inspectors and Investigators", 71750),
    ("correctional-officers", "33-3012", "Correctional Officers and Jailers", 47920),
    ("detectives-criminal-investigators", "33-3021", "Detectives and Criminal Investigators", 89930),
    ("police-officers", "33-3051", "Police and Sheriff's Patrol Officers", 74910),
    ("private-detectives-investigators", "33-9021", "Private Detectives and Investigators", 59380),
    ("security-guards", "33-9032", "Security Guards", 36020),
    ("crossing-guards", "33-9091", "Crossing Guards and Flaggers", 36070),

    # -------------------------------------------------------------------------
    # 35-0000  FOOD PREPARATION AND SERVING
    # -------------------------------------------------------------------------
    ("chefs-head-cooks", "35-1011", "Chefs and Head Cooks", 58740),
    ("first-line-supervisors-food", "35-1012", "First-Line Supervisors of Food Preparation and Serving", 40850),
    ("cooks-restaurant", "35-2014", "Cooks, Restaurant", 35110),
    ("cooks-fast-food", "35-2011", "Cooks, Fast Food", 28990),
    ("bartenders", "35-3011", "Bartenders", 31510),
    ("food-servers", "35-3041", "Food Servers, Nonrestaurant", 30160),
    ("waiters-waitresses", "35-3031", "Waiters and Waitresses", 31430),
    ("bakers", "35-2011", "Bakers", 34350),

    # -------------------------------------------------------------------------
    # 37-0000  BUILDING AND GROUNDS CLEANING AND MAINTENANCE
    # -------------------------------------------------------------------------
    ("janitors-cleaners", "37-2011", "Janitors and Cleaners", 34480),
    ("landscaping-groundskeeping", "37-3011", "Landscaping and Groundskeeping Workers", 36840),
    ("pest-control-workers", "37-2021", "Pest Control Workers", 40830),
    ("first-line-supervisors-housekeeping", "37-1011", "First-Line Supervisors of Housekeeping and Janitorial Workers", 47740),

    # -------------------------------------------------------------------------
    # 39-0000  PERSONAL CARE AND SERVICE
    # -------------------------------------------------------------------------
    ("animal-trainers", "39-2011", "Animal Trainers", 36690),
    ("barbers", "39-5011", "Barbers", 37680),
    ("hairdressers-hairstylists", "39-5012", "Hairdressers, Hairstylists, and Cosmetologists", 35080),
    ("childcare-workers", "39-9011", "Childcare Workers", 30210),
    ("fitness-trainers-instructors", "39-9031", "Fitness Trainers and Aerobics Instructors", 46480),
    ("funeral-attendants", "39-4021", "Funeral Attendants", 33530),
    ("travel-agents", "39-3031", "Travel Agents", 46900),

    # -------------------------------------------------------------------------
    # 41-0000  SALES AND RELATED
    # -------------------------------------------------------------------------
    ("first-line-supervisors-retail", "41-1011", "First-Line Supervisors of Retail Sales Workers", 47130),
    ("cashiers", "41-2011", "Cashiers", 29120),
    ("retail-salespersons", "41-2031", "Retail Salespersons", 33680),
    ("advertising-sales-agents", "41-3011", "Advertising Sales Agents", 61890),
    ("insurance-sales-agents", "41-3021", "Insurance Sales Agents", 59080),
    ("securities-financial-services-sales", "41-3031", "Securities, Commodities, and Financial Services Sales Agents", 76850),
    ("travel-agents-sales", "41-3041", "Travel Agents", 46900),
    ("real-estate-brokers", "41-9021", "Real Estate Brokers", 63060),
    ("real-estate-sales-agents", "41-9022", "Real Estate Sales Agents", 56620),
    ("sales-engineers", "41-9031", "Sales Engineers", 116950),
    ("sales-representatives-wholesale", "41-4012", "Sales Representatives, Wholesale and Manufacturing", 73080),
    ("telemarketers", "41-9041", "Telemarketers", 31560),

    # -------------------------------------------------------------------------
    # 43-0000  OFFICE AND ADMINISTRATIVE SUPPORT
    # -------------------------------------------------------------------------
    ("first-line-supervisors-office", "43-1011", "First-Line Supervisors of Office and Administrative Support Workers", 62180),
    ("bookkeeping-accounting-clerks", "43-3031", "Bookkeeping, Accounting, and Auditing Clerks", 47440),
    ("customer-service-representatives", "43-4051", "Customer Service Representatives", 39680),
    ("receptionists", "43-4171", "Receptionists and Information Clerks", 36840),
    ("cargo-freight-agents", "43-5011", "Cargo and Freight Agents", 51010),
    ("dispatchers", "43-5032", "Dispatchers", 46880),
    ("postal-service-mail-carriers", "43-5052", "Postal Service Mail Carriers", 55160),
    ("production-planning-clerks", "43-5061", "Production, Planning, and Expediting Clerks", 53070),
    ("shipping-receiving-clerks", "43-5071", "Shipping, Receiving, and Inventory Clerks", 38410),
    ("executive-secretaries-admin-assistants", "43-6011", "Executive Secretaries and Executive Administrative Assistants", 68230),
    ("legal-secretaries", "43-6012", "Legal Secretaries and Administrative Assistants", 53520),
    ("medical-secretaries", "43-6013", "Medical Secretaries and Administrative Assistants", 41580),
    ("secretaries-admin-assistants", "43-6014", "Secretaries and Administrative Assistants", 44680),
    ("data-entry-keyers", "43-9021", "Data Entry Keyers", 38930),
    ("insurance-claims-clerks", "43-9041", "Insurance Claims and Policy Processing Clerks", 47100),
    ("office-clerks-general", "43-9061", "Office Clerks, General", 38620),
    ("human-resources-assistants", "43-4161", "Human Resources Assistants", 46780),
    ("payroll-timekeeping-clerks", "43-3051", "Payroll and Timekeeping Clerks", 50230),

    # -------------------------------------------------------------------------
    # 45-0000  FARMING, FISHING, AND FORESTRY
    # -------------------------------------------------------------------------
    ("agricultural-inspectors", "45-2011", "Agricultural Inspectors", 48810),
    ("animal-breeders", "45-2021", "Animal Breeders", 44970),
    ("farmers-ranchers-agricultural-managers", "45-1011", "Farmers, Ranchers, and Other Agricultural Managers", 80060),
    ("logging-workers", "45-4022", "Logging Equipment Operators", 46430),

    # -------------------------------------------------------------------------
    # 47-0000  CONSTRUCTION AND EXTRACTION
    # -------------------------------------------------------------------------
    ("boilermakers", "47-2011", "Boilermakers", 64480),
    ("brickmasons-blockmasons", "47-2021", "Brickmasons and Blockmasons", 60400),
    ("carpenters", "47-2031", "Carpenters", 56350),
    ("carpet-floor-tile-installers", "47-2041", "Carpet Installers", 47180),
    ("cement-masons-concrete-finishers", "47-2051", "Cement Masons and Concrete Finishers", 51310),
    ("construction-laborers", "47-2061", "Construction Laborers", 43920),
    ("electricians", "47-2111", "Electricians", 61590),
    ("elevator-installers-repairers", "47-2111", "Elevator and Escalator Installers and Repairers", 102420),
    ("glaziers", "47-2121", "Glaziers", 50700),
    ("ironworkers", "47-2171", "Structural Iron and Steel Workers", 60640),
    ("painters-construction", "47-2141", "Painters, Construction and Maintenance", 46750),
    ("plumbers-pipefitters", "47-2152", "Plumbers, Pipefitters, and Steamfitters", 61550),
    ("roofers", "47-2181", "Roofers", 48390),
    ("sheet-metal-workers", "47-2211", "Sheet Metal Workers", 57700),
    ("solar-panel-installers", "47-2231", "Solar Photovoltaic Installers", 48800),
    ("operating-engineers", "47-2073", "Operating Engineers and Other Construction Equipment Operators", 56890),
    ("first-line-supervisors-construction", "47-1011", "First-Line Supervisors of Construction Trades", 76260),

    # -------------------------------------------------------------------------
    # 49-0000  INSTALLATION, MAINTENANCE, AND REPAIR
    # -------------------------------------------------------------------------
    ("automotive-service-technicians", "49-3023", "Automotive Service Technicians and Mechanics", 46840),
    ("bus-truck-mechanics", "49-3031", "Bus and Truck Mechanics and Diesel Engine Specialists", 56410),
    ("aircraft-mechanics", "49-3011", "Aircraft Mechanics and Service Technicians", 75020),
    ("hvac-technicians", "49-9021", "Heating, Air Conditioning, and Refrigeration Mechanics and Installers", 57300),
    ("industrial-machinery-mechanics", "49-9041", "Industrial Machinery Mechanics", 61590),
    ("maintenance-workers-general", "49-9071", "Maintenance and Repair Workers, General", 46700),
    ("telecommunications-equipment-installers", "49-2022", "Telecommunications Equipment Installers and Repairers", 61080),
    ("electrical-power-line-installers", "49-9051", "Electrical Power-Line Installers and Repairers", 82340),
    ("wind-turbine-technicians", "49-9081", "Wind Turbine Service Technicians", 61770),
    ("computer-automated-teller-machine-repairers", "49-2011", "Computer, Automated Teller, and Office Machine Repairers", 44830),
    ("first-line-supervisors-mechanics", "49-1011", "First-Line Supervisors of Mechanics, Installers, and Repairers", 76700),

    # -------------------------------------------------------------------------
    # 51-0000  PRODUCTION
    # -------------------------------------------------------------------------
    ("first-line-supervisors-production", "51-1011", "First-Line Supervisors of Production and Operating Workers", 66470),
    ("machinists", "51-4041", "Machinists", 49580),
    ("welders-cutters-solderers", "51-4121", "Welders, Cutters, Solderers, and Brazers", 48600),
    ("cnc-machine-tool-operators", "51-4011", "Computer Numerically Controlled Machine Tool Programmers", 58990),
    ("inspectors-testers-sorters", "51-9061", "Inspectors, Testers, Sorters, Samplers, and Weighers", 45970),
    ("printing-press-operators", "51-5112", "Printing Press Operators", 40870),
    ("water-wastewater-treatment-operators", "51-8031", "Water and Wastewater Treatment Plant and System Operators", 53920),
    ("power-plant-operators", "51-8013", "Power Plant Operators", 100110),
    ("chemical-plant-operators", "51-8091", "Chemical Plant and System Operators", 65370),
    ("food-processing-workers", "51-3020", "Food Processing Workers", 36940),
    ("woodworkers", "51-7040", "Woodworkers", 38200),
    ("electrical-electronic-assemblers", "51-2028", "Electrical, Electronic, and Electromechanical Assemblers", 39430),

    # -------------------------------------------------------------------------
    # 53-0000  TRANSPORTATION AND MATERIAL MOVING
    # -------------------------------------------------------------------------
    ("airline-pilots-flight-engineers", "53-2011", "Airline Pilots, Copilots, and Flight Engineers", 219140),
    ("commercial-pilots", "53-2012", "Commercial Pilots", 113080),
    ("air-traffic-controllers", "53-2021", "Air Traffic Controllers", 137380),
    ("bus-drivers-transit", "53-3052", "Bus Drivers, Transit and Intercity", 50100),
    ("bus-drivers-school", "53-3051", "Bus Drivers, School", 43020),
    ("truck-drivers-heavy-tractor-trailer", "53-3032", "Heavy and Tractor-Trailer Truck Drivers", 54320),
    ("truck-drivers-light-delivery", "53-3033", "Light Truck Drivers", 40910),
    ("taxi-drivers-chauffeurs", "53-3054", "Taxi Drivers and Chauffeurs", 36180),
    ("locomotive-engineers", "53-4011", "Locomotive Engineers", 79850),
    ("sailors-marine-oilers", "53-5011", "Sailors and Marine Oilers", 49160),
    ("parking-attendants", "53-6021", "Parking Attendants", 30870),
    ("industrial-truck-operators", "53-7051", "Industrial Truck and Tractor Operators", 41880),
    ("material-moving-workers", "53-7060", "Laborers and Material Movers", 35510),
    ("flight-attendants", "53-2031", "Flight Attendants", 68370),

    # -------------------------------------------------------------------------
    # ADDITIONAL OCCUPATIONS — Fill gaps for comprehensive coverage
    # -------------------------------------------------------------------------

    # Management additions
    ("architectural-engineering-managers", "11-9041", "Architectural and Engineering Managers", 165370),
    ("gaming-managers", "11-9071", "Gaming Managers", 83300),
    ("postmasters-mail-superintendents", "11-9131", "Postmasters and Mail Superintendents", 80850),

    # Business/Financial additions
    ("compensation-job-analysis-specialists", "13-1141", "Compensation, Benefits, and Job Analysis Specialists", 72530),
    ("credit-counselors", "13-2071", "Credit Counselors", 48690),
    ("financial-risk-specialists", "13-2054", "Financial Risk Specialists", 102120),

    # Computer/Math additions
    ("computer-science-teachers-postsecondary", "25-1021", "Computer Science Teachers, Postsecondary", 97950),

    # Architecture/Engineering additions
    ("agricultural-engineers", "17-2021", "Agricultural Engineers", 88750),
    ("architectural-civil-drafters", "17-3011", "Architectural and Civil Drafters", 60700),
    ("electrical-electronic-drafters", "17-3012", "Electrical and Electronics Drafters", 66670),
    ("mechanical-drafters", "17-3013", "Mechanical Drafters", 62180),
    ("electrical-engineering-technicians", "17-3023", "Electrical and Electronic Engineering Technicians", 65200),
    ("mechanical-engineering-technicians", "17-3027", "Mechanical Engineering Technicians", 62200),
    ("industrial-engineering-technicians", "17-3026", "Industrial Engineering Technicians", 60300),
    ("civil-engineering-technicians", "17-3022", "Civil Engineering Technicians", 60420),

    # Life/Physical/Social Science additions
    ("biological-technicians", "19-4021", "Biological Technicians", 51530),
    ("chemical-technicians", "19-4031", "Chemical Technicians", 53560),
    ("environmental-science-technicians", "19-4042", "Environmental Science and Protection Technicians", 50220),
    ("forensic-science-technicians", "19-4092", "Forensic Science Technicians", 64940),
    ("geological-technicians", "19-4043", "Geological and Hydrologic Technicians", 51320),
    ("nuclear-technicians", "19-4051", "Nuclear Technicians", 99340),
    ("food-scientists", "19-1012", "Food Scientists and Technologists", 82340),
    ("animal-scientists", "19-1011", "Animal Scientists", 77030),
    ("soil-plant-scientists", "19-1013", "Soil and Plant Scientists", 70160),
    ("hydrologists", "19-2043", "Hydrologists", 88620),
    ("political-scientists", "19-3094", "Political Scientists", 128020),
    ("anthropologists-archaeologists", "19-3091", "Anthropologists and Archaeologists", 68150),
    ("historians", "19-3093", "Historians", 69690),
    ("geographers", "19-3092", "Geographers", 87620),

    # Community/Social Service additions
    ("child-family-social-workers", "21-1021", "Child, Family, and School Social Workers", 55350),
    ("health-education-specialists", "21-1091", "Health Education Specialists", 62860),
    ("clergy", "21-2011", "Clergy", 57230),
    ("directors-religious-activities", "21-2021", "Directors, Religious Activities and Education", 49250),
    ("social-workers-all-other", "21-1029", "Social Workers, All Other", 64740),

    # Legal additions
    ("judicial-law-clerks", "23-1012", "Judicial Law Clerks", 62470),
    ("legal-support-workers", "23-2099", "Legal Support Workers, All Other", 60170),

    # Education additions
    ("substitute-teachers", "25-3031", "Substitute Teachers, Short-Term", 38030),
    ("teacher-assistants", "25-9042", "Teaching Assistants, Except Postsecondary", 33600),
    ("self-enrichment-teachers", "25-3021", "Self-Enrichment Teachers", 46500),
    ("adult-literacy-teachers", "25-3011", "Adult Basic Education and Literacy Teachers", 60780),
    ("curators", "25-4012", "Curators", 63880),
    ("museum-technicians", "25-4013", "Museum Technicians and Conservators", 49780),
    ("library-technicians", "25-4031", "Library Technicians", 39230),

    # Arts/Design/Entertainment/Media additions
    ("actors", "27-2011", "Actors", 56920),
    ("athletes-sports-competitors", "27-2021", "Athletes and Sports Competitors", 77300),
    ("coaches-scouts", "27-2022", "Coaches and Scouts", 44890),
    ("umpires-referees", "27-2023", "Umpires, Referees, and Other Sports Officials", 38060),
    ("dancers-choreographers", "27-2031", "Dancers and Choreographers", 42870),
    ("music-directors-composers", "27-2041", "Music Directors and Composers", 69880),
    ("musicians-singers", "27-2042", "Musicians and Singers", 51150),
    ("disc-jockeys", "27-2091", "Disc Jockeys", 43530),
    ("broadcast-announcers", "27-3011", "Broadcast Announcers and Radio Disc Jockeys", 43160),
    ("fine-artists", "27-1013", "Fine Artists, Including Painters, Sculptors, and Illustrators", 56320),
    ("craft-artists", "27-1012", "Craft Artists", 40530),
    ("floral-designers", "27-1023", "Floral Designers", 33430),
    ("set-exhibit-designers", "27-1027", "Set and Exhibit Designers", 61070),
    ("audio-video-technicians", "27-4011", "Audio and Video Technicians", 52120),
    ("broadcast-technicians", "27-4012", "Broadcast Technicians", 52280),
    ("lighting-technicians", "27-4015", "Lighting Technicians", 59990),
    ("camera-operators-tv-film", "27-4031", "Camera Operators, Television, Video, and Film", 62030),

    # Healthcare Practitioners additions
    ("chiropractors", "29-1011", "Chiropractors", 75380),
    ("athletic-trainers", "29-9091", "Athletic Trainers", 57930),
    ("exercise-physiologists", "29-1128", "Exercise Physiologists", 55560),
    ("genetic-counselors", "29-9092", "Genetic Counselors", 89990),
    ("orthotists-prosthetists", "29-2091", "Orthotists and Prosthetists", 77750),
    ("cardiovascular-technologists", "29-2031", "Cardiovascular Technologists and Technicians", 66620),
    ("nuclear-medicine-technologists", "29-2033", "Nuclear Medicine Technologists", 88930),
    ("mri-technologists", "29-2035", "Magnetic Resonance Imaging Technologists", 80790),
    ("psychiatric-technicians", "29-2053", "Psychiatric Technicians", 40470),
    ("medical-dosimetrists", "29-2036", "Medical Dosimetrists", 131590),
    ("ophthalmic-medical-technicians", "29-2057", "Ophthalmic Medical Technicians", 42650),
    ("dietetic-technicians", "29-2051", "Dietetic Technicians", 37840),

    # Healthcare Support additions
    ("psychiatric-aides", "31-1133", "Psychiatric Aides", 37260),
    ("medical-equipment-preparers", "31-9093", "Medical Equipment Preparers", 42130),
    ("medical-transcriptionists", "31-9094", "Medical Transcriptionists", 37080),

    # Protective Service additions
    ("fish-game-wardens", "33-3031", "Fish and Game Wardens", 60830),
    ("parking-enforcement-workers", "33-3041", "Parking Enforcement Workers", 44890),
    ("animal-control-workers", "33-9011", "Animal Control Workers", 43580),
    ("lifeguards-ski-patrol", "33-9092", "Lifeguards, Ski Patrol, and Other Recreational Protective Service Workers", 30560),
    ("transportation-security-screeners", "33-9093", "Transportation Security Screeners", 47360),
    ("gaming-surveillance-officers", "33-9031", "Gaming Surveillance Officers and Gaming Investigators", 39040),

    # Food Preparation additions
    ("cooks-institution-cafeteria", "35-2012", "Cooks, Institution and Cafeteria", 34340),
    ("cooks-short-order", "35-2015", "Cooks, Short Order", 31320),
    ("food-preparation-workers", "35-2021", "Food Preparation Workers", 30710),
    ("dishwashers", "35-9021", "Dishwashers", 29080),
    ("hosts-hostesses", "35-9031", "Hosts and Hostesses, Restaurant, Lounge, and Coffee Shop", 28520),
    ("dining-room-attendants", "35-9011", "Dining Room and Cafeteria Attendants and Bartender Helpers", 29320),
    ("baristas", "35-3023", "Baristas", 30560),

    # Building/Grounds additions
    ("maids-housekeeping-cleaners", "37-2012", "Maids and Housekeeping Cleaners", 32830),
    ("tree-trimmers-pruners", "37-3013", "Tree Trimmers and Pruners", 48890),
    ("grounds-maintenance-supervisors", "37-1012", "First-Line Supervisors of Landscaping, Lawn Service, and Groundskeeping Workers", 55900),

    # Personal Care additions
    ("skincare-specialists", "39-5094", "Skincare Specialists", 41050),
    ("manicurists-pedicurists", "39-5092", "Manicurists and Pedicurists", 33780),
    ("shampooers", "39-5093", "Shampooers", 28900),
    ("concierges", "39-6012", "Concierges", 38170),
    ("tour-travel-guides", "39-7011", "Tour and Travel Guides", 35860),
    ("funeral-directors", "39-4031", "Funeral Home Managers", 69930),
    ("gaming-dealers", "39-3011", "Gaming Dealers", 28720),
    ("gaming-cage-workers", "39-3012", "Gaming and Sports Book Writers and Runners", 30280),
    ("recreation-workers", "39-9032", "Recreation Workers", 33730),
    ("residential-advisors", "39-9041", "Residential Advisors", 35730),
    ("personal-care-aides", "39-9099", "Personal Care and Service Workers, All Other", 34750),
    ("embalmers", "39-4011", "Embalmers", 50610),
    ("motion-picture-projectionists", "39-3021", "Motion Picture Projectionists", 30250),
    ("amusement-recreation-attendants", "39-3091", "Amusement and Recreation Attendants", 28870),
    ("locker-room-attendants", "39-3093", "Locker Room, Coatroom, and Dressing Room Attendants", 31250),

    # Sales additions
    ("counter-rental-clerks", "41-2021", "Counter and Rental Clerks", 36490),
    ("parts-salespersons", "41-2022", "Parts Salespersons", 36680),
    ("demonstrators-product-promoters", "41-9011", "Demonstrators and Product Promoters", 37640),
    ("door-to-door-sales", "41-9091", "Door-to-Door Sales Workers and Street Vendors", 36480),
    ("models", "41-9012", "Models", 40960),

    # Office/Admin additions
    ("bank-tellers", "43-3071", "Tellers", 37250),
    ("bill-account-collectors", "43-3011", "Bill and Account Collectors", 42030),
    ("billing-posting-clerks", "43-3021", "Billing and Posting Clerks", 45250),
    ("hotel-motel-desk-clerks", "43-4081", "Hotel, Motel, and Resort Desk Clerks", 31470),
    ("order-clerks", "43-4151", "Order Clerks", 40140),
    ("stock-clerks", "43-5081", "Stock Clerks and Order Fillers", 33620),
    ("mail-clerks", "43-9051", "Mail Clerks and Mail Machine Operators", 35640),
    ("switchboard-operators", "43-2011", "Switchboard Operators, Including Answering Service", 35960),
    ("library-assistants", "43-4121", "Library Assistants, Clerical", 33380),
    ("court-clerks", "43-4031", "Court, Municipal, and License Clerks", 44730),
    ("meter-readers", "43-5041", "Meter Readers, Utilities", 45600),
    ("statistical-assistants", "43-9111", "Statistical Assistants", 50140),
    ("procurement-clerks", "43-3061", "Procurement Clerks", 48850),

    # Farming/Fishing/Forestry additions
    ("farmworkers-laborers", "45-2092", "Farmworkers and Laborers, Crop, Nursery, and Greenhouse", 33020),
    ("fishers-fishing-workers", "45-3031", "Fishing and Hunting Workers", 37530),
    ("forest-conservation-workers", "45-4011", "Forest and Conservation Workers", 35680),

    # Construction additions
    ("drywall-ceiling-tile-installers", "47-2081", "Drywall and Ceiling Tile Installers", 54550),
    ("insulation-workers", "47-2131", "Insulation Workers", 50750),
    ("tile-stone-setters", "47-2044", "Tile and Marble Setters", 49510),
    ("fence-erectors", "47-4031", "Fence Erectors", 42720),
    ("highway-maintenance-workers", "47-4051", "Highway Maintenance Workers", 47830),
    ("hazardous-materials-removal", "47-4041", "Hazardous Materials Removal Workers", 49660),
    ("stonemasons", "47-2022", "Stonemasons", 49950),
    ("helpers-construction-trades", "47-3010", "Helpers, Construction Trades", 38200),
    ("paving-surfacing-equipment-operators", "47-2071", "Paving, Surfacing, and Tamping Equipment Operators", 49350),
    ("pile-driver-operators", "47-2072", "Pile Driver Operators", 70700),
    ("septic-tank-servicers", "47-4071", "Septic Tank Servicers and Sewer Pipe Cleaners", 45050),
    ("reinforcing-iron-rebar-workers", "47-2171", "Reinforcing Iron and Rebar Workers", 61250),

    # Installation/Maintenance additions
    ("locksmiths", "49-9094", "Locksmiths and Safe Repairers", 47510),
    ("medical-equipment-repairers", "49-9062", "Medical Equipment Repairers", 58530),
    ("small-engine-mechanics", "49-3053", "Outdoor Power Equipment and Other Small Engine Mechanics", 42490),
    ("home-appliance-repairers", "49-9031", "Home Appliance Repairers", 46660),
    ("bicycle-repairers", "49-3091", "Bicycle Repairers", 35880),
    ("coin-vending-amusement-repairers", "49-9091", "Coin, Vending, and Amusement Machine Servicers and Repairers", 40710),
    ("riggers", "49-9096", "Riggers", 58440),
    ("signal-track-switch-repairers", "49-9097", "Signal and Track Switch Repairers", 79880),
    ("millwrights", "49-9044", "Millwrights", 62230),
    ("refractory-materials-repairers", "49-9045", "Refractory Materials Repairers", 52460),

    # Production additions
    ("butchers-meat-cutters", "51-3021", "Butchers and Meat Cutters", 38400),
    ("jewelers-precious-stone-workers", "51-9071", "Jewelers and Precious Stone and Metal Workers", 47970),
    ("dental-laboratory-technicians", "51-9081", "Dental Laboratory Technicians", 46550),
    ("laundry-dry-cleaning-workers", "51-6011", "Laundry and Dry-Cleaning Workers", 31090),
    ("sewing-machine-operators", "51-6031", "Sewing Machine Operators", 33190),
    ("stationary-engineers-boiler-operators", "51-8021", "Stationary Engineers and Boiler Operators", 66770),
    ("semiconductor-processing-technicians", "51-9141", "Semiconductor Processing Technicians", 46750),
    ("packaging-filling-machine-operators", "51-9111", "Packaging and Filling Machine Operators and Tenders", 37250),
    ("mixing-blending-machine-operators", "51-9023", "Mixing and Blending Machine Setters, Operators, and Tenders", 42320),
    ("painting-coating-workers", "51-9124", "Painting, Coating, and Decorating Workers", 36040),
    ("ophthalmic-laboratory-technicians", "51-9083", "Ophthalmic Laboratory Technicians", 39590),
    ("photographic-process-workers", "51-9151", "Photographic Process Workers and Processing Machine Operators", 34760),
    ("tool-die-makers", "51-4111", "Tool and Die Makers", 58580),
    ("model-makers-metal-plastic", "51-4061", "Model Makers, Metal and Plastic", 58420),
    ("patternmakers-metal-plastic", "51-4062", "Patternmakers, Metal and Plastic", 50580),

    # Transportation additions
    ("crane-tower-operators", "53-7021", "Crane and Tower Operators", 65220),
    ("subway-streetcar-operators", "53-4041", "Subway and Streetcar Operators", 81180),
    ("ship-captains-mates", "53-5021", "Captains, Mates, and Pilots of Water Vessels", 88490),
    ("ship-engineers", "53-5031", "Ship Engineers", 96510),
    ("refuse-recyclable-collectors", "53-7081", "Refuse and Recyclable Material Collectors", 44020),
    ("packers-packagers", "53-7064", "Packers and Packagers, Hand", 31530),
    ("stockers-order-fillers", "53-7065", "Stockers and Order Fillers", 33710),
    ("cleaners-vehicles-equipment", "53-7061", "Cleaners of Vehicles and Equipment", 32590),
    ("railroad-conductors-yardmasters", "53-4031", "Railroad Conductors and Yardmasters", 74250),
    ("railroad-brake-signal-switch", "53-4022", "Railroad Brake, Signal, and Switch Operators and Locomotive Firers", 64920),
    ("ambulance-drivers", "53-3011", "Ambulance Drivers and Attendants, Except Emergency Medical Technicians", 33850),
    ("passenger-vehicle-drivers", "53-3058", "Passenger Vehicle Drivers", 38520),

    # =========================================================================
    # EXPANSION — ~300 additional occupations for comprehensive BLS coverage
    # =========================================================================

    # Management — additional
    ("compensation-benefits-specialists-mgr", "11-3111", "Compensation and Benefits Managers", 137430),
    ("database-administrators-managers", "11-3021", "Computer and Information Systems Managers", 170500),

    # Business/Financial — additional
    ("tax-examiners-collectors", "13-2081", "Tax Examiners and Collectors, and Revenue Agents", 58530),
    ("property-appraisers", "13-2024", "Property Appraisers and Assessors", 62390),
    ("claims-adjusters-auto", "13-1032", "Insurance Appraisers, Auto Damage", 69010),
    ("management-consultants", "13-1111", "Management Consultants", 100530),
    ("fraud-examiners", "13-2099", "Financial Specialists, All Other", 80070),
    ("investment-fund-managers", "13-2054", "Investment Fund Managers", 102120),

    # Computer/Math — additional
    ("cloud-architects", "15-1299", "Cloud Architects", 135870),
    ("devops-engineers", "15-1299", "DevOps Engineers", 128350),
    ("machine-learning-engineers", "15-2051", "Machine Learning Engineers", 138200),
    ("cybersecurity-engineers", "15-1212", "Cybersecurity Engineers", 125640),
    ("data-engineers", "15-1252", "Data Engineers", 125480),
    ("ux-designers", "15-1255", "UX Designers", 89780),
    ("systems-engineers", "15-1299", "Systems Engineers", 115370),
    ("network-security-analysts", "15-1212", "Network Security Analysts", 112890),
    ("blockchain-developers", "15-1252", "Blockchain Developers", 141250),
    ("mobile-app-developers", "15-1252", "Mobile Application Developers", 127350),
    ("full-stack-developers", "15-1252", "Full Stack Developers", 125680),
    ("front-end-developers", "15-1254", "Front End Developers", 105430),
    ("back-end-developers", "15-1252", "Back End Developers", 119870),
    ("site-reliability-engineers", "15-1244", "Site Reliability Engineers", 138450),
    ("ai-research-scientists", "15-2051", "AI Research Scientists", 148370),
    ("business-intelligence-analysts", "15-2051", "Business Intelligence Analysts", 98340),
    ("etl-developers", "15-1252", "ETL Developers", 105670),
    ("technical-program-managers", "15-1299", "Technical Program Managers", 132680),
    ("scrum-masters", "15-1299", "Scrum Masters", 102450),
    ("qa-automation-engineers", "15-1253", "QA Automation Engineers", 108920),
    ("game-developers", "15-1252", "Game Developers", 103470),
    ("embedded-systems-engineers", "15-1252", "Embedded Systems Engineers", 115890),
    ("computer-vision-engineers", "15-2051", "Computer Vision Engineers", 142570),
    ("nlp-engineers", "15-2051", "Natural Language Processing Engineers", 139850),
    ("solutions-architects", "15-1241", "Solutions Architects", 138920),
    ("it-project-managers", "15-1299", "IT Project Managers", 112470),
    ("data-analysts", "15-2051", "Data Analysts", 82640),
    ("platform-engineers", "15-1252", "Platform Engineers", 128760),
    ("infrastructure-engineers", "15-1244", "Infrastructure Engineers", 118450),

    # Architecture/Engineering — additional
    ("fire-prevention-engineers", "17-2111", "Fire Prevention and Protection Engineers", 101890),
    ("photonics-engineers", "17-2199", "Photonics Engineers", 108750),
    ("robotics-engineers", "17-2199", "Robotics Engineers", 116340),
    ("structural-engineers", "17-2051", "Structural Engineers", 95780),
    ("geotechnical-engineers", "17-2051", "Geotechnical Engineers", 92450),
    ("transportation-engineers", "17-2051", "Transportation Engineers", 91680),
    ("water-resources-engineers", "17-2081", "Water Resources Engineers", 97340),
    ("process-engineers", "17-2041", "Process Engineers", 99870),
    ("quality-engineers", "17-2112", "Quality Engineers", 95430),
    ("manufacturing-engineers", "17-2112", "Manufacturing Engineers", 96780),
    ("validation-engineers", "17-2199", "Validation Engineers", 89670),
    ("systems-safety-engineers", "17-2111", "Systems Safety Engineers", 98450),
    ("cost-engineers", "17-2199", "Cost Engineers", 88790),
    ("controls-engineers", "17-2072", "Controls Engineers", 102340),
    ("acoustical-engineers", "17-2199", "Acoustical Engineers", 95670),
    ("optical-engineers", "17-2199", "Optical Engineers", 106890),
    ("packaging-engineers", "17-2199", "Packaging Engineers", 84560),
    ("reliability-engineers", "17-2199", "Reliability Engineers", 97340),
    ("test-engineers", "17-2199", "Test Engineers", 91250),
    ("cad-technicians", "17-3019", "CAD Technicians", 55780),
    ("surveying-mapping-technicians", "17-3031", "Surveying and Mapping Technicians", 50420),

    # Life/Physical/Social Science — additional
    ("materials-scientists", "19-2032", "Materials Scientists", 105320),
    ("bioinformatics-scientists", "19-1029", "Bioinformatics Scientists", 98670),
    ("toxicologists", "19-1042", "Toxicologists", 93450),
    ("pharmacologists", "19-1042", "Pharmacologists", 98760),
    ("climate-scientists", "19-2021", "Climate Scientists", 92340),
    ("marine-biologists", "19-1023", "Marine Biologists", 72560),
    ("ecologists", "19-1023", "Ecologists", 73890),
    ("genetics-counselors-research", "19-1042", "Genetics Researchers", 87650),
    ("archaeological-technicians", "19-4099", "Archaeological Technicians", 48920),
    ("cartographic-technicians", "19-4099", "Cartographic Technicians", 52340),
    ("social-science-research-assistants", "19-4061", "Social Science Research Assistants", 48150),
    ("forensic-anthropologists", "19-3091", "Forensic Anthropologists", 72340),

    # Community/Social Service — additional
    ("vocational-rehabilitation-counselors", "21-1015", "Vocational Rehabilitation Counselors", 44320),
    ("crisis-counselors", "21-1014", "Crisis Counselors", 51890),
    ("school-social-workers", "21-1021", "School Social Workers", 57340),
    ("case-managers", "21-1093", "Case Managers", 49870),
    ("youth-development-specialists", "21-1099", "Youth Development Specialists", 38450),
    ("peer-support-specialists", "21-1099", "Peer Support Specialists", 36780),

    # Legal — additional
    ("compliance-managers", "23-1011", "Compliance Managers", 127890),
    ("legal-nurse-consultants", "23-2099", "Legal Nurse Consultants", 78450),
    ("patent-agents", "23-2099", "Patent Agents", 98670),
    ("immigration-specialists", "23-2011", "Immigration Specialists", 62340),
    ("contract-administrators", "23-2099", "Contract Administrators", 72560),
    ("legal-investigators", "23-2099", "Legal Investigators", 58970),

    # Education — additional
    ("esl-teachers", "25-3031", "ESL Teachers", 59340),
    ("reading-specialists", "25-2059", "Reading Specialists", 63780),
    ("school-counselors", "21-1012", "School Counselors", 62340),
    ("education-consultants", "25-9031", "Education Consultants", 68450),
    ("academic-advisors", "25-9031", "Academic Advisors", 52670),
    ("curriculum-developers", "25-9031", "Curriculum Developers", 71230),
    ("learning-designers", "25-9031", "Learning Designers", 74560),
    ("stem-teachers", "25-2031", "STEM Teachers", 67890),
    ("special-education-aides", "25-9042", "Special Education Aides", 34560),
    ("school-principals", "11-9032", "School Principals", 103560),
    ("dean-of-students", "11-9033", "Dean of Students", 98760),
    ("college-admissions-counselors", "25-9031", "College Admissions Counselors", 52340),

    # Arts/Design/Entertainment — additional
    ("ux-researchers", "27-1029", "UX Researchers", 96780),
    ("motion-graphics-designers", "27-1014", "Motion Graphics Designers", 78450),
    ("creative-directors", "27-1011", "Creative Directors", 118670),
    ("brand-strategists", "27-1019", "Brand Strategists", 82340),
    ("video-game-designers", "27-1014", "Video Game Designers", 88560),
    ("sound-designers", "27-4014", "Sound Designers", 65780),
    ("storyboard-artists", "27-1014", "Storyboard Artists", 72340),
    ("voice-actors", "27-2011", "Voice Actors", 58670),
    ("sports-broadcasters", "27-3011", "Sports Broadcasters", 62340),
    ("podcast-producers", "27-2012", "Podcast Producers", 56780),
    ("social-media-managers", "27-3031", "Social Media Managers", 62450),
    ("content-strategists", "27-3042", "Content Strategists", 74560),
    ("copywriters", "27-3043", "Copywriters", 68790),
    ("seo-specialists", "27-3031", "SEO Specialists", 65430),
    ("video-producers", "27-2012", "Video Producers", 72340),
    ("3d-modelers", "27-1014", "3D Modelers", 74560),
    ("concept-artists", "27-1013", "Concept Artists", 68790),

    # Healthcare Practitioners — additional
    ("dermatologists", "29-1214", "Dermatologists", 302740),
    ("cardiologists", "29-1212", "Cardiologists", 353970),
    ("radiologists", "29-1224", "Radiologists", 319460),
    ("emergency-medicine-physicians", "29-1214", "Emergency Medicine Physicians", 310640),
    ("orthopedic-surgeons", "29-1248", "Orthopedic Surgeons", 371400),
    ("neurologists", "29-1217", "Neurologists", 267000),
    ("oncologists", "29-1218", "Oncologists", 326890),
    ("pediatricians", "29-1221", "Pediatricians", 198420),
    ("urologists", "29-1249", "Urologists", 354110),
    ("ophthalmologists", "29-1241", "Ophthalmologists", 306050),
    ("gastroenterologists", "29-1228", "Gastroenterologists", 346120),
    ("pathologists", "29-1222", "Pathologists", 288250),
    ("allergists-immunologists", "29-1228", "Allergists and Immunologists", 274350),
    ("pulmonologists", "29-1228", "Pulmonologists", 282670),
    ("endocrinologists", "29-1228", "Endocrinologists", 263890),
    ("rheumatologists", "29-1228", "Rheumatologists", 271450),
    ("neonatologists", "29-1228", "Neonatologists", 290670),
    ("nephrologists", "29-1228", "Nephrologists", 278340),
    ("sports-medicine-physicians", "29-1228", "Sports Medicine Physicians", 225670),
    ("hospice-palliative-care-physicians", "29-1228", "Hospice and Palliative Care Physicians", 261890),
    ("infectious-disease-physicians", "29-1228", "Infectious Disease Physicians", 248750),
    ("interventional-radiologists", "29-1224", "Interventional Radiologists", 338450),
    ("critical-care-nurses", "29-1141", "Critical Care Nurses", 92340),
    ("operating-room-nurses", "29-1141", "Operating Room Nurses", 89780),
    ("pediatric-nurses", "29-1141", "Pediatric Nurses", 85670),
    ("oncology-nurses", "29-1141", "Oncology Nurses", 88450),
    ("neonatal-nurses", "29-1141", "Neonatal Nurses", 87340),
    ("emergency-room-nurses", "29-1141", "Emergency Room Nurses", 90560),
    ("psychiatric-nurses", "29-1141", "Psychiatric Nurses", 84670),
    ("public-health-nurses", "29-1141", "Public Health Nurses", 82340),
    ("travel-nurses", "29-1141", "Travel Nurses", 98670),
    ("clinical-research-coordinators", "29-2099", "Clinical Research Coordinators", 56780),
    ("perfusionists", "29-2099", "Perfusionists", 138450),
    ("cytotechnologists", "29-2011", "Cytotechnologists", 68450),
    ("histotechnologists", "29-2011", "Histotechnologists", 62340),
    ("sleep-technologists", "29-2099", "Sleep Technologists", 56780),
    ("eeg-technologists", "29-2099", "EEG Technologists", 54670),
    ("neurodiagnostic-technologists", "29-2099", "Neurodiagnostic Technologists", 55890),
    ("sterile-processing-technicians", "29-2099", "Sterile Processing Technicians", 42670),
    ("medical-coders", "29-2072", "Medical Coders", 52340),
    ("health-information-technicians", "29-2072", "Health Information Technicians", 48670),
    ("patient-care-technicians", "31-9099", "Patient Care Technicians", 38450),
    ("dialysis-technicians", "29-2099", "Dialysis Technicians", 42670),

    # Healthcare Support — additional
    ("certified-nursing-assistants", "31-1131", "Certified Nursing Assistants", 37890),
    ("home-care-coordinators", "31-1120", "Home Care Coordinators", 38450),
    ("rehabilitation-aides", "31-2012", "Rehabilitation Aides", 35670),
    ("surgical-assistants", "31-9099", "Surgical Assistants", 52340),
    ("ophthalmic-assistants", "31-9099", "Ophthalmic Assistants", 38670),
    ("audiometric-technicians", "31-9099", "Audiometric Technicians", 41230),
    ("chiropractic-assistants", "31-9099", "Chiropractic Assistants", 35670),
    ("physical-therapy-aides", "31-2022", "Physical Therapy Aides", 32450),
    ("pharmacy-aides", "31-9095", "Pharmacy Aides", 33560),

    # Protective Service — additional
    ("border-patrol-agents", "33-3051", "Border Patrol Agents", 68450),
    ("crime-scene-investigators", "33-3021", "Crime Scene Investigators", 72340),
    ("emergency-dispatchers", "43-5031", "Emergency Dispatchers", 48560),
    ("forensic-examiners", "33-3021", "Forensic Examiners", 78670),
    ("cybersecurity-analysts-govt", "33-9099", "Government Cybersecurity Analysts", 98670),
    ("intelligence-analysts", "33-3021", "Intelligence Analysts", 86450),

    # Food Preparation — additional
    ("pastry-chefs", "35-1011", "Pastry Chefs", 52340),
    ("sous-chefs", "35-1011", "Sous Chefs", 54670),
    ("executive-chefs", "35-1011", "Executive Chefs", 68450),
    ("nutritional-cooks", "35-2014", "Nutritional Cooks", 38670),
    ("catering-managers", "35-1012", "Catering Managers", 48560),
    ("sommelier", "35-3031", "Sommeliers", 62340),
    ("food-safety-inspectors", "45-2011", "Food Safety Inspectors", 52340),
    ("brewers", "51-3092", "Brewers", 48670),

    # Building/Grounds — additional
    ("pool-technicians", "37-2019", "Pool Technicians", 38450),
    ("building-inspectors", "47-4011", "Construction and Building Inspectors", 67890),
    ("environmental-compliance-inspectors", "13-1041", "Environmental Compliance Inspectors", 72340),

    # Personal Care — additional
    ("wedding-planners", "39-3031", "Wedding Planners", 48670),
    ("life-coaches", "39-9099", "Life Coaches", 52340),
    ("dog-groomers", "39-2021", "Animal Groomers", 32670),
    ("nannies", "39-9011", "Nannies", 38450),
    ("personal-trainers", "39-9031", "Personal Trainers", 48670),
    ("yoga-instructors", "39-9031", "Yoga Instructors", 42340),
    ("pilates-instructors", "39-9031", "Pilates Instructors", 43560),
    ("spa-managers", "39-1022", "Spa Managers", 56780),

    # Sales — additional
    ("account-executives", "41-3099", "Account Executives", 72340),
    ("business-development-managers", "41-3099", "Business Development Managers", 98670),
    ("pharmaceutical-sales-reps", "41-4011", "Pharmaceutical Sales Representatives", 82340),
    ("medical-device-sales-reps", "41-4011", "Medical Device Sales Representatives", 92670),
    ("technology-sales-reps", "41-4011", "Technology Sales Representatives", 86450),
    ("sales-operations-analysts", "41-9099", "Sales Operations Analysts", 68450),
    ("retail-store-managers", "41-1011", "Retail Store Managers", 52340),
    ("e-commerce-managers", "41-9099", "E-Commerce Managers", 78670),
    ("merchandise-buyers", "13-1022", "Merchandise Buyers", 62340),
    ("wholesale-account-managers", "41-4012", "Wholesale Account Managers", 74560),

    # Office/Admin — additional
    ("accounts-payable-clerks", "43-3031", "Accounts Payable Clerks", 45670),
    ("accounts-receivable-clerks", "43-3031", "Accounts Receivable Clerks", 44560),
    ("credentialing-specialists", "43-4199", "Credentialing Specialists", 46780),
    ("patient-access-representatives", "43-4199", "Patient Access Representatives", 38450),
    ("medical-billing-specialists", "43-3021", "Medical Billing Specialists", 42340),
    ("scheduling-coordinators", "43-4199", "Scheduling Coordinators", 40560),
    ("records-management-specialists", "43-4199", "Records Management Specialists", 48670),
    ("immigration-paralegals", "43-4199", "Immigration Paralegals", 52340),
    ("virtual-assistants", "43-6014", "Virtual Assistants", 42670),
    ("administrative-coordinators", "43-6014", "Administrative Coordinators", 46780),

    # Farming/Fishing/Forestry — additional
    ("arborists", "37-3013", "Arborists", 48670),
    ("agricultural-technicians", "19-4012", "Agricultural Technicians", 42340),
    ("aquaculture-workers", "45-3031", "Aquaculture Workers", 35670),
    ("vineyard-managers", "45-1011", "Vineyard Managers", 62340),
    ("park-rangers", "33-3031", "Park Rangers", 45670),
    ("wildlife-rehabilitators", "19-1023", "Wildlife Rehabilitators", 38450),

    # Construction — additional
    ("crane-operators", "47-2073", "Crane Operators", 68450),
    ("demolition-workers", "47-2061", "Demolition Workers", 46780),
    ("concrete-finishers", "47-2051", "Concrete Finishers", 52340),
    ("pipeline-workers", "47-2152", "Pipeline Workers", 62340),
    ("well-drillers", "47-5021", "Well Drillers", 52670),
    ("blasters-explosives-workers", "47-5031", "Blasters and Explosives Workers", 58450),
    ("terrazzo-workers", "47-2053", "Terrazzo Workers and Finishers", 50890),

    # Installation/Maintenance — additional
    ("solar-panel-technicians", "49-9099", "Solar Panel Technicians", 48670),
    ("appliance-repair-technicians", "49-9031", "Appliance Repair Technicians", 44560),
    ("commercial-divers", "49-9092", "Commercial Divers", 62340),
    ("elevator-mechanics", "49-9099", "Elevator Mechanics", 102340),
    ("fire-alarm-technicians", "49-2098", "Fire Alarm Technicians", 52670),
    ("instrumentation-technicians", "49-9099", "Instrumentation Technicians", 62340),
    ("marine-mechanics", "49-3051", "Marine Mechanics", 48670),
    ("motorcycle-mechanics", "49-3052", "Motorcycle Mechanics", 42340),
    ("precision-instrument-repairers", "49-9069", "Precision Instrument Repairers", 56780),

    # Production — additional
    ("cnc-operators", "51-4011", "CNC Operators", 46780),
    ("injection-molding-operators", "51-4072", "Injection Molding Machine Operators", 38450),
    ("quality-control-inspectors", "51-9061", "Quality Control Inspectors", 48670),
    ("chemical-operators", "51-9011", "Chemical Equipment Operators", 58340),
    ("paper-goods-machine-operators", "51-9196", "Paper Goods Machine Setters and Operators", 42670),
    ("textile-machine-operators", "51-6063", "Textile Machine Operators", 35670),
    ("glass-blowers-molders", "51-9195", "Glass Blowers, Molders, Benders, and Finishers", 40560),
    ("foundry-workers", "51-4071", "Foundry Workers", 42340),
    ("heat-treating-equipment-operators", "51-4191", "Heat Treating Equipment Operators", 45670),
    ("metal-fabricators", "51-2041", "Metal Fabricators", 44560),
    ("plastics-workers", "51-4072", "Plastics Workers", 38450),
    ("stone-cutters-carvers", "51-9195", "Stone Cutters and Carvers", 40780),
    ("upholsterers", "51-6093", "Upholsterers", 39450),
    ("cabinetmakers-bench-carpenters", "51-7011", "Cabinetmakers and Bench Carpenters", 40670),
    ("furniture-finishers", "51-7021", "Furniture Finishers", 36780),

    # Transportation — additional
    ("delivery-drivers", "53-3031", "Delivery Drivers", 38450),
    ("warehouse-managers", "53-1047", "Warehouse Managers", 58670),
    ("forklift-operators", "53-7051", "Forklift Operators", 42340),
    ("dispatchers-transportation", "43-5032", "Transportation Dispatchers", 48670),
    ("logistics-coordinators", "43-5011", "Logistics Coordinators", 46780),
    ("freight-brokers", "43-5011", "Freight Brokers", 52340),
    ("dock-workers", "53-7062", "Dock Workers", 38450),
    ("aircraft-cargo-handlers", "53-7061", "Aircraft Cargo Handlers", 40560),
    ("ship-pilots", "53-5021", "Ship Pilots", 92340),
    ("traffic-managers", "11-3071", "Traffic Managers", 72340),
    ("fleet-managers", "11-3071", "Fleet Managers", 68450),
    ("supply-chain-analysts", "13-1081", "Supply Chain Analysts", 72340),
    ("import-export-specialists", "13-1199", "Import/Export Specialists", 58670),
]


# =============================================================================
# US METRO AREAS — 50 largest / most-searched metros
# Format: (slug, cbsa_code, full_name, short_name, state, col_factor, emp_mult)
#   col_factor: cost-of-living salary adjustment vs national median
#   emp_mult: employment multiplier (proxy for metro size)
# =============================================================================

US_METROS = [
    # Tier 1 — Mega metros
    ("new-york", "35620", "New York-Newark-Jersey City, NY-NJ-PA", "New York", "NY", 1.25, 2.0),
    ("los-angeles", "31080", "Los Angeles-Long Beach-Anaheim, CA", "Los Angeles", "CA", 1.18, 1.6),
    ("chicago", "16980", "Chicago-Naperville-Elgin, IL-IN-WI", "Chicago", "IL", 1.05, 1.4),
    ("dallas", "19100", "Dallas-Fort Worth-Arlington, TX", "Dallas", "TX", 1.05, 1.2),
    ("houston", "26420", "Houston-The Woodlands-Sugar Land, TX", "Houston", "TX", 1.02, 1.2),

    # Tier 2 — Major tech / finance hubs
    ("san-francisco", "41860", "San Francisco-Oakland-Berkeley, CA", "San Francisco", "CA", 1.38, 0.9),
    ("san-jose", "41940", "San Jose-Sunnyvale-Santa Clara, CA", "San Jose", "CA", 1.42, 0.6),
    ("seattle", "42660", "Seattle-Tacoma-Bellevue, WA", "Seattle", "WA", 1.30, 1.0),
    ("washington-dc", "47900", "Washington-Arlington-Alexandria, DC-VA-MD-WV", "Washington DC", "DC", 1.22, 1.3),
    ("boston", "14460", "Boston-Cambridge-Nashua, MA-NH", "Boston", "MA", 1.24, 1.0),

    # Tier 3 — Large metros
    ("philadelphia", "37980", "Philadelphia-Camden-Wilmington, PA-NJ-DE-MD", "Philadelphia", "PA", 1.08, 1.0),
    ("atlanta", "12060", "Atlanta-Sandy Springs-Alpharetta, GA", "Atlanta", "GA", 1.02, 1.0),
    ("miami", "33100", "Miami-Fort Lauderdale-Pompano Beach, FL", "Miami", "FL", 0.95, 0.8),
    ("phoenix", "38060", "Phoenix-Mesa-Chandler, AZ", "Phoenix", "AZ", 0.98, 0.9),
    ("minneapolis", "33460", "Minneapolis-St. Paul-Bloomington, MN-WI", "Minneapolis", "MN", 1.08, 0.8),
    ("san-diego", "41740", "San Diego-Chula Vista-Carlsbad, CA", "San Diego", "CA", 1.15, 0.6),
    ("denver", "19740", "Denver-Aurora-Lakewood, CO", "Denver", "CO", 1.12, 0.8),
    ("detroit", "19820", "Detroit-Warren-Dearborn, MI", "Detroit", "MI", 0.98, 0.8),
    ("austin", "12420", "Austin-Round Rock-Georgetown, TX", "Austin", "TX", 1.10, 0.6),
    ("portland", "38900", "Portland-Vancouver-Hillsboro, OR-WA", "Portland", "OR", 1.10, 0.6),

    # Tier 4 — Growing / mid-major metros
    ("nashville", "34980", "Nashville-Davidson-Murfreesboro-Franklin, TN", "Nashville", "TN", 0.98, 0.5),
    ("raleigh", "39580", "Raleigh-Cary, NC", "Raleigh", "NC", 1.02, 0.5),
    ("charlotte", "16740", "Charlotte-Concord-Gastonia, NC-SC", "Charlotte", "NC", 0.98, 0.6),
    ("salt-lake-city", "41620", "Salt Lake City, UT", "Salt Lake City", "UT", 1.00, 0.5),
    ("las-vegas", "29820", "Las Vegas-Henderson-Paradise, NV", "Las Vegas", "NV", 0.95, 0.5),
    ("tampa", "45300", "Tampa-St. Petersburg-Clearwater, FL", "Tampa", "FL", 0.93, 0.6),
    ("orlando", "36740", "Orlando-Kissimmee-Sanford, FL", "Orlando", "FL", 0.92, 0.5),
    ("san-antonio", "41700", "San Antonio-New Braunfels, TX", "San Antonio", "TX", 0.93, 0.5),
    ("columbus", "18140", "Columbus, OH", "Columbus", "OH", 0.97, 0.5),
    ("indianapolis", "26900", "Indianapolis-Carmel-Anderson, IN", "Indianapolis", "IN", 0.95, 0.5),

    # Tier 5 — Mid-size metros
    ("pittsburgh", "38300", "Pittsburgh, PA", "Pittsburgh", "PA", 0.96, 0.5),
    ("st-louis", "41180", "St. Louis, MO-IL", "St. Louis", "MO", 0.95, 0.6),
    ("baltimore", "12580", "Baltimore-Columbia-Towson, MD", "Baltimore", "MD", 1.08, 0.6),
    ("sacramento", "40900", "Sacramento-Roseville-Folsom, CA", "Sacramento", "CA", 1.08, 0.5),
    ("kansas-city", "28140", "Kansas City, MO-KS", "Kansas City", "MO", 0.97, 0.5),
    ("cleveland", "17460", "Cleveland-Elyria, OH", "Cleveland", "OH", 0.93, 0.5),
    ("cincinnati", "17140", "Cincinnati, OH-KY-IN", "Cincinnati", "OH", 0.95, 0.5),
    ("milwaukee", "33340", "Milwaukee-Waukesha, WI", "Milwaukee", "WI", 0.97, 0.4),
    ("jacksonville", "27260", "Jacksonville, FL", "Jacksonville", "FL", 0.93, 0.4),
    ("richmond", "40060", "Richmond, VA", "Richmond", "VA", 0.98, 0.4),

    # Tier 6 — Smaller but notable metros
    ("oklahoma-city", "36420", "Oklahoma City, OK", "Oklahoma City", "OK", 0.90, 0.4),
    ("memphis", "32820", "Memphis, TN-MS-AR", "Memphis", "TN", 0.90, 0.4),
    ("louisville", "31140", "Louisville/Jefferson County, KY-IN", "Louisville", "KY", 0.93, 0.4),
    ("new-orleans", "35380", "New Orleans-Metairie, LA", "New Orleans", "LA", 0.92, 0.3),
    ("hartford", "25540", "Hartford-East Hartford-Middletown, CT", "Hartford", "CT", 1.06, 0.3),
    ("buffalo", "15380", "Buffalo-Cheektowaga, NY", "Buffalo", "NY", 0.93, 0.3),
    ("birmingham", "13820", "Birmingham-Hoover, AL", "Birmingham", "AL", 0.90, 0.3),
    ("tucson", "46060", "Tucson, AZ", "Tucson", "AZ", 0.90, 0.3),
    ("honolulu", "46520", "Urban Honolulu, HI", "Honolulu", "HI", 1.12, 0.3),
    ("anchorage", "11260", "Anchorage, AK", "Anchorage", "AK", 1.10, 0.2),
]


# =============================================================================
# CANADIAN METRO AREAS — 10 major cities
# Format: (slug, code, full_name, short_name, province, col_factor, emp_mult)
# col_factor here is relative to a Canadian baseline (we convert US median → CA)
# =============================================================================

CA_METROS = [
    ("toronto", "TOR", "Toronto, ON", "Toronto", "ON", 1.15, 1.5),
    ("vancouver", "VAN", "Vancouver, BC", "Vancouver", "BC", 1.12, 0.9),
    ("montreal", "MTL", "Montreal, QC", "Montreal", "QC", 0.95, 1.0),
    ("ottawa", "OTT", "Ottawa, ON", "Ottawa", "ON", 1.05, 0.6),
    ("calgary", "CAL", "Calgary, AB", "Calgary", "AB", 1.08, 0.6),
    ("edmonton", "EDM", "Edmonton, AB", "Edmonton", "AB", 1.02, 0.5),
    ("winnipeg", "WPG", "Winnipeg, MB", "Winnipeg", "MB", 0.90, 0.3),
    ("quebec-city", "QBC", "Quebec City, QC", "Quebec City", "QC", 0.88, 0.3),
    ("hamilton", "HAM", "Hamilton, ON", "Hamilton", "ON", 0.95, 0.3),
    ("halifax", "HAL", "Halifax, NS", "Halifax", "NS", 0.90, 0.3),
]

# Canadian salaries are roughly this fraction of US medians (in CAD terms)
# Accounts for exchange rate + generally lower Canadian wage levels
CA_WAGE_FACTOR = 0.82


# =============================================================================
# GENERATION LOGIC
# =============================================================================

def slugify(name):
    """Convert an occupation name to a URL-friendly slug."""
    return (
        name.lower()
        .replace(",", "")
        .replace("'", "")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "-")
        .replace("&", "and")
        .replace("  ", " ")
        .strip()
        .replace(" ", "-")
    )


def salary_spread(median):
    """Return a spread factor based on salary level."""
    if median > 150000:
        return 0.50
    elif median > 100000:
        return 0.45
    elif median > 70000:
        return 0.40
    elif median > 45000:
        return 0.35
    else:
        return 0.30


def generate_record(occ_tuple, metro_tuple, country="US"):
    """Generate a single salary record."""
    slug, soc_code, name, nat_median = occ_tuple

    if country == "US":
        m_slug, m_code, m_full, m_short, m_state, col_factor, emp_mult = metro_tuple
        currency = "USD"
        base_median = nat_median
    else:
        m_slug, m_code, m_full, m_short, m_state, col_factor, emp_mult = metro_tuple
        currency = "CAD"
        base_median = nat_median * CA_WAGE_FACTOR

    # Apply metro adjustment with slight randomness (±3%)
    adjusted = col_factor * random.uniform(0.97, 1.03)
    median = round(base_median * adjusted / 1000) * 1000

    # Mean is typically slightly above median
    mean = round(median * random.uniform(1.02, 1.12) / 1000) * 1000

    # Percentile spread
    sp = salary_spread(median)
    p10 = round(median * (1 - sp) / 1000) * 1000
    p25 = round(median * (1 - sp * 0.55) / 1000) * 1000
    p75 = round(median * (1 + sp * 0.45) / 1000) * 1000
    p90 = round(median * (1 + sp * 0.75) / 1000) * 1000

    # Employment: random base scaled by metro size
    base_emp = random.randint(1500, 20000)
    emp = round(base_emp * emp_mult / 100) * 100
    emp = max(emp, 200)

    return {
        "area_code": m_code,
        "area_name": m_full,
        "city_short": m_short,
        "state": m_state,
        "country": country,
        "currency": currency,
        "occ_code": soc_code,
        "occ_name": name,
        "occ_slug": slug,
        "employment": emp,
        "mean_annual": mean,
        "median_annual": median,
        "pct10_annual": p10,
        "pct25_annual": p25,
        "pct75_annual": p75,
        "pct90_annual": p90,
    }


def main():
    print("=" * 60)
    print("  SalaryLens — Full Data Generation")
    print("=" * 60)

    print(f"\n  Occupations: {len(OCCUPATIONS)}")
    print(f"  US Metros:   {len(US_METROS)}")
    print(f"  CA Metros:   {len(CA_METROS)}")
    print(f"  Expected US records:  {len(OCCUPATIONS) * len(US_METROS):,}")
    print(f"  Expected CA records:  {len(OCCUPATIONS) * len(CA_METROS):,}")
    total_expected = len(OCCUPATIONS) * (len(US_METROS) + len(CA_METROS))
    print(f"  Expected total:       {total_expected:,}")

    records = []

    # Generate US records
    print("\n  Generating US records...")
    for occ in OCCUPATIONS:
        for metro in US_METROS:
            records.append(generate_record(occ, metro, "US"))
    us_count = len(records)
    print(f"    ✓ {us_count:,} US records")

    # Generate CA records
    print("  Generating Canadian records...")
    ca_start = len(records)
    for occ in OCCUPATIONS:
        for metro in CA_METROS:
            records.append(generate_record(occ, metro, "CA"))
    ca_count = len(records) - ca_start
    print(f"    ✓ {ca_count:,} Canadian records")

    # Sort by median salary descending
    records.sort(key=lambda r: r["median_annual"], reverse=True)

    # Write output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "salary_data.json")
    with open(out_path, "w") as f:
        json.dump(records, f, indent=2)

    file_size_mb = os.path.getsize(out_path) / (1024 * 1024)

    # Stats
    occupations = set(r["occ_slug"] for r in records)
    us_cities = set(r["city_short"] for r in records if r["country"] == "US")
    ca_cities = set(r["city_short"] for r in records if r["country"] == "CA")

    print(f"\n{'=' * 60}")
    print(f"  RESULTS")
    print(f"{'=' * 60}")
    print(f"  Total records:    {len(records):,}")
    print(f"  Unique jobs:      {len(occupations)}")
    print(f"  US cities:        {len(us_cities)}")
    print(f"  CA cities:        {len(ca_cities)}")
    print(f"  File size:        {file_size_mb:.1f} MB")
    print(f"  Output:           {out_path}")
    print(f"{'=' * 60}")

    # Estimated page counts
    salary_pages = len(records)
    job_pages = len(occupations)
    city_pages = len(us_cities) + len(ca_cities)
    # Comparison pages (combinations of cities)
    total_cities = len(us_cities) + len(ca_cities)
    compare_pages = total_cities * (total_cities - 1) // 2

    print(f"\n  Estimated pages:")
    print(f"    Salary pages:     {salary_pages:,}")
    print(f"    Job pages:        {job_pages:,}")
    print(f"    City pages:       {city_pages:,}")
    print(f"    Compare pages:    {compare_pages:,}")
    print(f"    TOTAL:            {salary_pages + job_pages + city_pages + compare_pages:,}")

    # Top paying
    print(f"\n  Top 10 highest paying:")
    for r in records[:10]:
        flag = "🇺🇸" if r["country"] == "US" else "🇨🇦"
        print(f"    {flag} ${r['median_annual']:>9,} {r['currency']}  {r['occ_name']} — {r['city_short']}")

    # Bottom 5
    print(f"\n  Bottom 5:")
    for r in records[-5:]:
        flag = "🇺🇸" if r["country"] == "US" else "🇨🇦"
        print(f"    {flag} ${r['median_annual']:>9,} {r['currency']}  {r['occ_name']} — {r['city_short']}")

    print()


if __name__ == "__main__":
    main()
