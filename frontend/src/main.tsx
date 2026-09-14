import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Upload,
  FileText,
  ArrowUpRight,
  Sparkles,
  History,
  BookOpen,
  Check,
  X,
  Download,
  Trash2,
  ChevronDown,
  Activity,
} from "lucide-react";
import "./styles.css";
import "./demo.css";
import "./role-plan.css";
import "./template.css";

type Analysis = {
  history_id?: number;
  final_score: number;
  target_role: string;
  candidate_name: string;
  analysis_date: string;
  insight: string;
  strengths: string[];
  improvements: string[];
  learning_plan: {
    skill: string;
    category: string;
    why: string;
    proof: string;
  }[];
  resume_rewrite: string[];
  tailored_resume: {
    notice: string;
    headline: string;
    summary: string;
    skills: string[];
    project_title: string;
    project_bullets: string[];
    next_step: string;
  };
  matched_skills: string[];
  missing_skills: { name: string; category: string }[];
  missing_keywords: string[];
  matched_keywords: string[];
  sections: Record<string, boolean>;
  score_explanation: string;
  skill_match: number;
  keyword_match: number;
  semantic_similarity: number;
  completeness: number;
  formatting: number;
  metadata: { filename: string; file_type: string; character_count: number };
};

type HistoryItem = {
  id: number;
  target_role: string;
  score: number;
  analysis_date: string;
};
const API = "";

async function readJsonResponse(response: Response) {
  const text = await response.text();
  if (!text) {
    throw new Error(
      "The server returned an empty response. Please start the backend API first.",
    );
  }
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`Unexpected server response: ${text.slice(0, 200)}`);
  }
}

const demoJob =
  "Role: AI Engineer. Build and deploy machine learning systems using Python, deep learning, NLP, TensorFlow, PyTorch, SQL, Docker, REST APIs and Git.";
const demoResume = `Alex Morgan\n alex@example.com | +1 555 0199\n\nSUMMARY\nComputer science student building practical Python and machine learning applications.\n\nEDUCATION\nB.Tech Computer Science and Engineering, 2026\n\nSKILLS\nPython, SQL, Git, Machine Learning, scikit-learn, Flask\n\nPROJECTS\nRecommendation Engine - Used Python, scikit-learn and machine learning for ranking.\nResume Analyzer - Built a Flask application for resume matching.\n\nCERTIFICATIONS\nMachine Learning Foundations`;

function App() {
  const [view, setView] = useState<"analyze" | "history" | "about">("analyze");
  const [file, setFile] = useState<File | null>(null);
  const [job, setJob] = useState("");
  const [result, setResult] = useState<Analysis | null>(null);
  const [demoMode, setDemoMode] = useState(false);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [showFormula, setShowFormula] = useState(false);
  useEffect(() => {
    loadHistory();
  }, []);
  async function loadHistory() {
    try {
      const response = await fetch(`${API}/api/history`);
      const data = await readJsonResponse(response);
      setHistory(data);
    } catch {
      /* API may not be running yet */
    }
  }
  function chooseFile(selected: File | undefined) {
    if (!selected) return;
    if (
      ![
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      ].includes(selected.type)
    ) {
      setMessage("Upload a PDF or DOCX file.");
      return;
    }
    setDemoMode(false);
    setFile(selected);
    setMessage("");
  }
  async function runAnalysis() {
    if (demoMode) {
      setBusy(true);
      setMessage("Running the sample through the same analysis pipeline...");
      try {
        const response = await fetch(`${API}/api/demo`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            resume_text: demoResume,
            job_description: job,
          }),
        });
        const data = await readJsonResponse(response);
        if (!response.ok) throw new Error(data.error);
        setResult(data);
        await loadHistory();
      } catch (error) {
        setMessage(
          error instanceof Error ? error.message : "The API is unavailable.",
        );
      } finally {
        setBusy(false);
      }
      return;
    }
    if (!file || !job.trim()) {
      setMessage("Add a resume and job description to continue.");
      return;
    }
    setBusy(true);
    setMessage("");
    const form = new FormData();
    form.append("resume", file);
    form.append("job_description", job);
    try {
      const response = await fetch(`${API}/api/analyze`, {
        method: "POST",
        body: form,
      });
      const data = await readJsonResponse(response);
      if (!response.ok) throw new Error(data.error);
      setResult(data);
      await loadHistory();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "The API is unavailable. Start the Flask server and try again.",
      );
    } finally {
      setBusy(false);
    }
  }
  function runDemo() {
    setDemoMode(true);
    setFile(new File(["sample"], "demo-resume.txt", { type: "text/plain" }));
    setJob(demoJob);
    setMessage(
      "Demo data loaded. Click Analyze to run it through the real API pipeline.",
    );
  }
  function downloadDemoResume() {
    const blob = new Blob([demoResume], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "resumate-demo-resume.txt";
    link.click();
    URL.revokeObjectURL(url);
  }
  async function downloadReport() {
    if (!result) return;
    const response = await fetch(`${API}/api/report`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(result),
    });
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "resumate-analysis.pdf";
    link.click();
    URL.revokeObjectURL(url);
  }
  async function removeHistory(id: number) {
    await fetch(`${API}/api/history/${id}`, { method: "DELETE" });
    await loadHistory();
  }
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">
            <Sparkles size={16} />
          </span>
          <span>
            RESUMATE <em>AI</em>
          </span>
        </div>
        <div className="eyebrow">CAREER INTELLIGENCE</div>
        <nav>
          <button
            className={view === "analyze" ? "active" : ""}
            onClick={() => setView("analyze")}
          >
            <Activity size={17} /> Analyze
          </button>
          <button
            className={view === "history" ? "active" : ""}
            onClick={() => setView("history")}
          >
            <History size={17} /> History
          </button>
          <button
            className={view === "about" ? "active" : ""}
            onClick={() => setView("about")}
          >
            <BookOpen size={17} /> About
          </button>
        </nav>
        <div className="sidebar-footer">
          <div className="status-dot" /> Local NLP workspace
          <br />
          <span>Privacy-first analysis</span>
        </div>
      </aside>
      <main className="main">
        <header className="topbar">
          <div>
            <span className="breadcrumb">
              Workspace /{" "}
              {view === "analyze"
                ? "New analysis"
                : view[0].toUpperCase() + view.slice(1)}
            </span>
            <h1>
              {view === "analyze"
                ? "Your resume, understood."
                : view === "history"
                  ? "Analysis archive."
                  : "The thinking behind it."}
            </h1>
          </div>
          <button className="demo-button" onClick={runDemo}>
            <Sparkles size={15} /> Load demo data
          </button>
        </header>
        {view === "analyze" && (
          <>
            {!result ? (
              <section className="analysis-layout">
                <div className="input-column">
                  <div className="step-line">
                    <span className="current">01</span>
                    <span>Upload resume</span>
                    <i />
                    <span>02</span>
                    <span>Add role</span>
                    <i />
                    <span>03</span>
                    <span>Analyze</span>
                  </div>
                  <div className="panel upload-panel">
                    <div className="panel-kicker">STEP 01 / RESUME</div>
                    <h2>Start with your story.</h2>
                    <p className="muted">
                      We read the structure and language of your resume to find
                      the signal.
                    </p>
                    <label
                      className="dropzone"
                      onDragOver={(event) => event.preventDefault()}
                      onDrop={(event) => {
                        event.preventDefault();
                        chooseFile(event.dataTransfer.files[0]);
                      }}
                    >
                      <input
                        type="file"
                        accept=".pdf,.docx"
                        onChange={(event) =>
                          chooseFile(event.target.files?.[0])
                        }
                      />
                      {file ? (
                        <>
                          <span className="file-icon">
                            <FileText />
                          </span>
                          <strong>{file.name}</strong>
                          <small>
                            {(file.size / 1024).toFixed(1)} KB · ready for
                            analysis
                          </small>
                          <button
                            type="button"
                            className="remove-file"
                            onClick={(event) => {
                              event.preventDefault();
                              setFile(null);
                            }}
                          >
                            <X size={14} /> Remove
                          </button>
                        </>
                      ) : (
                        <>
                          <span className="upload-icon">
                            <Upload />
                          </span>
                          <strong>Drop your resume here</strong>
                          <small>PDF or DOCX · up to 8 MB</small>
                          <span className="browse">
                            Browse files <ArrowUpRight size={13} />
                          </span>
                        </>
                      )}
                    </label>
                    {demoMode && (
                      <div className="demo-profile">
                        <div>
                          <span className="panel-kicker">
                            DEMO RESUME / ALEX MORGAN
                          </span>
                          <strong>AI Engineer starter profile</strong>
                          <p>
                            Skills in this sample: Python, SQL, Git, Machine
                            Learning, scikit-learn and Flask.
                          </p>
                        </div>
                        <button onClick={downloadDemoResume}>
                          <Download size={14} /> Get sample resume
                        </button>
                        <div className="demo-gap">
                          <span>Build next for this role</span>
                          <b>Deep Learning · NLP · TensorFlow · PyTorch · Docker · REST APIs</b>
                        </div>
                      </div>
                    )}
                  </div>
                  <div className="panel job-panel">
                    <div className="panel-kicker">STEP 02 / TARGET ROLE</div>
                    <div className="job-heading">
                      <div>
                        <h2>What are you aiming for?</h2>
                        <p className="muted">
                          Paste the job description you want to measure against.
                        </p>
                      </div>
                      <span className="char-count">{job.length} chars</span>
                    </div>
                    <textarea
                      value={job}
                      onChange={(event) => setJob(event.target.value)}
                      placeholder="Paste a job description here..."
                    />
                    <button
                      className="example-link"
                      onClick={() => setJob(demoJob)}
                    >
                      Use an example role <ArrowUpRight size={14} />
                    </button>
                  </div>
                  <button
                    className="analyze-button"
                    onClick={runAnalysis}
                    disabled={busy}
                  >
                    {busy ? (
                      <>
                        <span className="spinner" /> Reading and comparing...
                      </>
                    ) : (
                      <>
                        Analyze my resume <ArrowUpRight size={17} />
                      </>
                    )}
                  </button>
                  {message && (
                    <div className="notice">
                      <X size={15} /> {message}
                    </div>
                  )}
                </div>
                <div className="intro-column">
                  <span className="intro-number">01—03</span>
                  <h2>
                    From page
                    <br />
                    to <span>possibility.</span>
                  </h2>
                  <p>
                    Resumate turns the gap between what you wrote and what
                    employers need into a clear, actionable next step.
                  </p>
                  <div className="pipeline">
                    <span>Resume</span>
                    <i />
                    <span>Language</span>
                    <i />
                    <span>Match</span>
                    <i />
                    <span>Insight</span>
                  </div>
                  <div className="quote">
                    “The best career advice starts with an honest read of where
                    you are.”
                  </div>
                </div>
              </section>
            ) : (
              <ResultView
                result={result}
                showFormula={showFormula}
                setShowFormula={setShowFormula}
                onDownload={downloadReport}
                onReset={() => setResult(null)}
              />
            )}
          </>
        )}
        {view === "history" && (
          <HistoryView
            items={history}
            onOpen={async (id) => {
              const response = await fetch(`${API}/api/history/${id}`);
              const data = await readJsonResponse(response);
              setResult(data);
              setView("analyze");
            }}
            onDelete={removeHistory}
          />
        )}
        {view === "about" && <AboutView />}
      </main>
    </div>
  );
}

function ResultView({
  result,
  showFormula,
  setShowFormula,
  onDownload,
  onReset,
}: {
  result: Analysis;
  showFormula: boolean;
  setShowFormula: (value: boolean) => void;
  onDownload: () => void;
  onReset: () => void;
}) {
  const metrics = [
    ["Skill match", result.skill_match],
    ["Keyword match", result.keyword_match],
    ["Semantic similarity", result.semantic_similarity],
    ["Completeness", result.completeness],
    ["Formatting", result.formatting],
  ];
  const label =
    result.final_score >= 80
      ? "Strong match"
      : result.final_score >= 60
        ? "Good match"
        : result.final_score >= 40
          ? "Moderate match"
          : "Needs improvement";
  return (
    <section className="results">
      <div className="result-head">
        <div>
          <span className="breadcrumb">
            REPORT / {result.metadata.filename}
          </span>
          <h2>Your resume intelligence report.</h2>
          <p className="muted">{result.target_role}</p>
        </div>
        <div className="result-actions">
          <button className="secondary-button" onClick={onReset}>
            New analysis
          </button>
          <button className="dark-button" onClick={onDownload}>
            <Download size={16} /> Download report
          </button>
        </div>
      </div>
      <div className="score-grid">
        <div className="score-card">
          <span className="panel-kicker">ATS-STYLE COMPATIBILITY</span>
          <div className="big-score">
            {Math.round(result.final_score)}
            <small>/100</small>
          </div>
          <div className="score-label">
            <span className="score-pip" /> {label}
          </div>
          <p>{result.score_explanation}</p>
        </div>
        <div className="metrics-card">
          <div className="metrics-header">
            <span className="panel-kicker">THE BREAKDOWN</span>
            <button onClick={() => setShowFormula(!showFormula)}>
              {showFormula ? "Hide method" : "How is this calculated?"}{" "}
              <ChevronDown size={14} />
            </button>
          </div>
          {metrics.map(([name, value]) => (
            <div className="metric" key={name as string}>
              <div>
                <span>{name}</span>
                <b>{value}%</b>
              </div>
              <div className="bar">
                <i style={{ width: `${value}%` }} />
              </div>
            </div>
          ))}
          {showFormula && (
            <div className="formula">
              40% skills · 25% keywords · 20% semantic similarity · 10%
              completeness · 5% formatting
            </div>
          )}
        </div>
      </div>
      <div className="insight-banner">
        <Sparkles size={20} />
        <div>
          <span className="panel-kicker">RESUME INTELLIGENCE</span>
          <p>{result.insight}</p>
        </div>
      </div>
      <RoleFitPlan result={result} />
      <div className="result-columns">
        <div className="result-panel">
          <div className="panel-kicker">MATCHED SKILLS</div>
          <h3>What already speaks to the role</h3>
          <div className="chips">
            {result.matched_skills.length ? (
              result.matched_skills.map((skill) => (
                <span className="chip matched" key={skill}>
                  <Check size={13} /> {skill}
                </span>
              ))
            ) : (
              <span className="muted">No catalogued skills detected.</span>
            )}
          </div>
          <div className="panel-kicker gap-kicker">NOT DETECTED IN RESUME</div>
          <h3>Potential areas to explore</h3>
          <div className="chips">
            {result.missing_skills.length ? (
              result.missing_skills.map((skill) => (
                <span className="chip missing" key={skill.name}>
                  <span /> {skill.name}
                </span>
              ))
            ) : (
              <span className="muted">No skill gaps detected.</span>
            )}
          </div>
        </div>
        <div className="result-panel">
          <div className="panel-kicker">EVIDENCE-BASED NOTES</div>
          <h3>Strengths</h3>
          {result.strengths.map((item) => (
            <p className="bullet" key={item}>
              <Check size={15} /> {item}
            </p>
          ))}
          <h3 className="improve-title">Areas to improve</h3>
          {result.improvements.map((item) => (
            <p className="bullet improve" key={item}>
              <ArrowUpRight size={15} /> {item}
            </p>
          ))}
        </div>
      </div>
      <div className="sections-strip">
        <span className="panel-kicker">SECTION DETECTION</span>
        <div>
          {Object.entries(result.sections).map(([section, detected]) => (
            <span
              className={detected ? "section detected" : "section"}
              key={section}
            >
              {detected ? <Check size={12} /> : <X size={12} />} {section}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}
function RoleFitPlan({ result }: { result: Analysis }) {
  function downloadTailoredResume() {
    const template = result.tailored_resume;
    const text = `${template.headline}\n\nSUMMARY\n${template.summary}\n\nSKILLS TO BUILD / VERIFY\n${template.skills.join(', ')}\n\nPROJECT TEMPLATE\n${template.project_title}\n${template.project_bullets.map((bullet) => `- ${bullet}`).join('\n')}\n\nNEXT STEP\n${template.next_step}\n\n${template.notice}`;
    const url = URL.createObjectURL(new Blob([text], { type: 'text/plain' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = `role-ready-${result.target_role.toLowerCase().replace(/\s+/g, '-')}-template.txt`;
    link.click();
    URL.revokeObjectURL(url);
  }
  return (
    <div className="role-plan">
      <div className="panel-kicker">ROLE-READY RESUME PLAN</div>
      <h3>How to move this resume toward {result.target_role}</h3>
      <div className="template-heading">
        <div>
          <span className="plan-label">ROLE-SPECIFIC DEMO RESUME</span>
          <p>Use this as a model for how your resume should look after you build the missing evidence.</p>
        </div>
        <button className="template-download" onClick={downloadTailoredResume}><Download size={14} /> Download template</button>
      </div>
      <div className="template-preview">
        <strong>{result.tailored_resume.headline}</strong>
        <p>{result.tailored_resume.summary}</p>
        <span className="plan-label">SKILLS TO VERIFY BEFORE ADDING</span>
        <div className="plan-chips">{result.tailored_resume.skills.map((skill) => <span className="plan-chip learn" key={skill}>{skill}</span>)}</div>
        <span className="plan-label template-project-label">PROJECT BULLET MODEL</span>
        <b>{result.tailored_resume.project_title}</b>
        {result.tailored_resume.project_bullets.map((bullet) => <p className="template-bullet" key={bullet}>• {bullet}</p>)}
      </div>
      <div className="plan-columns">
        <div>
          <span className="plan-label">ALREADY DETECTED</span>
          <div className="plan-chips">
            {result.matched_skills.map((skill) => (
              <span className="plan-chip have" key={skill}>
                <Check size={12} /> {skill}
              </span>
            ))}
          </div>
        </div>
        <div>
          <span className="plan-label">LEARN / BUILD NEXT</span>
          <div className="plan-chips">
            {result.learning_plan.length ? (
              result.learning_plan.map((item) => (
                <span className="plan-chip learn" key={item.skill}>
                  {item.skill}
                </span>
              ))
            ) : (
              <span className="muted">No catalogued gaps detected.</span>
            )}
          </div>
        </div>
      </div>
      {result.learning_plan.length > 0 && (
        <div className="learning-list">
          {result.learning_plan.map((item) => (
            <div className="learning-item" key={item.skill}>
              <strong>{item.skill}</strong>
              <span>{item.why}</span>
              <small>{item.proof}</small>
            </div>
          ))}
        </div>
      )}
      <div className="rewrite-box">
        <span className="plan-label">HONEST RESUME CHANGES</span>
        {result.resume_rewrite.map((item) => (
          <p key={item}>
            <ArrowUpRight size={14} /> {item}
          </p>
        ))}
      </div>
    </div>
  );
}

function HistoryView({
  items,
  onOpen,
  onDelete,
}: {
  items: HistoryItem[];
  onOpen: (id: number) => void;
  onDelete: (id: number) => void;
}) {
  return (
    <section className="simple-page">
      <div className="page-intro">
        <span className="intro-number">ARCHIVE</span>
        <p>
          Every analysis is stored locally so you can compare your progress over
          time.
        </p>
      </div>
      {items.length ? (
        <div className="history-list">
          {items.map((item) => (
            <div className="history-row" key={item.id}>
              <div className="history-icon">
                <FileText size={18} />
              </div>
              <div>
                <strong>{item.target_role}</strong>
                <small>
                  {new Date(item.analysis_date).toLocaleDateString()}
                </small>
              </div>
              <b>
                {Math.round(item.score)}
                <small>/100</small>
              </b>
              <button onClick={() => onOpen(item.id)}>
                View <ArrowUpRight size={14} />
              </button>
              <button className="icon-button" onClick={() => onDelete(item.id)}>
                <Trash2 size={15} />
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <History size={30} />
          <h2>Your archive is quiet.</h2>
          <p>Completed analyses will appear here.</p>
        </div>
      )}
    </section>
  );
}
function AboutView() {
  return (
    <section className="about-page">
      <span className="intro-number">ABOUT RESUMATE</span>
      <h2>
        Readable intelligence
        <br />
        <span>for career decisions.</span>
      </h2>
      <div className="about-grid">
        <div>
          <h3>What it does</h3>
          <p>
            Resumate AI compares an uploaded resume with a target job
            description. It extracts document text, identifies sections and
            skills, measures keyword overlap, and calculates a transparent
            compatibility score.
          </p>
        </div>
        <div>
          <h3>How the AI works</h3>
          <p>
            PDF and DOCX text is cleaned before a TF-IDF vector representation
            is created. Cosine similarity measures shared language. A rule-based
            skill catalog and section detector make the output explainable
            rather than magical.
          </p>
        </div>
        <div>
          <h3>Built for learning</h3>
          <p>
            Flask, React, SQLite, PyMuPDF, python-docx, scikit-learn, and
            ReportLab keep the system local, inspectable, and easy to extend
            with a sentence-transformers model later.
          </p>
        </div>
        <div>
          <h3>Important limitation</h3>
          <p>
            This is an ATS-style compatibility estimate, not an official score
            from any applicant tracking system. A missing detection is not proof
            that a person lacks a skill.
          </p>
        </div>
      </div>
    </section>
  );
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
