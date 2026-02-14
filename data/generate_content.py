"""
Generate content enrichment for SalaryLens pages.

Creates two JSON files:
  - occupation_content.json — career descriptions, skills, education, tips per occupation
  - city_content.json — job market overviews, industries, cost of living per city

Content is template-based (no API needed). Uses SOC major group templates with
occupation-specific variable substitution for uniqueness.
"""

import json
import os
import hashlib

# Import occupation list from the data generator
from generate_full_data import OCCUPATIONS, US_METROS, CA_METROS

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "next-app", "src", "lib")


# =============================================================================
# SOC MAJOR GROUP TEMPLATES
# =============================================================================

SOC_GROUPS = {
    "11": {
        "group_name": "Management",
        "descriptions": [
            "{name} plan, direct, and coordinate the operational activities of organizations. They formulate policies, manage daily operations, and make key decisions that shape business strategy and organizational direction.",
            "{name} oversee teams and departments, setting goals and ensuring that resources are allocated efficiently. Their leadership drives organizational performance and helps achieve both short-term targets and long-term objectives.",
            "{name} are responsible for guiding their organizations toward success by managing budgets, developing strategies, and building high-performing teams. They play a critical role in shaping company culture and operational efficiency.",
        ],
        "skills": ["Leadership", "Strategic Planning", "Budgeting", "Decision Making", "Team Management", "Communication", "Problem Solving", "Project Management", "Negotiation", "Organizational Development"],
        "education": "Bachelor's degree in business, management, or a related field",
        "education_detail": "Most positions require a bachelor's degree, with many employers preferring candidates who hold an MBA or master's degree in a relevant discipline. Significant work experience in the field is typically required before moving into management.",
        "outlook": "Employment is projected to grow about as fast as average, with demand driven by organizational expansion and the need for skilled leadership across industries.",
        "tips": [
            "Pursue an MBA or advanced management certification",
            "Develop expertise in data-driven decision making and analytics",
            "Build a track record of measurable business results",
            "Expand your professional network through industry conferences and associations",
            "Gain experience managing cross-functional teams and projects",
            "Stay current with industry trends and emerging technologies",
            "Develop strong financial literacy and budgeting skills",
        ],
        "work_env": "Most work in office settings, though travel to satellite locations or client sites may be required. Long hours and high-pressure situations are common, especially during critical business periods.",
    },
    "13": {
        "group_name": "Business and Financial Operations",
        "descriptions": [
            "{name} support organizational operations by analyzing financial data, managing business processes, and ensuring compliance with regulations. Their analytical skills help organizations make informed decisions and operate efficiently.",
            "{name} work at the intersection of business strategy and operational execution. They analyze trends, manage projects, and develop recommendations that help organizations optimize performance and manage risk.",
            "{name} play a vital role in keeping organizations running smoothly by managing financial records, evaluating business processes, and providing insights that drive strategic decision-making.",
        ],
        "skills": ["Financial Analysis", "Data Analysis", "Excel", "Communication", "Problem Solving", "Attention to Detail", "Project Management", "Research", "Regulatory Compliance", "Critical Thinking"],
        "education": "Bachelor's degree in business, finance, accounting, or a related field",
        "education_detail": "A bachelor's degree is the minimum requirement for most positions. Professional certifications such as CPA, CFA, or PMP can significantly enhance career prospects and earning potential.",
        "outlook": "Employment is expected to grow faster than average as organizations increasingly rely on data analysis and financial planning to guide business decisions.",
        "tips": [
            "Earn professional certifications relevant to your specialty (CPA, CFA, PMP)",
            "Develop advanced Excel and data visualization skills",
            "Learn business intelligence tools like Tableau or Power BI",
            "Build expertise in regulatory compliance and risk management",
            "Pursue a master's degree in business, finance, or analytics",
            "Develop strong presentation and communication skills",
            "Stay current with changes in financial regulations and standards",
        ],
        "work_env": "Most work in office environments with standard business hours. Some positions may require travel for audits, client meetings, or conferences.",
    },
    "15": {
        "group_name": "Computer and Mathematical",
        "descriptions": [
            "{name} design, develop, and maintain technology solutions that power modern businesses and organizations. They work with software, hardware, networks, and data to solve complex technical challenges and create innovative products.",
            "{name} apply technical expertise and analytical thinking to build and optimize computer systems, applications, and digital infrastructure. Their work enables organizations to leverage technology for competitive advantage.",
            "{name} are at the forefront of technological innovation, creating software applications, managing IT infrastructure, and analyzing data to drive business insights. Their skills are essential in virtually every industry.",
        ],
        "skills": ["Programming", "Problem Solving", "Software Development", "Data Analysis", "Cloud Computing", "Cybersecurity", "Database Management", "Version Control", "Agile Methodologies", "System Design"],
        "education": "Bachelor's degree in computer science, information technology, or a related field",
        "education_detail": "A bachelor's degree in computer science or a related field is standard. However, many roles also value practical experience, coding bootcamp credentials, and industry certifications from AWS, Google, Microsoft, or other major tech companies.",
        "outlook": "Employment is projected to grow much faster than average, driven by the increasing reliance on technology across all industries and the growing demand for cybersecurity, cloud computing, and data science expertise.",
        "tips": [
            "Master in-demand programming languages and frameworks",
            "Earn cloud certifications (AWS, Azure, or GCP)",
            "Build a strong portfolio of projects on GitHub",
            "Specialize in high-growth areas like AI/ML, cybersecurity, or cloud architecture",
            "Contribute to open-source projects to build your reputation",
            "Stay current with rapidly evolving technologies and tools",
            "Develop soft skills like communication and teamwork alongside technical abilities",
        ],
        "work_env": "Most work in office settings or remotely, with many companies offering flexible or fully remote arrangements. Standard hours are common, though project deadlines may occasionally require additional time.",
    },
    "17": {
        "group_name": "Architecture and Engineering",
        "descriptions": [
            "{name} apply scientific and mathematical principles to design, develop, and evaluate systems, structures, and processes. Their technical expertise helps solve practical problems and bring innovative designs to life.",
            "{name} combine creativity with technical knowledge to design and improve products, structures, and systems. They work on projects ranging from buildings and bridges to electronics and manufacturing processes.",
            "{name} use their expertise in math, science, and design to create solutions for real-world challenges. Whether working on infrastructure, products, or systems, they ensure that designs are safe, efficient, and functional.",
        ],
        "skills": ["CAD Software", "Technical Drawing", "Problem Solving", "Mathematics", "Project Management", "Quality Control", "Analytical Thinking", "Regulatory Compliance", "Technical Writing", "Teamwork"],
        "education": "Bachelor's degree in engineering, architecture, or a related technical field",
        "education_detail": "A bachelor's degree in engineering or a related field is required. Many positions also require professional licensure (PE license for engineers, architectural license for architects). A master's degree can lead to advanced positions.",
        "outlook": "Employment is expected to grow about as fast as average, with demand for engineers and architects driven by infrastructure needs, technology development, and environmental sustainability initiatives.",
        "tips": [
            "Obtain your Professional Engineer (PE) license or architectural license",
            "Learn advanced CAD and simulation software tools",
            "Specialize in high-demand areas like renewable energy or sustainable design",
            "Pursue a master's degree or professional certifications",
            "Develop project management skills alongside technical expertise",
            "Stay current with building codes, regulations, and industry standards",
            "Build experience with emerging technologies like 3D printing and BIM",
        ],
        "work_env": "Work environments vary from offices and laboratories to construction sites and manufacturing plants. Some positions require travel to project sites or client locations.",
    },
    "19": {
        "group_name": "Life, Physical, and Social Science",
        "descriptions": [
            "{name} conduct research and analysis to expand our understanding of the natural and social world. Their discoveries and insights contribute to advances in medicine, technology, environmental protection, and public policy.",
            "{name} apply the scientific method to study natural phenomena, human behavior, or social systems. Their research helps solve complex problems and informs evidence-based decision making across many fields.",
            "{name} investigate and analyze data to advance scientific knowledge and develop practical applications. Their work spans laboratories, field sites, and research institutions, contributing to breakthroughs that benefit society.",
        ],
        "skills": ["Research Methods", "Data Analysis", "Statistical Software", "Scientific Writing", "Laboratory Techniques", "Critical Thinking", "Attention to Detail", "Presentation Skills", "Grant Writing", "Peer Review"],
        "education": "Master's or doctoral degree in a relevant scientific discipline",
        "education_detail": "Many research positions require a master's or doctoral degree. Some entry-level technician roles may accept a bachelor's degree. Postdoctoral research experience is common for academic and senior research positions.",
        "outlook": "Employment is expected to grow about as fast as average, with increasing demand for research in areas like environmental science, healthcare, and data analysis.",
        "tips": [
            "Publish research in peer-reviewed journals to build your professional reputation",
            "Develop strong statistical analysis and programming skills (R, Python, SAS)",
            "Pursue postdoctoral research opportunities for academic career advancement",
            "Apply for research grants from government agencies and private foundations",
            "Build a professional network through conferences and professional associations",
            "Develop expertise in interdisciplinary research methods",
            "Consider industry positions for higher earning potential outside academia",
        ],
        "work_env": "Work settings include research laboratories, field locations, offices, and academic institutions. Hours can be irregular, especially when conducting experiments or fieldwork.",
    },
    "21": {
        "group_name": "Community and Social Service",
        "descriptions": [
            "{name} help individuals and communities navigate challenges and access support services. They provide counseling, case management, and advocacy to improve quality of life for the people they serve.",
            "{name} work directly with individuals, families, and communities to address social, emotional, and behavioral challenges. Their compassion and expertise help people overcome obstacles and build healthier lives.",
            "{name} play a crucial role in supporting vulnerable populations and strengthening communities. They connect people with resources, provide guidance, and advocate for systemic changes that promote well-being.",
        ],
        "skills": ["Active Listening", "Empathy", "Case Management", "Crisis Intervention", "Cultural Competency", "Communication", "Documentation", "Group Facilitation", "Community Outreach", "Conflict Resolution"],
        "education": "Bachelor's or master's degree in social work, counseling, or a related field",
        "education_detail": "Requirements vary by role. Some positions accept a bachelor's degree, while clinical and counseling roles typically require a master's degree and state licensure. Ongoing continuing education is usually required to maintain credentials.",
        "outlook": "Employment is projected to grow faster than average, driven by increased demand for mental health services and community support programs.",
        "tips": [
            "Obtain relevant state licensure or certification (LCSW, LPC, etc.)",
            "Specialize in a high-demand area such as substance abuse or trauma counseling",
            "Pursue a master's degree in social work or counseling for clinical roles",
            "Develop cultural competency and multilingual skills",
            "Build experience through internships and volunteer work",
            "Stay current with evidence-based therapeutic approaches",
            "Consider supervision credentials to advance into leadership roles",
        ],
        "work_env": "Work settings include social service agencies, schools, hospitals, community centers, and private practices. Many roles involve direct client interaction and may require evening or weekend hours.",
    },
    "23": {
        "group_name": "Legal",
        "descriptions": [
            "{name} work within the legal system to advise clients, represent parties in legal proceedings, and ensure compliance with laws and regulations. Their expertise helps individuals and organizations navigate complex legal matters.",
            "{name} apply knowledge of the law to resolve disputes, draft legal documents, and protect the rights of individuals and organizations. They play an essential role in maintaining justice and the rule of law.",
            "{name} provide legal expertise that helps individuals and organizations understand their rights and obligations. Whether in courtrooms, offices, or government agencies, they ensure that legal processes are followed correctly.",
        ],
        "skills": ["Legal Research", "Writing", "Critical Thinking", "Negotiation", "Attention to Detail", "Public Speaking", "Client Management", "Analytical Reasoning", "Document Drafting", "Case Management"],
        "education": "Juris Doctor (JD) degree for lawyers; associate's or bachelor's degree for support roles",
        "education_detail": "Lawyers must earn a Juris Doctor degree from an accredited law school and pass the state bar exam. Paralegals and legal assistants typically need an associate's or bachelor's degree, and some earn professional certifications.",
        "outlook": "Employment is expected to grow about as fast as average, with demand for legal services continuing across corporate, government, and private practice settings.",
        "tips": [
            "Specialize in a high-demand legal area (intellectual property, healthcare law, cybersecurity law)",
            "Build a strong professional network through bar associations and legal organizations",
            "Develop expertise in legal technology and e-discovery tools",
            "Consider additional certifications or an LLM for specialized practice areas",
            "Gain trial experience or develop alternative dispute resolution skills",
            "Stay current with changes in laws and regulations in your practice area",
            "Develop business development skills to build your client base",
        ],
        "work_env": "Most work in law firms, corporate legal departments, government agencies, or courtrooms. Hours can be long, especially for attorneys working on complex cases or transactions.",
    },
    "25": {
        "group_name": "Educational Instruction and Library",
        "descriptions": [
            "{name} educate students and facilitate learning across various settings and age groups. They develop curricula, create engaging lessons, and assess student progress to foster academic and personal growth.",
            "{name} shape the next generation by teaching, mentoring, and inspiring students. They create supportive learning environments and adapt their teaching methods to meet diverse student needs.",
            "{name} play a fundamental role in education by delivering instruction, developing educational materials, and supporting student development. Their work builds the foundation for lifelong learning and career readiness.",
        ],
        "skills": ["Lesson Planning", "Classroom Management", "Communication", "Patience", "Adaptability", "Assessment Design", "Technology Integration", "Differentiated Instruction", "Student Engagement", "Curriculum Development"],
        "education": "Bachelor's degree in education or a subject area; state teaching license for K-12",
        "education_detail": "K-12 teachers need a bachelor's degree and state teaching certification. Postsecondary teachers typically need a master's or doctoral degree. Librarians usually need a master's degree in library science (MLS).",
        "outlook": "Employment is expected to grow about as fast as average, with demand varying by region, subject area, and grade level. Special education and STEM teachers are typically in highest demand.",
        "tips": [
            "Earn additional certifications in high-demand subject areas",
            "Pursue a master's degree for salary advancement on the pay scale",
            "Develop expertise in educational technology and online instruction",
            "Seek National Board Certification for recognition and salary increases",
            "Consider administrative credentials for leadership positions",
            "Build skills in special education or English language learner instruction",
            "Engage in professional development and continuing education regularly",
        ],
        "work_env": "Most work in schools, colleges, universities, or libraries during academic terms. K-12 teachers follow the school calendar, while postsecondary instructors may have more flexible schedules.",
    },
    "27": {
        "group_name": "Arts, Design, Entertainment, Sports, and Media",
        "descriptions": [
            "{name} use their creative talents to communicate ideas, entertain audiences, and produce visual, written, or performance-based works. Their creativity drives culture, media, and the design of products and experiences.",
            "{name} bring ideas to life through artistic expression, design, and storytelling. They work across diverse media and platforms to create content that informs, entertains, and inspires audiences.",
            "{name} combine artistic skill with technical knowledge to create compelling content and designs. Whether working in visual arts, media production, or performance, they shape how people experience culture and information.",
        ],
        "skills": ["Creativity", "Design Software", "Communication", "Collaboration", "Time Management", "Attention to Detail", "Visual Storytelling", "Adaptability", "Client Management", "Portfolio Development"],
        "education": "Bachelor's degree in fine arts, design, communications, or a related field",
        "education_detail": "Education requirements vary widely. Many positions value a strong portfolio and practical experience as much as formal education. A bachelor's degree is common, but talent, creativity, and a compelling body of work are often most important.",
        "outlook": "Employment growth varies by specialty, but overall demand is expected to grow about as fast as average. Digital media, UX design, and content creation roles are among the fastest-growing areas.",
        "tips": [
            "Build a strong, diverse portfolio showcasing your best work",
            "Master industry-standard software and tools for your specialty",
            "Develop a personal brand and online presence to attract opportunities",
            "Network actively through industry events, social media, and professional groups",
            "Stay current with design trends and emerging technologies",
            "Develop complementary business skills like marketing and client management",
            "Consider freelancing or contract work to diversify your income",
        ],
        "work_env": "Work settings vary widely, from studios and offices to on-location shoots and performance venues. Many creative professionals work as freelancers or on a project basis, with irregular schedules.",
    },
    "29": {
        "group_name": "Healthcare Practitioners and Technical",
        "descriptions": [
            "{name} diagnose and treat patients, provide specialized medical care, and work to improve health outcomes. Their clinical expertise and compassion are essential to the healthcare system.",
            "{name} apply medical knowledge and clinical skills to assess, diagnose, and treat health conditions. They work in hospitals, clinics, and private practices to deliver care that improves patients' quality of life.",
            "{name} are essential healthcare providers who combine scientific knowledge with patient-centered care. They perform examinations, interpret diagnostic tests, and develop treatment plans to address a wide range of health issues.",
        ],
        "skills": ["Clinical Assessment", "Patient Care", "Medical Knowledge", "Critical Thinking", "Communication", "Attention to Detail", "Electronic Health Records", "Teamwork", "Empathy", "Continuing Education"],
        "education": "Doctoral or professional degree for physicians; bachelor's or associate's for technicians",
        "education_detail": "Requirements range from associate's degrees for technicians to doctoral degrees for physicians. Most practitioners require professional licensure or certification. Continuing education is mandatory to maintain credentials.",
        "outlook": "Employment is projected to grow much faster than average, driven by an aging population, advances in medical technology, and increased access to healthcare services.",
        "tips": [
            "Pursue board certification in your specialty for higher earning potential",
            "Stay current with medical research and evidence-based practices",
            "Develop subspecialty expertise in a high-demand area",
            "Consider leadership roles in healthcare administration",
            "Build experience with electronic health records and health informatics",
            "Pursue advanced degrees or fellowships for career advancement",
            "Develop strong patient communication and bedside manner skills",
        ],
        "work_env": "Work settings include hospitals, clinics, private practices, and outpatient care centers. Many healthcare professionals work shifts, including nights, weekends, and holidays. The work can be physically and emotionally demanding.",
    },
    "31": {
        "group_name": "Healthcare Support",
        "descriptions": [
            "{name} provide essential support services in healthcare settings, assisting nurses, physicians, and other medical professionals with patient care and clinical tasks.",
            "{name} help patients and medical staff by performing routine clinical tasks, maintaining equipment, and ensuring that healthcare facilities run smoothly. Their support is critical to delivering quality patient care.",
            "{name} work directly with patients to provide basic care, comfort, and assistance with daily activities. They serve as a vital link between patients and the healthcare professionals who oversee their treatment.",
        ],
        "skills": ["Patient Care", "Medical Terminology", "CPR/First Aid", "Communication", "Physical Stamina", "Attention to Detail", "Compassion", "Infection Control", "Vital Signs Monitoring", "Electronic Health Records"],
        "education": "High school diploma or equivalent; postsecondary certificate for some roles",
        "education_detail": "Many healthcare support roles require a high school diploma and on-the-job training. Some positions, such as physical therapy assistants or dental hygienists, require an associate's degree or postsecondary certificate. State certification may be required.",
        "outlook": "Employment is projected to grow much faster than average, as healthcare facilities need more support staff to care for an aging population.",
        "tips": [
            "Earn certifications to qualify for higher-paying specialized roles",
            "Consider advancing to a licensed practical nurse or registered nurse role",
            "Develop skills in specialized areas like dialysis or surgical assistance",
            "Pursue additional education for career advancement opportunities",
            "Build strong relationships with supervising healthcare professionals",
            "Stay current with infection control protocols and safety standards",
            "Consider bilingual skills to serve diverse patient populations",
        ],
        "work_env": "Most work in hospitals, nursing care facilities, clinics, or patients' homes. The work is physically demanding, often requiring standing, lifting, and assisting patients. Shifts may include nights and weekends.",
    },
    "33": {
        "group_name": "Protective Service",
        "descriptions": [
            "{name} protect the public by enforcing laws, responding to emergencies, and ensuring community safety. They work in law enforcement, firefighting, corrections, and security roles.",
            "{name} serve their communities by maintaining public safety, preventing crime, and responding to emergency situations. Their training and vigilance help protect lives and property.",
            "{name} are dedicated to safeguarding individuals and communities. Whether patrolling streets, fighting fires, or monitoring security, they put themselves at risk to keep others safe.",
        ],
        "skills": ["Physical Fitness", "Situational Awareness", "Communication", "Decision Making", "Conflict Resolution", "Emergency Response", "Report Writing", "Teamwork", "De-escalation", "First Aid"],
        "education": "High school diploma to bachelor's degree, depending on the role",
        "education_detail": "Requirements vary significantly. Police officers typically need some college education or a degree. Firefighters usually need a high school diploma plus fire academy training. Federal law enforcement positions often require a bachelor's degree.",
        "outlook": "Employment is expected to grow about as fast as average, with ongoing need for public safety professionals in communities of all sizes.",
        "tips": [
            "Maintain excellent physical fitness to meet job demands and pass fitness tests",
            "Pursue advanced training and specialized certifications",
            "Earn a bachelor's degree in criminal justice for federal or detective roles",
            "Develop leadership skills for promotion to supervisory positions",
            "Build expertise in emerging areas like cybercrime or digital forensics",
            "Consider bilingual skills for serving diverse communities",
            "Pursue lateral moves to specialized units for higher pay and career growth",
        ],
        "work_env": "Work environments vary from patrol vehicles and offices to outdoor posts and emergency scenes. Many roles require shift work, including nights, weekends, and holidays. The work can be physically demanding and stressful.",
    },
    "35": {
        "group_name": "Food Preparation and Serving",
        "descriptions": [
            "{name} prepare, cook, and serve food in restaurants, hotels, cafeterias, and other dining establishments. They ensure that meals are prepared safely and presented appealingly to satisfy customers.",
            "{name} work in the food service industry, preparing ingredients, cooking meals, and serving customers. Their skills and dedication help create enjoyable dining experiences for patrons.",
            "{name} play an essential role in the food service industry, from preparing ingredients and cooking dishes to serving customers and maintaining clean, safe kitchen environments.",
        ],
        "skills": ["Food Safety", "Cooking Techniques", "Time Management", "Teamwork", "Customer Service", "Menu Knowledge", "Physical Stamina", "Knife Skills", "Inventory Management", "Multitasking"],
        "education": "High school diploma or equivalent; culinary degree for advanced roles",
        "education_detail": "Many positions require little formal education beyond a high school diploma. Chefs and head cooks often benefit from culinary school training or apprenticeships. On-the-job training is common across all levels.",
        "outlook": "Employment is expected to grow about as fast as average, driven by continued demand for dining out and food delivery services.",
        "tips": [
            "Complete culinary school or an apprenticeship for advanced chef roles",
            "Earn food safety certifications (ServSafe, food handler's card)",
            "Develop expertise in a culinary specialty (pastry, international cuisine, etc.)",
            "Build management skills to advance to head chef or restaurant manager",
            "Stay current with food trends and dietary preferences",
            "Consider catering or private chef work for higher earning potential",
            "Build a reputation through competitions, social media, or food publications",
        ],
        "work_env": "Most work in restaurant kitchens, cafeterias, or food service establishments. Hours are often long and irregular, including evenings, weekends, and holidays. Kitchens can be hot, fast-paced, and physically demanding.",
    },
    "37": {
        "group_name": "Building and Grounds Cleaning and Maintenance",
        "descriptions": [
            "{name} keep buildings, grounds, and facilities clean, safe, and well-maintained. Their work ensures that properties look their best and meet health and safety standards.",
            "{name} maintain the appearance and functionality of buildings and outdoor spaces. They perform cleaning, landscaping, and maintenance tasks that create pleasant environments for occupants and visitors.",
            "{name} are responsible for the upkeep of buildings, grounds, and facilities. Their work ranges from routine cleaning and landscaping to specialized maintenance tasks that keep properties in top condition.",
        ],
        "skills": ["Physical Stamina", "Attention to Detail", "Equipment Operation", "Time Management", "Safety Awareness", "Customer Service", "Groundskeeping", "Cleaning Techniques", "Basic Repairs", "Chemical Safety"],
        "education": "High school diploma or equivalent; on-the-job training",
        "education_detail": "Most positions require a high school diploma and provide on-the-job training. Some specialized roles, like pest control technicians, may require state certification. Supervisory roles may prefer some college education.",
        "outlook": "Employment is expected to grow about as fast as average, with steady demand for maintenance and cleaning services across commercial and residential properties.",
        "tips": [
            "Obtain certifications for specialized services (pest control, pool maintenance, etc.)",
            "Develop supervisory skills to advance to management positions",
            "Learn equipment maintenance and repair for greater versatility",
            "Consider starting your own cleaning or landscaping business",
            "Build expertise in green cleaning or sustainable landscaping practices",
            "Pursue training in building systems (HVAC, electrical, plumbing basics)",
            "Develop client relationship skills for service-oriented roles",
        ],
        "work_env": "Work is primarily performed outdoors or in buildings, often requiring physical labor. Exposure to weather, cleaning chemicals, and heavy equipment is common. Hours may include early mornings, evenings, or weekends.",
    },
    "39": {
        "group_name": "Personal Care and Service",
        "descriptions": [
            "{name} provide a range of personal services that enhance clients' well-being, appearance, and quality of life. They work in settings from salons and spas to private homes and entertainment venues.",
            "{name} help people look and feel their best by providing personal care, fitness guidance, and lifestyle services. Their work focuses on meeting individual client needs and creating positive experiences.",
            "{name} deliver personalized services that improve clients' physical appearance, wellness, or daily lives. They build strong client relationships and take pride in the quality of care they provide.",
        ],
        "skills": ["Customer Service", "Communication", "Physical Stamina", "Creativity", "Time Management", "Attention to Detail", "Interpersonal Skills", "Sales Ability", "Hygiene Practices", "Patience"],
        "education": "High school diploma; postsecondary training or state license for some roles",
        "education_detail": "Requirements vary widely. Cosmetologists and barbers need state licensure, which typically requires completing an approved training program. Fitness trainers benefit from professional certifications. Childcare workers may need CPR certification.",
        "outlook": "Employment is expected to grow about as fast as average, with demand for personal care services driven by population growth and consumer spending on health and wellness.",
        "tips": [
            "Obtain required state licenses and professional certifications",
            "Build a loyal client base through excellent service and word-of-mouth referrals",
            "Develop skills in high-demand specialties within your field",
            "Consider opening your own business or working as an independent contractor",
            "Stay current with trends and new techniques in your specialty",
            "Build a social media presence to attract new clients",
            "Pursue continuing education to expand your service offerings",
        ],
        "work_env": "Work settings include salons, spas, fitness centers, private homes, and entertainment venues. Many work evenings and weekends to accommodate client schedules. Some roles are physically demanding.",
    },
    "41": {
        "group_name": "Sales and Related",
        "descriptions": [
            "{name} drive revenue by selling products and services to individuals and businesses. They build relationships with customers, identify their needs, and present solutions that deliver value.",
            "{name} connect customers with products and services that meet their needs. They use product knowledge, persuasion skills, and relationship-building to close deals and generate revenue for their organizations.",
            "{name} are essential to business growth, using their interpersonal skills and product expertise to engage customers, negotiate deals, and achieve sales targets across various industries.",
        ],
        "skills": ["Communication", "Persuasion", "Customer Relationship Management", "Product Knowledge", "Negotiation", "Goal Setting", "CRM Software", "Active Listening", "Presentation Skills", "Prospecting"],
        "education": "High school diploma for retail; bachelor's degree for B2B and specialized sales",
        "education_detail": "Retail sales positions typically require a high school diploma. Business-to-business sales, technical sales, and sales management roles often require a bachelor's degree. Professional sales certifications can boost career prospects.",
        "outlook": "Employment is expected to grow about as fast as average, with particularly strong demand for sales professionals in technology, healthcare, and financial services.",
        "tips": [
            "Develop deep product knowledge and industry expertise",
            "Master CRM software and sales automation tools",
            "Build strong negotiation and closing skills",
            "Pursue sales certifications or training programs",
            "Develop expertise in consultative or solution-based selling",
            "Build and maintain a strong professional network",
            "Track your sales metrics and continuously improve your process",
        ],
        "work_env": "Work settings range from retail stores and offices to client sites and remote locations. Travel is common for outside sales roles. Hours may include evenings and weekends, especially in retail.",
    },
    "43": {
        "group_name": "Office and Administrative Support",
        "descriptions": [
            "{name} keep offices and organizations running efficiently by performing administrative tasks, managing records, and supporting daily operations. Their organizational skills are essential to workplace productivity.",
            "{name} provide the administrative backbone of organizations, handling correspondence, scheduling, data entry, and customer interactions that keep business operations on track.",
            "{name} perform essential clerical and administrative tasks that support the smooth operation of offices, businesses, and government agencies. Their attention to detail and organizational skills are highly valued.",
        ],
        "skills": ["Microsoft Office", "Data Entry", "Organization", "Communication", "Customer Service", "Filing", "Scheduling", "Attention to Detail", "Multitasking", "Record Keeping"],
        "education": "High school diploma; associate's degree or certifications for specialized roles",
        "education_detail": "Many positions require a high school diploma with on-the-job training. Specialized roles like medical or legal secretaries may require postsecondary education or certification in their respective fields.",
        "outlook": "Employment is projected to grow slower than average overall, though some specialized roles like medical secretaries continue to see strong demand.",
        "tips": [
            "Master Microsoft Office Suite, especially Excel and Word",
            "Learn industry-specific software and database systems",
            "Develop strong organizational and time management skills",
            "Pursue certifications such as the Certified Administrative Professional (CAP)",
            "Specialize in a high-demand area like medical or legal administration",
            "Develop bookkeeping or accounting skills for expanded responsibilities",
            "Build proficiency with office technology and communication tools",
        ],
        "work_env": "Most work in comfortable office settings during standard business hours. Some positions may require overtime during busy periods. Customer-facing roles involve regular phone and in-person interactions.",
    },
    "45": {
        "group_name": "Farming, Fishing, and Forestry",
        "descriptions": [
            "{name} work in agriculture, fishing, and forestry to produce food, manage natural resources, and maintain ecosystems. Their labor is essential to food production and environmental stewardship.",
            "{name} cultivate crops, raise livestock, harvest fish, or manage forest resources. Their work is deeply connected to the land and natural cycles, requiring physical endurance and practical knowledge.",
            "{name} play a vital role in food production, natural resource management, and environmental conservation. They combine traditional knowledge with modern techniques to sustainably manage agricultural and natural resources.",
        ],
        "skills": ["Equipment Operation", "Physical Stamina", "Agricultural Knowledge", "Weather Awareness", "Animal Husbandry", "Safety Procedures", "Problem Solving", "Mechanical Skills", "Time Management", "Environmental Awareness"],
        "education": "High school diploma; bachelor's degree for management and scientific roles",
        "education_detail": "Many entry-level positions require hands-on experience rather than formal education. Farm managers and agricultural scientists typically need a bachelor's degree. Specialized certifications may be required for pesticide application or forestry work.",
        "outlook": "Employment is projected to show little or no change, as productivity improvements offset the need for additional workers in many agricultural sectors.",
        "tips": [
            "Learn modern agricultural technology and precision farming techniques",
            "Obtain certifications for pesticide application or specialized equipment",
            "Consider organic farming or sustainable agriculture for premium markets",
            "Develop business management skills for farm operation",
            "Stay current with agricultural regulations and sustainability practices",
            "Build expertise in crop science, soil management, or animal nutrition",
            "Explore agritourism or direct-to-consumer sales for additional income",
        ],
        "work_env": "Work is primarily outdoors, often in rural locations. Physical labor is intensive, and hours depend on seasonal demands. Exposure to weather, machinery, and agricultural chemicals is common.",
    },
    "47": {
        "group_name": "Construction and Extraction",
        "descriptions": [
            "{name} build, repair, and maintain structures and infrastructure using specialized skills and equipment. Their craftsmanship is essential to constructing the buildings, roads, and systems that communities depend on.",
            "{name} work on construction sites and extraction operations, applying skilled trades to build and renovate structures. They read blueprints, operate equipment, and ensure that projects meet safety and quality standards.",
            "{name} use their specialized trade skills to construct, renovate, and maintain buildings and infrastructure. They work with a variety of materials and tools to bring construction projects from blueprint to completion.",
        ],
        "skills": ["Blueprint Reading", "Power Tools", "Physical Stamina", "Safety Awareness", "Mathematics", "Teamwork", "Problem Solving", "Manual Dexterity", "Equipment Operation", "Building Codes"],
        "education": "High school diploma plus apprenticeship or trade school training",
        "education_detail": "Most construction trades require a high school diploma followed by an apprenticeship program (typically 3-5 years) or vocational school training. Journeyman and master certifications are available in many trades.",
        "outlook": "Employment is projected to grow about as fast as average, driven by ongoing construction of buildings, roads, and infrastructure, as well as the need for renovation and maintenance of existing structures.",
        "tips": [
            "Complete a formal apprenticeship program to earn journeyman status",
            "Obtain trade-specific licenses and certifications required in your area",
            "Develop skills in multiple trades for greater versatility",
            "Consider specializing in high-demand areas like green building or solar installation",
            "Pursue supervisory training to advance to foreman or project manager",
            "Stay current with building codes and safety regulations",
            "Consider starting your own contracting business once you have experience",
        ],
        "work_env": "Most work outdoors on construction sites, often in varying weather conditions. The work is physically demanding and can be hazardous. Hours may be long during good weather or tight deadlines.",
    },
    "49": {
        "group_name": "Installation, Maintenance, and Repair",
        "descriptions": [
            "{name} install, maintain, and repair equipment, machinery, and systems to keep them running efficiently. Their technical skills help prevent breakdowns and ensure that critical systems operate safely.",
            "{name} troubleshoot, repair, and maintain a wide range of equipment and systems. They use diagnostic tools and technical knowledge to identify problems and restore equipment to proper working condition.",
            "{name} ensure that machinery, vehicles, and equipment function properly through routine maintenance and skilled repairs. Their work minimizes downtime and extends the lifespan of valuable assets.",
        ],
        "skills": ["Troubleshooting", "Mechanical Knowledge", "Electrical Systems", "Hand Tools", "Safety Procedures", "Diagnostic Equipment", "Blueprint Reading", "Physical Stamina", "Attention to Detail", "Customer Service"],
        "education": "High school diploma plus technical training or apprenticeship",
        "education_detail": "Most positions require a high school diploma and postsecondary technical training, apprenticeship, or military training. Industry certifications from manufacturers or professional organizations can enhance career prospects.",
        "outlook": "Employment is expected to grow about as fast as average, as equipment and systems across all industries continue to need installation, maintenance, and repair.",
        "tips": [
            "Earn manufacturer certifications and industry-recognized credentials",
            "Stay current with evolving technology in your specialty area",
            "Develop skills in electrical, plumbing, and HVAC systems for versatility",
            "Consider specializing in high-tech equipment or renewable energy systems",
            "Build strong diagnostic and problem-solving skills",
            "Pursue supervisory training for management advancement",
            "Consider self-employment or starting your own repair business",
        ],
        "work_env": "Work settings vary from shops and factories to customer locations and outdoor sites. The work can be physically demanding, requiring lifting, climbing, and working in confined spaces. Some positions involve travel.",
    },
    "51": {
        "group_name": "Production",
        "descriptions": [
            "{name} operate machinery, assemble products, and oversee manufacturing processes that produce goods used by consumers and businesses. Their precision and attention to quality ensure that products meet exacting standards.",
            "{name} work in manufacturing and processing facilities, operating equipment and performing tasks that transform raw materials into finished products. They ensure production quality and efficiency.",
            "{name} play a key role in the manufacturing process by setting up, operating, and maintaining production equipment. Their skills help ensure that goods are produced efficiently, safely, and to specification.",
        ],
        "skills": ["Machine Operation", "Quality Control", "Safety Awareness", "Attention to Detail", "Physical Stamina", "Mechanical Aptitude", "Blueprint Reading", "Mathematics", "Teamwork", "Problem Solving"],
        "education": "High school diploma; on-the-job training or technical certification",
        "education_detail": "Most positions require a high school diploma with on-the-job training. Skilled trades like machinists and tool and die makers may require apprenticeships or postsecondary technical training. CNC programming roles benefit from formal certification.",
        "outlook": "Employment is projected to decline slightly in some areas due to automation, though skilled positions like CNC operators and quality inspectors remain in demand.",
        "tips": [
            "Learn CNC programming and computer-aided manufacturing (CAM) software",
            "Earn certifications in quality control (Six Sigma, ISO standards)",
            "Develop skills in robotics and automation technology",
            "Pursue training in multiple production processes for versatility",
            "Stay current with manufacturing technology and safety standards",
            "Consider supervisory training for advancement to shift leader or manager",
            "Develop expertise in lean manufacturing and process improvement",
        ],
        "work_env": "Most work in manufacturing plants and factories. The work can be repetitive and physically demanding, requiring standing for long periods and operating heavy machinery. Shift work, including nights and weekends, is common.",
    },
    "53": {
        "group_name": "Transportation and Material Moving",
        "descriptions": [
            "{name} transport people and goods safely and efficiently across roads, railways, waterways, and airways. They operate vehicles, manage logistics, and ensure that deliveries arrive on time.",
            "{name} keep the economy moving by operating vehicles, managing freight, and coordinating the movement of goods and passengers. Their reliability and skill ensure safe, timely transportation.",
            "{name} are essential to commerce and travel, operating everything from trucks and buses to ships and aircraft. They follow safety regulations, maintain vehicles, and ensure efficient transportation of people and cargo.",
        ],
        "skills": ["Vehicle Operation", "Safety Awareness", "Navigation", "Time Management", "Physical Stamina", "Communication", "Attention to Detail", "Logistics", "Customer Service", "Regulatory Compliance"],
        "education": "High school diploma; commercial driver's license (CDL) or specialized training",
        "education_detail": "Requirements vary by role. Truck drivers need a CDL. Airline pilots require an ATP certificate and extensive flight hours. Railroad engineers need on-the-job training. Material movers typically need a high school diploma and on-the-job training.",
        "outlook": "Employment is expected to grow about as fast as average, with particularly strong demand for truck drivers and delivery workers driven by e-commerce growth.",
        "tips": [
            "Obtain required licenses and endorsements for your specialty",
            "Maintain a clean driving record and safety certifications",
            "Consider specialized endorsements (hazmat, tanker, doubles/triples)",
            "Develop logistics and route optimization skills",
            "Stay current with transportation regulations and safety standards",
            "Consider owner-operator status for higher earning potential",
            "Build experience with GPS, ELD, and fleet management technology",
        ],
        "work_env": "Work settings include vehicles, warehouses, airports, ports, and railyards. Hours are often long and irregular, with many roles requiring overnight travel or shift work. Physical demands vary by position.",
    },
}


# =============================================================================
# OCCUPATION-SPECIFIC OVERRIDES (for high-traffic occupations)
# =============================================================================

OCCUPATION_OVERRIDES = {
    "software-developers": {
        "description": "Software developers design, build, test, and maintain software applications and systems that power everything from mobile apps to enterprise platforms. They write code in various programming languages, collaborate with product teams, and solve complex technical problems to create reliable, scalable software solutions.",
        "skills": ["Python", "JavaScript", "Java", "SQL", "Git", "Cloud Computing", "System Design", "Agile/Scrum", "API Development", "Testing"],
    },
    "registered-nurses": {
        "description": "Registered nurses provide and coordinate patient care, educate patients about health conditions, and offer emotional support to patients and their families. They administer medications, monitor vital signs, develop care plans, and work closely with physicians and other healthcare professionals to deliver quality care.",
        "skills": ["Patient Assessment", "Medication Administration", "IV Therapy", "Electronic Health Records", "Critical Thinking", "Communication", "CPR/BLS", "Patient Education", "Wound Care", "Team Collaboration"],
    },
    "data-scientists": {
        "description": "Data scientists analyze large, complex datasets to uncover patterns, build predictive models, and generate actionable insights that drive business decisions. They combine expertise in statistics, programming, and domain knowledge to transform raw data into strategic value for organizations.",
        "skills": ["Python", "R", "SQL", "Machine Learning", "Statistics", "Data Visualization", "TensorFlow/PyTorch", "Big Data Tools", "A/B Testing", "Communication"],
    },
    "physicians-surgeons": {
        "description": "Physicians diagnose and treat injuries and illnesses, prescribe medications, and counsel patients on preventive care. They conduct examinations, order diagnostic tests, interpret results, and develop treatment plans tailored to individual patient needs.",
        "skills": ["Clinical Diagnosis", "Patient Care", "Medical Procedures", "Electronic Health Records", "Research", "Communication", "Decision Making", "Continuing Education", "Surgical Skills", "Team Leadership"],
    },
    "lawyers": {
        "description": "Lawyers advise and represent individuals, businesses, and government agencies on legal issues and disputes. They research laws, draft legal documents, negotiate settlements, and advocate for clients in courtrooms and before regulatory bodies.",
        "skills": ["Legal Research", "Brief Writing", "Oral Advocacy", "Contract Negotiation", "Client Counseling", "Case Strategy", "Regulatory Analysis", "Mediation", "Legal Technology", "Business Development"],
    },
    "financial-analysts": {
        "description": "Financial analysts evaluate investment opportunities, analyze financial data, and provide recommendations that guide business and investment decisions. They build financial models, assess market trends, and prepare reports for management and clients.",
        "skills": ["Financial Modeling", "Excel", "Bloomberg Terminal", "Valuation Methods", "Financial Reporting", "Data Analysis", "Presentation Skills", "Research", "Risk Assessment", "SQL"],
    },
    "accountants-auditors": {
        "description": "Accountants and auditors prepare and examine financial records, ensure accuracy, and verify that taxes are paid properly and on time. They assess financial operations, help organizations run efficiently, and ensure compliance with laws and regulations.",
        "skills": ["GAAP", "Tax Preparation", "Auditing", "Excel", "Financial Reporting", "QuickBooks", "Regulatory Compliance", "Analytical Skills", "Attention to Detail", "ERP Systems"],
    },
    "electricians": {
        "description": "Electricians install, maintain, and repair electrical power, communications, lighting, and control systems in homes, businesses, and industrial facilities. They read blueprints, follow building codes, and ensure that electrical systems are safe and functioning properly.",
        "skills": ["Electrical Systems", "Blueprint Reading", "NEC Code", "Troubleshooting", "Wiring", "Safety Procedures", "Power Tools", "Circuit Testing", "Motor Controls", "Conduit Bending"],
    },
    "graphic-designers": {
        "description": "Graphic designers create visual concepts using computer software or by hand to communicate ideas that inspire, inform, and captivate consumers. They develop layouts and production designs for advertisements, brochures, magazines, websites, and corporate communications.",
        "skills": ["Adobe Creative Suite", "Typography", "Color Theory", "Layout Design", "Branding", "UI Design", "Print Production", "Illustration", "Photography", "Client Communication"],
    },
    "marketing-managers": {
        "description": "Marketing managers plan and direct marketing programs, including market research, pricing strategy, and advertising campaigns. They identify demand for products and services, develop marketing strategies, and oversee the teams that implement these plans.",
        "skills": ["Marketing Strategy", "Digital Marketing", "Brand Management", "Market Research", "Content Marketing", "Analytics", "Budget Management", "Team Leadership", "SEO/SEM", "Social Media"],
    },
}


# =============================================================================
# CITY CONTENT
# =============================================================================

CITY_CONTENT = {
    # US Cities - Tier 1
    "new-york": {
        "overview": "New York City is one of the world's largest and most diverse job markets, serving as a global hub for finance, media, technology, and healthcare. The metropolitan area employs millions across virtually every industry, with particularly strong opportunities in financial services, advertising, and professional services.",
        "top_industries": ["Finance & Banking", "Healthcare", "Technology", "Media & Entertainment", "Professional Services"],
        "cost_of_living": "high",
        "cost_of_living_detail": "New York has one of the highest costs of living in the US, driven primarily by housing costs. Salaries typically run 20-30% above national averages to compensate, though purchasing power can still lag behind less expensive metros.",
    },
    "los-angeles": {
        "overview": "Los Angeles is a major economic engine with strengths in entertainment, aerospace, technology, and international trade. The vast metropolitan area offers diverse career opportunities, from Hollywood studios to Silicon Beach tech startups to the nation's busiest port complex.",
        "top_industries": ["Entertainment & Media", "Aerospace & Defense", "Technology", "International Trade", "Healthcare"],
        "cost_of_living": "high",
        "cost_of_living_detail": "Los Angeles has a high cost of living, particularly for housing and transportation. Salaries are generally above national averages, though the premium is somewhat offset by California's higher state income taxes.",
    },
    "chicago": {
        "overview": "Chicago is a major business and financial center with a diversified economy spanning manufacturing, finance, technology, and professional services. The city's central location and strong infrastructure make it a hub for transportation, logistics, and corporate headquarters.",
        "top_industries": ["Finance & Insurance", "Manufacturing", "Technology", "Professional Services", "Transportation & Logistics"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Chicago offers a moderate cost of living compared to coastal cities, with more affordable housing and reasonable transportation costs. Salaries are competitive and generally stretch further than in New York or San Francisco.",
    },
    "dallas": {
        "overview": "Dallas-Fort Worth is one of the fastest-growing metros in the US, with a booming economy driven by technology, financial services, and corporate relocations. The area has attracted numerous Fortune 500 headquarters and offers strong job growth across multiple sectors.",
        "top_industries": ["Technology", "Financial Services", "Healthcare", "Telecommunications", "Energy"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Dallas offers a moderate cost of living with relatively affordable housing compared to coastal cities. No state income tax in Texas means workers keep more of their earnings, making it an attractive option for salary-conscious professionals.",
    },
    "houston": {
        "overview": "Houston is the energy capital of the world, with a strong economy anchored by oil and gas, healthcare, and aerospace. The Texas Medical Center and NASA's Johnson Space Center are major employers, and the city's diverse population supports a broad range of industries.",
        "top_industries": ["Energy & Oil/Gas", "Healthcare", "Aerospace", "Manufacturing", "International Trade"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Houston offers a moderate cost of living with affordable housing by major metro standards. Like Dallas, there is no state income tax, which effectively increases take-home pay for all workers.",
    },
    # US Cities - Tier 2
    "san-francisco": {
        "overview": "San Francisco is the epicenter of the global technology industry, home to countless startups and major tech companies. The Bay Area offers some of the highest salaries in the country, particularly in software engineering, data science, and product management.",
        "top_industries": ["Technology", "Finance & Venture Capital", "Biotech & Life Sciences", "Professional Services", "Tourism"],
        "cost_of_living": "high",
        "cost_of_living_detail": "San Francisco has one of the highest costs of living in the nation, with extremely expensive housing. While salaries are significantly above average, the high cost of living means purchasing power is often lower than in more affordable metros.",
    },
    "san-jose": {
        "overview": "San Jose sits at the heart of Silicon Valley, the world's leading technology innovation hub. Major tech companies including Apple, Google, and Adobe are headquartered in the area, creating an incredibly dense concentration of high-paying technology jobs.",
        "top_industries": ["Technology & Software", "Semiconductor Manufacturing", "Clean Energy", "Advanced Manufacturing", "Biotech"],
        "cost_of_living": "high",
        "cost_of_living_detail": "San Jose has an extremely high cost of living, with housing costs among the highest in the nation. Tech salaries are the highest in the country, but significant income is needed to afford living in Silicon Valley.",
    },
    "seattle": {
        "overview": "Seattle has emerged as a major technology hub, home to Amazon, Microsoft, and a growing startup ecosystem. The city also has strong aerospace (Boeing), healthcare, and retail sectors, offering diverse career opportunities with competitive compensation.",
        "top_industries": ["Technology", "Aerospace & Defense", "Healthcare", "E-Commerce & Retail", "Cloud Computing"],
        "cost_of_living": "high",
        "cost_of_living_detail": "Seattle has a high cost of living, primarily due to rising housing costs. However, Washington state has no income tax, which effectively boosts take-home pay compared to high-tax states like California.",
    },
    "washington-dc": {
        "overview": "Washington DC's economy is anchored by the federal government, with extensive opportunities in government contracting, cybersecurity, consulting, and nonprofit organizations. The area also has a growing technology sector and strong healthcare institutions.",
        "top_industries": ["Federal Government", "Government Contracting", "Cybersecurity", "Consulting", "Healthcare"],
        "cost_of_living": "high",
        "cost_of_living_detail": "The DC metro area has a high cost of living, with expensive housing in the District and nearby suburbs. However, government and contractor salaries are generally competitive, and federal benefits packages add significant value.",
    },
    "boston": {
        "overview": "Boston is a world-class center for education, healthcare, and biotechnology. Home to Harvard, MIT, and numerous leading hospitals, the city offers exceptional opportunities in life sciences, technology, and financial services.",
        "top_industries": ["Biotech & Life Sciences", "Higher Education", "Healthcare", "Technology", "Financial Services"],
        "cost_of_living": "high",
        "cost_of_living_detail": "Boston has a high cost of living, particularly for housing. Salaries in biotech, tech, and healthcare are well above national averages, reflecting both the high demand for talent and the area's expensive real estate market.",
    },
    # US Cities - Tier 3
    "philadelphia": {
        "overview": "Philadelphia has a diversified economy with strengths in healthcare, education, and financial services. The city's pharmaceutical and biotech sectors are growing, and its lower cost of living compared to New York makes it an attractive alternative for professionals.",
        "top_industries": ["Healthcare", "Education", "Financial Services", "Pharmaceuticals", "Manufacturing"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Philadelphia offers a moderate cost of living, significantly lower than neighboring New York City. Housing is more affordable, and the city provides a good balance of urban amenities and reasonable expenses.",
    },
    "atlanta": {
        "overview": "Atlanta is a major business hub in the Southeast, with a diverse economy spanning technology, media, logistics, and healthcare. The city is home to numerous Fortune 500 companies and has a rapidly growing tech scene.",
        "top_industries": ["Logistics & Transportation", "Technology", "Media & Entertainment", "Healthcare", "Financial Services"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Atlanta offers a moderate cost of living with relatively affordable housing for a major metro. The city provides a good balance of competitive salaries and reasonable living expenses.",
    },
    "miami": {
        "overview": "Miami is a gateway to Latin America with strengths in international trade, tourism, finance, and real estate. The city's diverse, multilingual workforce and growing tech scene make it an increasingly attractive market for professionals.",
        "top_industries": ["International Trade", "Tourism & Hospitality", "Real Estate", "Finance", "Healthcare"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Miami has a moderate to high cost of living, with rising housing costs. Florida has no state income tax, which increases take-home pay, though salaries tend to be somewhat below those in other major metros.",
    },
    "phoenix": {
        "overview": "Phoenix is one of the fastest-growing metros in the US, attracting businesses and workers with its lower costs and warm climate. The economy is diversified across technology, healthcare, financial services, and manufacturing.",
        "top_industries": ["Technology", "Healthcare", "Financial Services", "Manufacturing", "Real Estate"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Phoenix offers a moderate cost of living that is below the national average for major metros. Affordable housing and no state income tax make it an attractive relocation destination for cost-conscious professionals.",
    },
    "minneapolis": {
        "overview": "Minneapolis-St. Paul has a strong, diversified economy anchored by healthcare, finance, retail, and food production. The metro is home to numerous Fortune 500 companies and offers competitive salaries with a relatively affordable cost of living.",
        "top_industries": ["Healthcare", "Financial Services", "Retail", "Food Production", "Technology"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Minneapolis offers a moderate cost of living with affordable housing relative to coastal cities. The metro provides strong salaries and good purchasing power, though cold winters are a consideration.",
    },
    "san-diego": {
        "overview": "San Diego's economy is driven by defense, biotechnology, tourism, and a growing technology sector. The city's proximity to the US-Mexico border also supports international trade and manufacturing operations.",
        "top_industries": ["Defense & Military", "Biotech & Life Sciences", "Tourism", "Technology", "Healthcare"],
        "cost_of_living": "high",
        "cost_of_living_detail": "San Diego has a high cost of living, largely driven by housing costs. While salaries are above national averages, the cost premium is significant, particularly compared to other Sunbelt metros.",
    },
    "denver": {
        "overview": "Denver has a thriving economy with strengths in technology, aerospace, energy, and outdoor recreation industries. The city has attracted significant tech talent and corporate relocations in recent years.",
        "top_industries": ["Technology", "Aerospace & Defense", "Energy", "Healthcare", "Financial Services"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Denver has a moderate to high cost of living, with housing costs that have risen significantly in recent years. Salaries are competitive and the state offers a flat income tax rate.",
    },
    "detroit": {
        "overview": "Detroit's economy is anchored by the automotive industry, with major manufacturers and suppliers headquartered in the metro area. The city is also growing in technology, healthcare, and advanced manufacturing sectors.",
        "top_industries": ["Automotive", "Manufacturing", "Technology", "Healthcare", "Financial Services"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Detroit has one of the lowest costs of living among major metros, with very affordable housing. Salaries go further here than in most other large cities, making it attractive for cost-conscious professionals.",
    },
    "austin": {
        "overview": "Austin is one of America's fastest-growing tech hubs, attracting major companies and startups with its business-friendly environment and vibrant culture. The city has become a top destination for technology workers and entrepreneurs.",
        "top_industries": ["Technology", "Government", "Education", "Healthcare", "Entertainment"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Austin's cost of living has risen significantly with its tech boom but remains moderate compared to Silicon Valley. No state income tax in Texas boosts take-home pay for workers.",
    },
    "portland": {
        "overview": "Portland has a diverse economy with strengths in technology, manufacturing, outdoor apparel, and creative industries. The city attracts talent with its quality of life, sustainability focus, and growing tech sector.",
        "top_industries": ["Technology", "Manufacturing", "Outdoor & Apparel", "Healthcare", "Creative Industries"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Portland has a moderate cost of living, though housing costs have risen. Oregon has no sales tax, which helps offset the state income tax. The city offers good value compared to nearby Seattle and California metros.",
    },
    # US Cities - Tier 4
    "nashville": {
        "overview": "Nashville is a rapidly growing metro with a diversified economy beyond its famous music industry. Healthcare, education, finance, and technology sectors are all expanding, attracting businesses and workers from across the country.",
        "top_industries": ["Healthcare", "Music & Entertainment", "Education", "Financial Services", "Technology"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Nashville has a moderate cost of living with no state income tax on wages. Housing costs have risen with the city's popularity but remain affordable compared to coastal metros.",
    },
    "raleigh": {
        "overview": "Raleigh-Durham, anchored by Research Triangle Park, is a major hub for technology, biotechnology, and academic research. The presence of Duke, NC State, and UNC creates a highly educated workforce and strong innovation ecosystem.",
        "top_industries": ["Technology", "Biotech & Pharmaceuticals", "Education", "Healthcare", "Government"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Raleigh offers a moderate cost of living with affordable housing relative to major tech hubs. The combination of competitive tech salaries and reasonable costs makes it one of the best-value metros in the country.",
    },
    "charlotte": {
        "overview": "Charlotte is the second-largest banking center in the US, home to Bank of America and Truist. The city's economy extends beyond finance into technology, energy, and healthcare, with strong job growth across sectors.",
        "top_industries": ["Banking & Finance", "Energy", "Technology", "Healthcare", "Logistics"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Charlotte has a moderate cost of living with affordable housing and no local income tax. The city offers strong financial sector salaries in a relatively affordable market.",
    },
    "salt-lake-city": {
        "overview": "Salt Lake City has a growing technology sector, often called the 'Silicon Slopes,' alongside strengths in healthcare, outdoor recreation, and financial services. The metro offers a high quality of life with mountain access.",
        "top_industries": ["Technology", "Healthcare", "Financial Services", "Outdoor Recreation", "Mining & Resources"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Salt Lake City has a moderate cost of living, though housing prices have risen with the tech sector growth. The metro still offers good value compared to coastal tech hubs.",
    },
    "las-vegas": {
        "overview": "Las Vegas is best known for its tourism and entertainment industry, but the metro also has growing healthcare, technology, and logistics sectors. The city's business-friendly tax environment attracts corporate relocations.",
        "top_industries": ["Tourism & Hospitality", "Entertainment & Gaming", "Healthcare", "Construction", "Logistics"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Las Vegas has a moderate cost of living with affordable housing by major metro standards. Nevada has no state income tax, which increases take-home pay for workers.",
    },
    "tampa": {
        "overview": "Tampa's economy is driven by financial services, healthcare, technology, and tourism. The metro area has seen strong population and job growth, attracting remote workers and corporate relocations with its warm climate and affordable living.",
        "top_industries": ["Financial Services", "Healthcare", "Technology", "Tourism", "Defense"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Tampa has a moderate cost of living with no state income tax in Florida. Housing is relatively affordable, making it attractive for professionals relocating from higher-cost metros.",
    },
    "orlando": {
        "overview": "Orlando's economy extends well beyond its famous theme parks, with growing technology, simulation, and healthcare sectors. The metro's tourism infrastructure supports a large hospitality workforce, while the tech sector continues to expand.",
        "top_industries": ["Tourism & Hospitality", "Technology & Simulation", "Healthcare", "Aerospace", "Education"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Orlando has a moderate cost of living with no state income tax. Housing is affordable compared to many major metros, though prices have been rising with population growth.",
    },
    "san-antonio": {
        "overview": "San Antonio has a strong military presence and growing healthcare, cybersecurity, and financial services sectors. The city offers a relatively affordable cost of living with no state income tax.",
        "top_industries": ["Military & Defense", "Healthcare", "Cybersecurity", "Financial Services", "Tourism"],
        "cost_of_living": "low",
        "cost_of_living_detail": "San Antonio has a low cost of living with affordable housing and no state income tax. It offers some of the best purchasing power among major Texas metros.",
    },
    "columbus": {
        "overview": "Columbus is Ohio's capital and largest city, with a diverse economy anchored by government, education, insurance, and technology. The presence of Ohio State University drives research and innovation.",
        "top_industries": ["Government", "Education", "Insurance", "Technology", "Healthcare"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Columbus has a low cost of living with very affordable housing. Salaries stretch further here than in most comparably sized metros, offering strong purchasing power.",
    },
    "indianapolis": {
        "overview": "Indianapolis has a diversified economy with strengths in healthcare, motorsports, logistics, and manufacturing. The city's central location makes it a natural transportation and distribution hub.",
        "top_industries": ["Healthcare", "Manufacturing", "Logistics", "Insurance", "Technology"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Indianapolis has a low cost of living with very affordable housing. The city offers competitive salaries relative to its costs, making it one of the higher purchasing-power metros in the Midwest.",
    },
    # US Cities - Tier 5
    "pittsburgh": {
        "overview": "Pittsburgh has transformed from its steel-industry roots into a hub for technology, healthcare, and education. Carnegie Mellon and the University of Pittsburgh drive innovation in robotics, AI, and life sciences.",
        "top_industries": ["Healthcare", "Technology & Robotics", "Education", "Financial Services", "Energy"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Pittsburgh has a low cost of living with affordable housing and a high quality of life. Tech and healthcare salaries stretch significantly further than in coastal cities.",
    },
    "st-louis": {
        "overview": "St. Louis has a diversified economy with strengths in healthcare, biotechnology, financial services, and manufacturing. The metro area is home to several Fortune 500 companies and major medical institutions.",
        "top_industries": ["Healthcare", "Biotechnology", "Financial Services", "Manufacturing", "Defense"],
        "cost_of_living": "low",
        "cost_of_living_detail": "St. Louis has a low cost of living, particularly for housing. The city offers excellent purchasing power relative to salaries, especially in healthcare and finance.",
    },
    "baltimore": {
        "overview": "Baltimore's economy is driven by healthcare, higher education, and its proximity to Washington DC. Johns Hopkins University and Hospital are major employers, and the city benefits from significant federal spending in the region.",
        "top_industries": ["Healthcare", "Education", "Cybersecurity", "Biotech", "Government"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Baltimore has a moderate cost of living, lower than nearby Washington DC. The city offers competitive salaries, particularly in healthcare and cybersecurity, with more affordable housing than the capital.",
    },
    "sacramento": {
        "overview": "Sacramento is California's state capital with a large government workforce, along with growing technology and healthcare sectors. The city offers a more affordable alternative to the Bay Area while remaining within California's economic ecosystem.",
        "top_industries": ["Government", "Healthcare", "Technology", "Agriculture", "Education"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Sacramento has a moderate cost of living for California, significantly lower than San Francisco or Los Angeles. It offers good value for workers who want California living at a lower price point.",
    },
    "kansas-city": {
        "overview": "Kansas City spans two states and offers a diversified economy with strengths in agriculture, transportation, and an emerging technology sector. The metro area has a growing startup scene and several Fortune 500 companies.",
        "top_industries": ["Agriculture & Food Processing", "Transportation", "Technology", "Financial Services", "Healthcare"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Kansas City has a low cost of living with very affordable housing. The city offers strong purchasing power and a high quality of life relative to its costs.",
    },
    "cleveland": {
        "overview": "Cleveland has a healthcare-driven economy, anchored by the Cleveland Clinic and University Hospitals. The city also has strengths in manufacturing, financial services, and a growing technology sector.",
        "top_industries": ["Healthcare", "Manufacturing", "Financial Services", "Technology", "Education"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Cleveland has one of the lowest costs of living among major metros, with extremely affordable housing. Healthcare salaries in particular offer exceptional purchasing power.",
    },
    "cincinnati": {
        "overview": "Cincinnati is home to several Fortune 500 companies, including Procter & Gamble and Kroger. The city has a strong consumer goods, healthcare, and financial services economy with a growing tech presence.",
        "top_industries": ["Consumer Goods", "Healthcare", "Financial Services", "Manufacturing", "Technology"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Cincinnati has a low cost of living with affordable housing and a strong job market. Corporate headquarters provide competitive salaries with significantly lower living costs than coastal cities.",
    },
    "milwaukee": {
        "overview": "Milwaukee has a strong manufacturing heritage alongside growing healthcare, finance, and technology sectors. The city offers a high quality of life with access to Lake Michigan and a vibrant cultural scene.",
        "top_industries": ["Manufacturing", "Healthcare", "Financial Services", "Food & Beverage", "Technology"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Milwaukee has a low cost of living with affordable housing. The city provides good salaries relative to costs, especially in manufacturing and healthcare.",
    },
    "jacksonville": {
        "overview": "Jacksonville is Florida's largest city by area, with a diversified economy spanning logistics, financial services, healthcare, and military installations. The city's port is one of the busiest on the East Coast.",
        "top_industries": ["Logistics & Transportation", "Financial Services", "Healthcare", "Military", "Insurance"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Jacksonville has a low cost of living with affordable housing and no state income tax. The combination makes it one of the highest purchasing-power metros in the Southeast.",
    },
    "richmond": {
        "overview": "Richmond is Virginia's capital with a diversified economy including government, financial services, healthcare, and a growing technology sector. The city blends historic charm with modern economic development.",
        "top_industries": ["Government", "Financial Services", "Healthcare", "Technology", "Manufacturing"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Richmond has a moderate cost of living with reasonably affordable housing. The city offers a good balance between salary levels and living expenses.",
    },
    # US Cities - Tier 6
    "oklahoma-city": {
        "overview": "Oklahoma City's economy is centered on energy, aerospace, and government, with a growing healthcare and technology presence. The city offers one of the lowest costs of living among US metros.",
        "top_industries": ["Energy", "Aerospace", "Government", "Healthcare", "Agriculture"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Oklahoma City has one of the lowest costs of living in the country, with very affordable housing. Salaries provide excellent purchasing power.",
    },
    "memphis": {
        "overview": "Memphis is a major logistics hub, home to FedEx's world headquarters. The city's economy also includes healthcare, manufacturing, and a significant agricultural sector.",
        "top_industries": ["Logistics & Shipping", "Healthcare", "Manufacturing", "Agriculture", "Tourism"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Memphis has a low cost of living with some of the most affordable housing among major US metros. No state income tax on wages boosts purchasing power.",
    },
    "louisville": {
        "overview": "Louisville has a diversified economy with strengths in healthcare, logistics, manufacturing, and the bourbon industry. UPS Worldport, the company's global air hub, makes Louisville a major logistics center.",
        "top_industries": ["Healthcare", "Logistics & Shipping", "Manufacturing", "Bourbon & Spirits", "Automotive"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Louisville has a low cost of living with affordable housing and reasonable taxes. The city offers good purchasing power for a mid-sized metro.",
    },
    "new-orleans": {
        "overview": "New Orleans has a unique economy driven by tourism, energy, port operations, and a distinctive cultural sector. The city is rebuilding and diversifying its economy, with growing technology and creative industry sectors.",
        "top_industries": ["Tourism & Hospitality", "Energy", "Port Operations", "Healthcare", "Film & Media"],
        "cost_of_living": "low",
        "cost_of_living_detail": "New Orleans has a low cost of living with relatively affordable housing. Louisiana has a moderate state income tax, but overall living costs are well below the national average for a major city.",
    },
    "hartford": {
        "overview": "Hartford is the insurance capital of America, home to numerous major insurance companies. The metro also has strengths in aerospace manufacturing, healthcare, and financial services.",
        "top_industries": ["Insurance", "Aerospace Manufacturing", "Healthcare", "Financial Services", "Education"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Hartford has a moderate cost of living, lower than nearby Boston or New York. The insurance industry provides stable, well-paying employment in a reasonably affordable market.",
    },
    "buffalo": {
        "overview": "Buffalo's economy is diversifying from its manufacturing roots, with growth in healthcare, education, and professional services. The city offers an affordable cost of living near the Canadian border.",
        "top_industries": ["Healthcare", "Education", "Manufacturing", "Financial Services", "Tourism"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Buffalo has a low cost of living with very affordable housing. The city offers strong purchasing power, though New York state taxes can offset some savings.",
    },
    "birmingham": {
        "overview": "Birmingham is Alabama's largest city with a strong healthcare and financial services economy. The city is home to the University of Alabama at Birmingham, a major medical research institution and employer.",
        "top_industries": ["Healthcare", "Financial Services", "Manufacturing", "Construction", "Education"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Birmingham has one of the lowest costs of living among US metros, with very affordable housing and low overall expenses. Healthcare salaries offer particularly strong purchasing power.",
    },
    "tucson": {
        "overview": "Tucson's economy includes aerospace, defense, mining, and a significant higher education sector centered around the University of Arizona. The city offers an affordable alternative to Phoenix.",
        "top_industries": ["Aerospace & Defense", "Education", "Healthcare", "Mining", "Tourism"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Tucson has a low cost of living with affordable housing and reasonable overall expenses. The city offers good purchasing power, particularly for defense and education sector workers.",
    },
    "honolulu": {
        "overview": "Honolulu's economy is driven by tourism, military spending, and government services. The unique island location creates both opportunities and challenges, with high living costs but a distinctive quality of life.",
        "top_industries": ["Tourism & Hospitality", "Military & Defense", "Government", "Healthcare", "Construction"],
        "cost_of_living": "high",
        "cost_of_living_detail": "Honolulu has a very high cost of living, driven by expensive housing and higher prices for goods that must be imported. Salaries are above national averages but may not fully compensate for the elevated costs.",
    },
    "anchorage": {
        "overview": "Anchorage is Alaska's economic center, with an economy driven by oil and gas, government, healthcare, and tourism. The city offers unique opportunities in resource extraction and remote area services.",
        "top_industries": ["Oil & Gas", "Government", "Healthcare", "Tourism", "Transportation"],
        "cost_of_living": "high",
        "cost_of_living_detail": "Anchorage has a high cost of living due to the remote location and higher prices for goods and services. However, Alaska has no state income or sales tax, and the Permanent Fund Dividend provides an annual payment to residents.",
    },

    # Canadian Cities
    "toronto": {
        "overview": "Toronto is Canada's largest city and financial capital, with a diverse economy spanning finance, technology, film, and healthcare. The city has become one of North America's fastest-growing tech hubs and attracts talent from around the world.",
        "top_industries": ["Financial Services", "Technology", "Film & Television", "Healthcare", "Mining & Resources"],
        "cost_of_living": "high",
        "cost_of_living_detail": "Toronto has one of the highest costs of living in Canada, driven primarily by housing costs. Salaries are competitive for Canada, though generally lower than comparable US metros when adjusted for exchange rates.",
    },
    "vancouver": {
        "overview": "Vancouver has a diverse economy with strengths in technology, film production, natural resources, and tourism. The city's quality of life and Pacific Rim connections make it a gateway for international business.",
        "top_industries": ["Technology", "Film & Television", "Natural Resources", "Tourism", "Real Estate"],
        "cost_of_living": "high",
        "cost_of_living_detail": "Vancouver has the highest housing costs in Canada and one of the highest in North America. Salaries may not fully compensate for the extreme cost of real estate.",
    },
    "montreal": {
        "overview": "Montreal is a major cultural and economic hub with strengths in aerospace, AI research, video game development, and pharmaceuticals. The city benefits from a lower cost of living than Toronto and Vancouver.",
        "top_industries": ["Aerospace", "AI & Technology", "Video Games", "Pharmaceuticals", "Financial Services"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Montreal has a moderate cost of living by Canadian major city standards, with more affordable housing than Toronto or Vancouver. Quebec's higher taxes are offset by lower living costs.",
    },
    "ottawa": {
        "overview": "Ottawa is Canada's national capital with a large federal government workforce. The city also has a significant technology sector, particularly in telecommunications and software, anchored by the Kanata tech park.",
        "top_industries": ["Federal Government", "Technology", "Healthcare", "Education", "Defense"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Ottawa has a moderate cost of living with more affordable housing than Toronto. Government salaries are stable and competitive, with strong benefits packages.",
    },
    "calgary": {
        "overview": "Calgary is the hub of Canada's energy sector, home to major oil and gas companies. The city also has a growing technology sector and offers some of the highest average salaries in Canada.",
        "top_industries": ["Oil & Gas", "Technology", "Financial Services", "Agriculture", "Transportation"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Calgary has a moderate cost of living with no provincial sales tax in Alberta. Energy sector salaries are among the highest in Canada, offering strong purchasing power.",
    },
    "edmonton": {
        "overview": "Edmonton is Alberta's capital and a major center for oil sands operations, government services, and education. The University of Alberta is a significant employer and research institution.",
        "top_industries": ["Oil & Gas", "Government", "Education", "Healthcare", "Construction"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Edmonton has a moderate cost of living with affordable housing by major Canadian city standards. No provincial sales tax in Alberta provides additional savings for residents.",
    },
    "winnipeg": {
        "overview": "Winnipeg has a diversified economy including manufacturing, agriculture, financial services, and government. The city is a major transportation hub connecting eastern and western Canada.",
        "top_industries": ["Manufacturing", "Agriculture", "Financial Services", "Government", "Transportation"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Winnipeg has one of the lowest costs of living among major Canadian cities, with very affordable housing. Salaries offer strong purchasing power despite being lower than in Toronto or Vancouver.",
    },
    "quebec-city": {
        "overview": "Quebec City is the provincial capital of Quebec, with a primarily French-speaking economy centered on government, technology, insurance, and tourism. The historic city attracts millions of visitors annually.",
        "top_industries": ["Government", "Technology", "Insurance", "Tourism", "Healthcare"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Quebec City has a low cost of living with very affordable housing. While salaries are generally lower than in Montreal or Toronto, the purchasing power is strong due to low living costs.",
    },
    "hamilton": {
        "overview": "Hamilton is an industrial city near Toronto that has been diversifying its economy from steel manufacturing into healthcare, education, and technology. Its proximity to Toronto offers additional job market access.",
        "top_industries": ["Healthcare", "Manufacturing", "Education", "Technology", "Logistics"],
        "cost_of_living": "moderate",
        "cost_of_living_detail": "Hamilton has a moderate cost of living, lower than nearby Toronto. The city has become popular with Toronto commuters seeking more affordable housing while accessing the larger metro's job market.",
    },
    "halifax": {
        "overview": "Halifax is the economic hub of Atlantic Canada, with strengths in government, military, education, and ocean technology. The city offers a lower cost of living than most Canadian metros.",
        "top_industries": ["Government & Military", "Education", "Ocean Technology", "Healthcare", "Tourism"],
        "cost_of_living": "low",
        "cost_of_living_detail": "Halifax has a low cost of living for a major Canadian city, with affordable housing and reasonable overall expenses. The city offers good value for workers in government and education sectors.",
    },
}


# =============================================================================
# RELATED OCCUPATIONS MAPPING
# =============================================================================

def get_related_occupations(slug, soc_code, all_occupations):
    """Find 2-3 related occupations based on SOC code proximity."""
    group = soc_code[:2]
    related = []
    for s, code, name, median in all_occupations:
        if s == slug:
            continue
        if code[:2] == group and len(related) < 3:
            related.append(s)
    return related


# =============================================================================
# CONTENT GENERATION
# =============================================================================

def generate_occupation_content(occupations):
    """Generate content for all occupations."""
    content = {}

    for slug, soc_code, name, median in occupations:
        group_code = soc_code[:2]
        group = SOC_GROUPS.get(group_code)

        if not group:
            continue

        # Check for override
        override = OCCUPATION_OVERRIDES.get(slug, {})

        # Select description template deterministically
        desc_hash = int(hashlib.md5(slug.encode()).hexdigest(), 16)
        desc_idx = desc_hash % len(group["descriptions"])
        description = override.get("description", group["descriptions"][desc_idx].format(
            name=name,
            name_lower=name.lower(),
        ))

        # Select skills
        if "skills" in override:
            skills = override["skills"]
        else:
            # Take first 3 from group pool deterministically, then add 3-5 more
            all_skills = group["skills"]
            start = desc_hash % max(1, len(all_skills) - 5)
            skills = all_skills[start:start + 6]
            if len(skills) < 6:
                skills = (all_skills + all_skills)[:6]

        # Select tips (pick 5 from pool)
        all_tips = group["tips"]
        tip_start = (desc_hash >> 4) % max(1, len(all_tips) - 4)
        tips = all_tips[tip_start:tip_start + 5]
        if len(tips) < 5:
            tips = (all_tips + all_tips)[:5]

        # Related occupations
        related = get_related_occupations(slug, soc_code, occupations)

        content[slug] = {
            "soc_group": group_code,
            "description": description,
            "skills": skills,
            "education": group["education"],
            "education_detail": group["education_detail"],
            "career_outlook": group["outlook"],
            "salary_tips": tips,
            "work_environment": group["work_env"],
            "related_occupations": related,
        }

    return content


def main():
    print("=" * 60)
    print("  SalaryLens — Content Generation")
    print("=" * 60)

    # Generate occupation content
    print(f"\n  Generating content for {len(OCCUPATIONS)} occupations...")
    occ_content = generate_occupation_content(OCCUPATIONS)
    print(f"    Generated {len(occ_content)} occupation entries")

    # City content
    city_content = CITY_CONTENT
    print(f"  City content: {len(city_content)} cities")

    # Write occupation content
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    occ_path = os.path.join(OUTPUT_DIR, "occupation_content.json")
    with open(occ_path, "w") as f:
        json.dump(occ_content, f, indent=2)
    occ_size = os.path.getsize(occ_path) / 1024
    print(f"\n  occupation_content.json: {occ_size:.0f} KB ({len(occ_content)} entries)")

    # Write city content
    city_path = os.path.join(OUTPUT_DIR, "city_content.json")
    with open(city_path, "w") as f:
        json.dump(city_content, f, indent=2)
    city_size = os.path.getsize(city_path) / 1024
    print(f"  city_content.json: {city_size:.0f} KB ({len(city_content)} entries)")

    print(f"\n  Output directory: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
