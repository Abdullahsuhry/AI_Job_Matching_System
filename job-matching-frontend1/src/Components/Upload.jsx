import React, { useState } from 'react'
import axios from 'axios'

export default function Upload() {
  const [file, setFile] = useState(null)
  const [text, setText] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleFileChange = (e) => setFile(e.target.files[0])

  const uploadFile = async () => {
    if (!file) return
    const form = new FormData()
    form.append('file', file)
    setLoading(true)
    try {
      const res = await axios.post('/api/upload', form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setText(res.data.text || '')
    } catch (err) {
      console.error(err)
      alert('Upload failed')
    } finally {
      setLoading(false)
    }
  }

  const analyze = async () => {
    if (!text) return alert('No text to analyze')
    setLoading(true)
    try {
      const res = await axios.post('/api/analyze', { text })
      setAnalysis(res.data)
    } catch (err) {
      console.error(err)
      alert('Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Upload Resume</h2>
      <input type="file" onChange={handleFileChange} className="mb-4" />
      <div className="space-x-4">
        <button onClick={uploadFile} className="bg-indigo-600 text-white px-4 py-2 rounded">Upload</button>
        <button onClick={analyze} className="bg-green-600 text-white px-4 py-2 rounded">Analyze Text</button>
      </div>

      {loading && <p className="mt-4">Working...</p>}

      {text && (
        <section className="mt-6 p-4 bg-white rounded shadow">
          <h3 className="font-semibold">Extracted Text</h3>
          <pre className="whitespace-pre-wrap text-sm text-gray-700">{text}</pre>
        </section>
      )}

      {analysis && (
        <section className="mt-6 p-4 bg-white rounded shadow">
          <h3 className="font-semibold">Analysis</h3>
          <p><strong>Detected skills:</strong> {analysis.resume_skills.join(', ')}</p>
          <p><strong>Missing skills:</strong> {analysis.missing_skills.join(', ') || 'None'}</p>
          <div className="mt-3">
            <h4 className="font-semibold">Course recommendations</h4>
            <ul>
              {Object.entries(analysis.course_recommendations).map(([skill, recs]) => (
                <li key={skill}><strong>{skill}:</strong> {recs.length ? recs.join(' | ') : 'No suggestions'}</li>
              ))}
            </ul>
          </div>
        </section>
      )}
    </div>
  )
}
