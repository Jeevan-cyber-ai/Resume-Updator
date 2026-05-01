import axios from 'axios'

// Base axios instance configured for the backend
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 120000, // 2 minutes — Gemini can take time on large resumes
})

// Request interceptor – log all outgoing requests
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor – standardize error messages
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'An unexpected error occurred.'
    return Promise.reject(new Error(message))
  }
)

/**
 * Upload a resume file using the unified LangChain extraction pipeline.
 * @param {File} file - The resume file (PDF or DOCX)
 * @returns {Promise<Object>} The structured resume data returned by the AI
 */
export const uploadResume = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post('/api/upload-resume', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

/**
 * Compare extracted resume data against a job title using the backend LLM.
 * @param {Object} resumeData - The structured resume JSON
 * @param {string} jobTitle - Target job title
 * @returns {Promise<Object>} Scores and suggestions for skills, projects, objective
 */
export const compareResumeWithJob = async (resumeData, jobTitle) => {
  const response = await api.post('/api/compare', {
    resume_data: resumeData,
    job_title: jobTitle,
  })
  return response.data
}

/**
 * Call the LangGraph improver workflow for a specific resume section.
 * @param {string} section - "objective", "projects", or "skills"
 * @param {Object} resumeData - The current structured resume data
 * @param {string} jobTitle - The target job title
 * @param {string} userInput - The rough input from the user (for objective/projects)
 * @param {Array} feedbackHistory - The conversational history for Human-in-the-Loop iteration
 */
export const improveSection = async (section, resumeData, jobTitle, userInput = "", feedbackHistory = []) => {
  const response = await api.post('/api/improve', {
    section,
    resume_data: resumeData,
    job_title: jobTitle,
    user_input: userInput,
    feedback_history: feedbackHistory
  })
  return response.data
}

export default api
