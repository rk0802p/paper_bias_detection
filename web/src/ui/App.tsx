import React, { useState } from 'react'
import axios from 'axios'

const panel: React.CSSProperties = {
  background: 'var(--panel)',
  boxShadow: '0 2px 12px rgba(0,0,0,0.08)',
  borderRadius: 8,
  padding: 16,
  border: '1px solid rgba(0,0,0,0.05)'
}

function Section({name, data}: {name: string, data: any}){
  return (
    <div style={{...panel, marginBottom: 16}}>
      <h3 style={{marginTop:0}}>{name} — {data?.best_similarity_percent?.toFixed(2)}%</h3>
      <div style={{fontStyle:'italic', color:'#6b5b53'}}>{data?.category}</div>
      {data?.matches?.length ? (
        <table style={{width:'100%', marginTop:12}}>
          <thead>
            <tr>
              <th align="left">% Match</th>
              <th align="left">Title</th>
              <th align="left">Link</th>
            </tr>
          </thead>
          <tbody>
            {data.matches.map((m: any, i: number) => (
              <tr key={i}>
                <td>{m.percent.toFixed(2)}%</td>
                <td>{m.title}</td>
                <td><a href={m.url} style={{color:'var(--accent)'}} target="_blank">Open</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div style={{marginTop:8, color:'#6b5b53'}}>No close matches found.</div>
      )}
    </div>
  )
}

export default function App(){
  const [file, setFile] = useState<File|null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string|null>(null)
  const [report, setReport] = useState<any>(null)

  const onUpload = async () => {
    if(!file) return
    setLoading(true); setError(null); setReport(null)
    try{
      const form = new FormData()
      form.append('file', file)
      const resp = await axios.post('/analyze', form, { baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000', headers: { 'Content-Type': 'multipart/form-data' } })
      setReport(resp.data)
    }catch(e:any){
      setError(e?.response?.data?.error || e.message)
    }finally{
      setLoading(false)
    }
  }

  return (
    <div style={{maxWidth: 1100, margin:'0 auto', padding: 24}}>
      <header style={{marginBottom: 24}}>
        <h1 style={{margin:0}}>Research Paper Plagiarism & Similarity Analysis</h1>
        <div style={{color:'#6b5b53'}}></div>
      </header>

      <div style={{display:'grid', gridTemplateColumns:'1fr', gap: 16}}>
        <div style={panel}>
          <h3 style={{marginTop:0}}>Upload Academic Paper (PDF)</h3>
          <input type="file" accept="application/pdf" onChange={e=> setFile(e.target.files?.[0] || null)} />
          <button onClick={onUpload} disabled={!file || loading} style={{marginLeft:12, background:'var(--accent)', color:'white', border:'none', padding:'8px 14px', borderRadius:6}}>
            {loading ? 'Analyzing…' : 'Analyze'}
          </button>
          {error && <div style={{color:'#a00000', marginTop:8}}>{error}</div>}
        </div>

        {report && (
          <>
            <div style={panel}>
              <h2 style={{marginTop:0}}>Overall Similarity</h2>
              <div style={{fontSize: 28, fontWeight: 700}}>{report.overall_percent?.toFixed(2)}%</div>
              <div style={{color:'#6b5b53'}}>{report.overall_category}</div>
            </div>

            <Section name="Title" data={report.sections?.Title} />
            <Section name="Abstract" data={report.sections?.Abstract} />
            <Section name="Methodology" data={report.sections?.Methodology} />
            <Section name="Conclusions" data={report.sections?.Conclusions} />
          </>
        )}
      </div>
    </div>
  )
}
