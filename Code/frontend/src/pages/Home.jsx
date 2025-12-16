import { useState, useEffect } from "react";

import CodeEditor from "../components/CodeEditor";
import IssueList from "../components/IssueList";
import ComplexityPanel from "../components/ComplexityPanel";
import ScorePanel from "../components/ScorePanel";
import RefactoredCode from "../components/RefactoredCode";
import ExplanationPanel from "../components/ExplanationPanel";
import VersionHistory from "../components/VersionHistory";
import TestCasesPanel from "../components/TestCasesPanel";

import {
  analyzeCode,
  refactorCode,
  analyzeAndRefactor,
  saveVersion,
  getVersionHistory,
  deleteVersion,
  clearAllVersions,
  generateTestCases,
} from "../utils/api";


function Home({ theme, setTheme }) {
  /* =======================
     CORE STATE
  ======================= */
  const [code, setCode] = useState("");

  const [issues, setIssues] = useState([]);
  const [activeFilter, setActiveFilter] = useState("all");

  const [complexity, setComplexity] = useState(null);

  const [scores, setScores] = useState({
    finalScore: null,
  });

  const [refactoredCode, setRefactoredCode] = useState("");
  const [explanation, setExplanation] = useState(null);

  const [versionHistory, setVersionHistory] = useState([]);

  const [testCases, setTestCases] = useState(null);

  /* =======================
     LOAD VERSION HISTORY (PHASE 4)
  ======================= */
  useEffect(() => {
    getVersionHistory()
      .then(setVersionHistory)
      .catch(console.error);
  }, []);

  /* =======================
     RESET ON EMPTY CODE
  ======================= */
  useEffect(() => {
    if (code.trim() === "") {
      setIssues([]);
      setComplexity(null);
      setScores({ finalScore: null });
      setRefactoredCode("");
      setExplanation(null);
    }
  }, [code]);

  /* =======================
     DERIVED STATE
  ======================= */
  const canSaveVersion =
    issues.length > 0 ||
    complexity !== null ||
    scores.finalScore !== null ||
    refactoredCode !== "";

  /* =======================
     HANDLERS
  ======================= */
  async function handleAnalyze() {
    const result = await analyzeCode(code);
    setIssues(result.issues);
    const c = result.complexity;
    setComplexity({
      nestingDepth: c.nesting?.max_nesting_depth ?? "—",
      loopDepth: c.loops?.max_loop_depth ?? "—",
      bigO: c.big_o ?? "—",
      score: c.score ?? 0,
      patterns: c.loops?.nested_loops_detected ? ["Nested Loops"] : []
    });
    setScores({
      readability: result.readability,
      maintainability: result.maintainability,
      documentation: result.documentation,
      style: result.style,
      finalScore: result.qualityScore,
    });
  }

  async function handleRefactor() {
    const result = await refactorCode(code, issues);
    setRefactoredCode(result.refactoredCode);
    setExplanation(result.explanation);
  }


  async function handleFullPipeline() {
    const result = await analyzeAndRefactor(code);

    setIssues(result.issues);
    setComplexity(result.complexity);
    setScores({
      readability: result.readability,
      maintainability: result.maintainability,
      style: result.style,
      documentation: result.documentation,
      finalScore: result.qualityScore,
    });
    setRefactoredCode(result.refactoredCode);
    setExplanation(result.explanation);

    // 🔥 AUTO-SAVE TO BACKEND
    await saveVersion({
      original_code: code,
      refactored_code: result.refactoredCode,
      issues: result.issues,
      complexity: result.complexity,
      qualityScore: result.qualityScore,
    });

    // 🔄 Reload persisted history
    const history = await getVersionHistory();
    setVersionHistory(history);
  }

  async function handleSaveVersion() {
    try {
      await saveVersion({
        original_code: code,
        refactored_code: refactoredCode || code,
        issues,
        complexity,
        qualityScore: scores.finalScore,
      });

      const history = await getVersionHistory();
      setVersionHistory(history);
    } catch (err) {
      console.error("Save version failed:", err);
    }
  }

  async function handleDeleteVersion(versionId) {
    await deleteVersion(versionId);
    const history = await getVersionHistory();
    setVersionHistory(history);
  }
  
  async function handleClearAllVersions() {
    await clearAllVersions();
    setVersionHistory([]);
  }

  async function handleGenerateTests() {
    try {
      const tests = await generateTestCases(
        refactoredCode || code, // prefer refactored code
        issues
      );
      setTestCases(tests);
    } catch (err) {
      console.error("Test case generation failed", err);
    }
  }



  /* =======================
     RENDER
  ======================= */
  return (
    <div
      className="min-h-screen bg-neutral-100 dark:bg-neutral-950
                 text-neutral-900 dark:text-neutral-100
                 transition-colors duration-300"
    >
      <div className="mx-auto max-w-6xl px-6 py-8 space-y-8">

        {/* 🌗 THEME TOGGLE */}
        <div className="flex justify-end">
          <button
            onClick={() =>
              setTheme(theme === "dark" ? "light" : "dark")
            }
            className="px-3 py-1 rounded-lg text-sm font-medium
                       border border-neutral-700 dark:border-neutral-600
                       hover:bg-neutral-200 dark:hover:bg-neutral-800
                       transition"
          >
            {theme === "dark" ? "🌞 Light Mode" : "🌙 Dark Mode"}
          </button>
        </div>

        <CodeEditor
          code={code}
          onCodeChange={setCode}
          onAnalyze={handleAnalyze}
          onRefactor={handleRefactor}
          onFullPipeline={handleFullPipeline}
          onGenerateTests={handleGenerateTests}
        />

        <IssueList
          issues={issues}
          activeFilter={activeFilter}
          setActiveFilter={setActiveFilter}
          onIssueClick={(line) => console.log("Jump to line:", line)}
        />

        {complexity && <ComplexityPanel data={complexity} />}

        {scores.finalScore !== null && <ScorePanel data={scores} />}

        {refactoredCode && (
          <RefactoredCode
            originalCode={code}
            refactoredCode={refactoredCode}
          />
        )}

        {explanation && <ExplanationPanel data={explanation} />}

        {Array.isArray(testCases) && (
          <TestCasesPanel testCases={testCases} />
        )}


        <VersionHistory
          versions={versionHistory}
          onSaveVersion={handleSaveVersion}
          onDeleteVersion={handleDeleteVersion}
          onClearAll={handleClearAllVersions}
          canSave={canSaveVersion}
        />

      </div>
    </div>
  );
}

export default Home;
