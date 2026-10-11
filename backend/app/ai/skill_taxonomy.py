SKILL_TAXONOMY = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C", "C#", "Go", "Rust", 
        "PHP", "Ruby", "Swift", "Kotlin", "R", "Scala", "Dart", "MATLAB", "SQL", "HTML", "CSS", "Bash", "Shell"
    ],
    "Web Development": [
        "React", "React.js", "Angular", "Vue", "Vue.js", "Next.js", "Nuxt.js", "Node.js", "Express", "Express.js", 
        "Django", "FastAPI", "Flask", "Spring Boot", "Laravel", "ASP.NET", "GraphQL", "REST API", "Redux", "Tailwind", 
        "Tailwind CSS", "Bootstrap", "Sass", "Webpack", "Vite", "WebSockets"
    ],
    "Databases": [
        "PostgreSQL", "MySQL", "MongoDB", "SQLite", "Redis", "Oracle", "SQL Server", "DynamoDB", 
        "Cassandra", "Elasticsearch", "Neo4j", "Firebase", "Supabase", "MariaDB"
    ],
    "Cloud": [
        "AWS", "Amazon Web Services", "Azure", "GCP", "Google Cloud Platform", "Heroku", 
        "DigitalOcean", "Vercel", "Netlify", "Cloudflare", "Serverless", "S3", "EC2", "Lambda"
    ],
    "DevOps": [
        "Docker", "Kubernetes", "Git", "GitHub", "GitLab", "CI/CD", "Jenkins", "Terraform", 
        "Ansible", "Nginx", "Linux", "Unix", "ArgoCD", "Prometheus", "Grafana", "Actions"
    ],
    "AI/ML": [
        "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "OpenCV", "Hugging Face", 
        "Transformers", "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing", 
        "Computer Vision", "LLM", "Generative AI", "LangChain", "LlamaIndex", "Neural Networks"
    ],
    "Data Science": [
        "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Power BI", "Tableau", 
        "Data Analysis", "Data Visualization", "Data Mining", "ETL", "Spark", "PySpark", "Airflow"
    ],
    "Tools & Platforms": [
        "Postman", "Swagger", "Jira", "Confluence", "Figma", "VS Code", "IntelliJ", "Eclipse", 
        "Docker Desktop", "Bitbucket", "Trello", "Linux CLI", "npm", "pip", "Poetry"
    ],
    "Soft Skills": [
        "Problem Solving", "Communication", "Teamwork", "Leadership", "Critical Thinking", 
        "Time Management", "Agile", "Scrum", "Adaptability", "Collaboration", "Project Management"
    ]
}

# Alias map for flexible skill matching (case-insensitive key mapping)
SKILL_ALIASES = {
    "python": "Python",
    "py": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "csharp": "C#",
    "react": "React",
    "react.js": "React",
    "reactjs": "React",
    "angular": "Angular",
    "angularjs": "Angular",
    "vue": "Vue",
    "vue.js": "Vue",
    "vuejs": "Vue",
    "next": "Next.js",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "node": "Node.js",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "express": "Express",
    "express.js": "Express",
    "expressjs": "Express",
    "django": "Django",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "spring": "Spring Boot",
    "spring boot": "Spring Boot",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "sqlite": "SQLite",
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "docker": "Docker",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "google cloud": "GCP",
    "google cloud platform": "GCP",
    "linux": "Linux",
    "tensorflow": "TensorFlow",
    "tf": "TensorFlow",
    "pytorch": "PyTorch",
    "scikit-learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "dl": "Deep Learning",
    "nlp": "NLP",
    "natural language processing": "NLP",
    "cv": "Computer Vision",
    "computer vision": "Computer Vision",
    "html": "HTML",
    "html5": "HTML",
    "css": "CSS",
    "css3": "CSS",
    "tailwind": "Tailwind",
    "tailwind css": "Tailwind",
    "bootstrap": "Bootstrap",
    "sql": "SQL",
    "graphql": "GraphQL",
    "rest": "REST API",
    "rest api": "REST API",
    "restful api": "REST API",
    "ci/cd": "CI/CD",
    "jenkins": "Jenkins",
    "power bi": "Power BI",
    "tableau": "Tableau",
    "agile": "Agile",
    "scrum": "Scrum",
    "jira": "Jira",
    "postman": "Postman",
    "figma": "Figma"
}
