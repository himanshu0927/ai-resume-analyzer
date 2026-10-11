export interface User {
  id: number;
  name: string;
  email: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Resume {
  id: number;
  user_id: number;
  filename: string;
  file_type: string;
  uploaded_at: string;
  extracted_text?: string;
}

export interface ScoreFactor {
  factor: string;
  weight: string;
  score: number;
  status: string;
}

export interface Suggestion {
  priority: 'High' | 'Medium' | 'Low';
  category: string;
  text: string;
}

export interface ResumeAnalysis {
  id: number;
  user_id: number;
  resume_id: number;
  overall_score: number;
  skills_score: number;
  experience_score: number;
  education_score: number;
  projects_score: number;
  certifications_score: number;
  completeness_score: number;
  keyword_relevance_score: number;
  formatting_score: number;
  personal_info: {
    name: string;
    email: string;
    phone: string;
    location: string;
  };
  education: Array<{
    degree: string;
    institution: string;
    graduation_year: string;
    relevant_coursework: string;
  }>;
  experience: Array<{
    company: string;
    job_title: string;
    duration: string;
    responsibilities: string[];
  }>;
  projects: Array<{
    project_name: string;
    technologies: string;
    description: string;
  }>;
  certifications: string[];
  raw_extracted_data: {
    all_skills: string[];
    categorized_skills: Record<string, string[]>;
    total_count: number;
  };
  score_factors: ScoreFactor[];
  suggestions: Suggestion[];
  created_at: string;
}

export interface JobMatch {
  id?: number;
  resume_id?: number;
  job_title: string;
  job_description: string;
  match_score: number;
  matching_skills: string[];
  missing_skills: string[];
  relevant_experience: string[];
  relevant_projects: string[];
  suggestions: Array<{ type: string; text: string }>;
  created_at?: string;
}

export interface JobRecommendation {
  id?: number;
  role: string;
  match_percentage: number;
  reason: string;
  key_matching_skills: string[];
}

export interface SkillGapAnalysis {
  target_role: string;
  total_target_skills: number;
  already_learned: string[];
  partially_covered: string[];
  missing: string[];
  stats: {
    learned_count: number;
    learned_percentage: number;
    partial_count: number;
    partial_percentage: number;
    missing_count: number;
    missing_percentage: number;
  };
  learning_suggestions: {
    topics_to_learn: string[];
    suggested_project_ideas: string[];
    suggested_practice_areas: string[];
  };
}
