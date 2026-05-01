import { useState, useRef } from 'react'
import { uploadResume, compareResumeWithJob } from './api/resumeApi'
import ImproveModal from './components/ImproveModal'
import './UploadPage.css'

export default function UploadPage() {
  const [file, setFile] = useState(null)
  const [companyName, setCompanyName] = useState('')
  const [jobTitle, setJobTitle] = useState('')
  const [dragging, setDragging] = useState(false)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [scores, setScores] = useState(null)
  const [error, setError] = useState(null)
  const [showRaw, setShowRaw] = useState(false)
  const [improveModal, setImproveModal] = useState({ isOpen: false, section: '' })
  const fileInputRef = useRef(null)

  const handleFile = (selected) => {
    if (!selected) return
    const ext = selected.name.split('.').pop().toLowerCase()
    if (!['pdf', 'docx'].includes(ext)) {
      setError('Only PDF and DOCX files are supported.')
      return
    }
    setFile(selected)
    setError(null)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    handleFile(e.dataTransfer.files[0])
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!companyName.trim()) { setError('Please enter the company name.'); return }
    if (!jobTitle.trim()) { setError('Please enter the job title.'); return }
    if (!file) { setError('Please upload your resume file.'); return }

    setLoading(true)
    setError(null)
    setResult(null)
    setScores(null)

    try {
      const res = await uploadResume(file)
      const data = res.data
      setResult({ ...data, _company: companyName, _jobTitle: jobTitle })

      // Call LLM-powered backend comparison
      const compareRes = await compareResumeWithJob(data, jobTitle)
      setScores(compareRes.scores)
    } catch (err) {
      setError(err.message || 'Something went wrong. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  const getScoreColor = (score) => {
    if (score >= 70) return 'score-green'
    if (score >= 40) return 'score-yellow'
    return 'score-red'
  }

  const handleApplyImprovement = (section, generatedText) => {
    setResult(prev => {
      const updated = { ...prev }
      if (section === 'objective') {
        updated.summary = generatedText
        updated.objectives = generatedText
      } else if (section === 'projects') {
        updated.projects = [{ name: '✨ AI Tailored Project', description: generatedText }, ...(updated.projects || [])]
      } else if (section === 'skills') {
        const newSkills = generatedText.split(',').map(s => s.trim()).filter(s => s)
        updated.skills = [...new Set([...(updated.skills || []), ...newSkills])]
      }
      return updated
    })
  }

  return (
    <div className="page">
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <div className="orb orb-3" />

      <div className="wrapper">
        {/* Header */}
        <header className="header">
          <div className="logo">
            <span className="logo-icon">✦</span>
            <span className="logo-text">ResumeAI</span>
          </div>
          <div className="header-badge">
            <span className="badge-dot" />
            Powered by Gemini 2.5
          </div>
        </header>

        {/* Hero */}
        <section className="hero">
          <div className="hero-tag">🚀 AI Resume Tailoring</div>
          <h1 className="hero-title">
            Transform Your Resume<br />
            <span className="gradient-text">For Any Job in Seconds</span>
          </h1>
          <p className="hero-subtitle">
            Tell us your target role, upload your resume — AI analyzes the match and customizes your profile automatically.
          </p>
        </section>

        {/* Form */}
        <form className="form" onSubmit={handleSubmit}>

          {/* Step 1 – Job Details (moved to top) */}
          <div className="card">
            <div className="step-header">
              <div className="step-num">01</div>
              <div>
                <h2 className="step-title">Target Job Details</h2>
                <p className="step-desc">Tell us where you want to apply</p>
              </div>
            </div>

            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">Company Name</label>
                <div className="input-wrapper">
                  <span className="input-icon">🏢</span>
                  <input
                    type="text"
                    className="form-input"
                    placeholder="e.g. Google, Infosys, TCS"
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Job Position / Title</label>
                <div className="input-wrapper">
                  <span className="input-icon">💼</span>
                  <input
                    type="text"
                    className="form-input"
                    placeholder="e.g. Web Developer, Data Analyst"
                    value={jobTitle}
                    onChange={(e) => setJobTitle(e.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Step 2 – Upload Resume (moved below) */}
          <div className="card">
            <div className="step-header">
              <div className="step-num">02</div>
              <div>
                <h2 className="step-title">Upload Your Resume</h2>
                <p className="step-desc">Supports PDF and DOCX formats</p>
              </div>
            </div>

            <div
              className={`dropzone ${dragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
              onClick={() => !file && fileInputRef.current.click()}
              onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
              onDragLeave={() => setDragging(false)}
              onDrop={handleDrop}
            >
              <input
                type="file"
                ref={fileInputRef}
                accept=".pdf,.docx"
                style={{ display: 'none' }}
                onChange={(e) => handleFile(e.target.files[0])}
              />

              {!file ? (
                <div className="dropzone-empty">
                  <div className="drop-icon">📄</div>
                  <p className="drop-text">Drag & drop your resume here</p>
                  <p className="drop-sub">PDF or DOCX · Max 10MB</p>
                  <button type="button" className="btn-browse" onClick={() => fileInputRef.current.click()}>
                    Browse Files
                  </button>
                </div>
              ) : (
                <div className="file-preview">
                  <span className="file-icon">✅</span>
                  <div className="file-meta">
                    <span className="file-name">{file.name}</span>
                    <span className="file-size">{formatFileSize(file.size)}</span>
                  </div>
                  <button
                    type="button"
                    className="btn-remove"
                    onClick={(e) => { e.stopPropagation(); setFile(null) }}
                  >✕</button>
                </div>
              )}
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="error-banner">
              <span>⚠️</span> {error}
            </div>
          )}

          {/* Submit */}
          <div className="submit-row">
            <button type="submit" className="btn-submit" disabled={loading}>
              {loading ? (
                <>
                  <span className="spinner-sm" />
                  Analyzing...
                </>
              ) : (
                <>
                  <span>Analyze My Resume</span>
                  <span className="btn-arrow">→</span>
                </>
              )}
            </button>
            <p className="submit-note">Your data is processed securely and never stored permanently.</p>
          </div>
        </form>

        {/* Loader Overlay */}
        {loading && (
          <div className="loader-overlay">
            <div className="loader-card">
              <div className="spinner" />
              <p className="loader-title">Analyzing Your Resume...</p>
              <p className="loader-sub">Gemini AI is reading and extracting data</p>
              <div className="loader-bar">
                <div className="loader-fill" />
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {result && (
          <section className="result-section">
            <div className="result-header">
              <div className="result-badge">✅ Analysis Complete</div>
              <h2 className="result-title">Resume Match Report</h2>
              <p className="result-subtitle">
                Analyzing fit for <strong>{result._jobTitle}</strong> at <strong>{result._company}</strong>
              </p>
            </div>

            {/* Match Score Bars */}
            {scores && (
              <div className="scores-card">
                <div className="scores-title">📊 Job Match Analysis</div>
                <p className="scores-subtitle">How well your current resume matches the <strong>{result._jobTitle}</strong> role</p>

                {[
                  { label: 'Title Match', icon: '📛', score: scores.title_score, suggestion: scores.title_suggestion },
                  { label: 'Skill Match', icon: '⚡', score: scores.skill_score, suggestion: scores.skill_suggestion },
                  { label: 'Project Match', icon: '🛠️', score: scores.project_score, suggestion: scores.project_suggestion },
                  { label: 'Objective Match', icon: '🎯', score: scores.objective_score, suggestion: scores.objective_suggestion },
                ].map(({ label, icon, score, suggestion }) => (
                  <div className="score-row" key={label}>
                    <div className="score-top">
                      <div className="score-label-group">
                        <span className="score-icon">{icon}</span>
                        <div>
                          <span className="score-label">{label}</span>
                          {suggestion && <span className="score-hint">{suggestion}</span>}
                        </div>
                      </div>
                      <div className="score-right">
                        <span className={`score-pct ${getScoreColor(score)}`}>{score}%</span>
                        {score < 50 && label !== 'Title Match' && (
                          <button 
                            type="button" 
                            className="btn-improve"
                            onClick={() => setImproveModal({ isOpen: true, section: label.toLowerCase().split(' ')[0] })}
                          >
                            Improve ✨
                          </button>
                        )}
                      </div>
                    </div>
                    <div className="score-bar-track">
                      <div
                        className={`score-bar-fill ${getScoreColor(score)}`}
                        style={{ width: `${score}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Extracted Data Grid */}
            <div className="result-grid">
              {[
                { label: 'Full Name', value: result.name },
                { label: 'Email', value: result.email },
                { label: 'Phone', value: result.phone },
                { label: 'Location', value: result.location },
                { label: 'LinkedIn', value: result.linkedin },
                { label: 'GitHub', value: result.github },
              ].map(({ label, value }) => (
                <div className="result-item" key={label}>
                  <div className="result-label">{label}</div>
                  <div className={`result-value ${!value ? 'empty' : ''}`}>
                    {value && (label === 'LinkedIn' || label === 'GitHub')
                      ? <a href={value} target="_blank" rel="noreferrer" className="result-link">{value}</a>
                      : value || '—'}
                  </div>
                </div>
              ))}

              <div className="result-item result-item-full">
                <div className="result-label">Summary / Objective</div>
                <div className={`result-value ${!(result.summary || result.objectives) ? 'empty' : ''}`}>
                  {result.summary || result.objectives || '—'}
                </div>
              </div>

              <div className="result-item result-item-full">
                <div className="result-label">Skills</div>
                <div className="skills-list">
                  {result.skills?.length
                    ? result.skills.map((s, i) => <span key={i} className="skill-tag">{s}</span>)
                    : <span className="result-value empty">—</span>}
                </div>
              </div>

              {result.education?.length > 0 && (
                <div className="result-item result-item-full">
                  <div className="result-label">Education</div>
                  {result.education.map((edu, i) => (
                    <div key={i} className="sub-item">
                      <strong>{edu.degree}</strong> — {edu.institution} {edu.year ? `(${edu.year})` : ''}
                    </div>
                  ))}
                </div>
              )}

              {result.experience?.length > 0 && (
                <div className="result-item result-item-full">
                  <div className="result-label">Experience</div>
                  {result.experience.map((exp, i) => (
                    <div key={i} className="sub-item">
                      <strong>{exp.role}</strong> at {exp.company} {exp.duration ? `· ${exp.duration}` : ''}
                      {exp.description && <p className="sub-desc">{exp.description}</p>}
                    </div>
                  ))}
                </div>
              )}

              {result.projects?.length > 0 && (
                <div className="result-item result-item-full">
                  <div className="result-label">Projects</div>
                  {result.projects.map((proj, i) => (
                    <div key={i} className="sub-item">
                      <strong>{proj.name}</strong>
                      {proj.description && <p className="sub-desc">{proj.description}</p>}
                    </div>
                  ))}
                </div>
              )}

              {result.certifications?.length > 0 && (
                <div className="result-item result-item-full">
                  <div className="result-label">Certifications</div>
                  <div className="skills-list">
                    {result.certifications.map((c, i) => <span key={i} className="skill-tag">{c}</span>)}
                  </div>
                </div>
              )}
            </div>

            <div className="raw-toggle-row">
              <button className="btn-toggle" onClick={() => setShowRaw(v => !v)}>
                {showRaw ? 'Hide Raw JSON ↑' : 'View Raw JSON ↓'}
              </button>
            </div>
            {showRaw && (
              <pre className="raw-json">{JSON.stringify(result, null, 2)}</pre>
            )}
          </section>
        )}

      </div>

      <ImproveModal 
        isOpen={improveModal.isOpen} 
        onClose={() => setImproveModal({ isOpen: false, section: '' })}
        section={improveModal.section}
        result={result}
        jobTitle={result?._jobTitle}
        onApply={handleApplyImprovement}
      />
    </div>
  )
}
