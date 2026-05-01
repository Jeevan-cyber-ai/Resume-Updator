import { useState } from 'react'
import { improveSection } from '../api/resumeApi'
import './ImproveModal.css'

export default function ImproveModal({ isOpen, onClose, section, result, jobTitle, onApply }) {
  const [step, setStep] = useState('input') // 'input' | 'loading' | 'review'
  const [userInput, setUserInput] = useState('')
  const [generatedOutput, setGeneratedOutput] = useState('')
  const [feedback, setFeedback] = useState('')
  const [feedbackHistory, setFeedbackHistory] = useState([])
  const [error, setError] = useState(null)

  if (!isOpen) return null

  const handleGenerate = async (isRegenerate = false) => {
    setStep('loading')
    setError(null)

    let currentHistory = [...feedbackHistory]

    if (isRegenerate && feedback.trim()) {
      // Add previous AI generation to history
      currentHistory.push({ role: 'ai', content: generatedOutput })
      // Add user feedback to history
      currentHistory.push({ role: 'user', content: feedback })
      setFeedbackHistory(currentHistory)
    } else if (!isRegenerate) {
      // First generation, clear history
      setFeedbackHistory([])
      currentHistory = []
    }

    try {
      const res = await improveSection(section, result, jobTitle, userInput, currentHistory)
      setGeneratedOutput(res.generated_output)
      setStep('review')
      setFeedback('') // Clear feedback input for next potential iteration
    } catch (err) {
      setError(err.message || 'Failed to generate improvement')
      setStep(isRegenerate ? 'review' : 'input')
    }
  }

  const handleApply = () => {
    onApply(section, generatedOutput)
    handleClose()
  }

  const handleClose = () => {
    setStep('input')
    setUserInput('')
    setGeneratedOutput('')
    setFeedback('')
    setFeedbackHistory([])
    setError(null)
    onClose()
  }

  const getPlaceholder = () => {
    if (section === 'objective') return "E.g., I want to highlight my 3 years of React experience and my transition to full-stack."
    if (section === 'projects') return "E.g., Built an e-commerce site using Next.js, Stripe, and PostgreSQL. It handled 1000 users/day."
    return "Enter details..."
  }

  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <button className="modal-close" onClick={handleClose}>✕</button>
        
        <h2 className="modal-title">✨ Improve {section.charAt(0).toUpperCase() + section.slice(1)}</h2>
        
        {error && <div className="modal-error">⚠️ {error}</div>}

        {step === 'input' && (
          <div className="modal-step fade-in">
            <p className="modal-desc">
              Tell the AI what you want to highlight for the <strong>{jobTitle}</strong> role.
            </p>
            <textarea
              className="modal-textarea"
              placeholder={getPlaceholder()}
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              rows={4}
            />
            <div className="modal-actions">
              <button className="btn-secondary" onClick={handleClose}>Cancel</button>
              <button 
                className="btn-primary" 
                onClick={() => handleGenerate(false)}
                disabled={!userInput.trim()}
              >
                Generate Draft →
              </button>
            </div>
          </div>
        )}

        {step === 'loading' && (
          <div className="modal-step fade-in loading-step">
            <div className="spinner-modal" />
            <p>LangGraph AI is crafting your {section}...</p>
          </div>
        )}

        {step === 'review' && (
          <div className="modal-step fade-in review-step">
            <div className="ai-draft-container">
              <div className="draft-badge">AI Draft</div>
              <pre className="ai-draft">{generatedOutput}</pre>
            </div>

            <div className="feedback-section">
              <p className="feedback-label">Not quite right? Give feedback to iterate:</p>
              <div className="feedback-input-row">
                <input
                  type="text"
                  className="feedback-input"
                  placeholder="E.g., Make it shorter, focus more on database optimization..."
                  value={feedback}
                  onChange={(e) => setFeedback(e.target.value)}
                />
                <button 
                  className="btn-secondary btn-sm" 
                  onClick={() => handleGenerate(true)}
                  disabled={!feedback.trim()}
                >
                  Regenerate 🔄
                </button>
              </div>
            </div>

            <div className="modal-actions apply-actions">
              <button className="btn-secondary" onClick={() => setStep('input')}>← Back</button>
              <button className="btn-primary" onClick={handleApply}>
                ✅ Apply to Resume
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
