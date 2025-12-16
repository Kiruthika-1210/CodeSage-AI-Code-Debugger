const BASE_URL = "http://127.0.0.1:8000";

/* =====================================================
   SESSION ID (STABLE & PERSISTENT)
===================================================== */
export const sessionId =
  localStorage.getItem("codesage_session") ??
  (() => {
    const id = crypto.randomUUID();
    localStorage.setItem("codesage_session", id);
    return id;
  })();

/* =====================================================
   ANALYZE CODE
===================================================== */
export async function analyzeCode(code) {
  const res = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });

  if (!res.ok) throw new Error("Analyze failed");
  return await res.json();
}


/* =====================================================
   AI REFACTOR
===================================================== */
export async function refactorCode(code, issues = []) {
  const res = await fetch(`${BASE_URL}/ai/refactor`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code, issues }),
  });

  const data = await res.json();

  return {
    refactoredCode: data.refactored_code,
    explanation: data.notes,
  };
}

/* =====================================================
   ANALYZE + REFACTOR
===================================================== */
export async function analyzeAndRefactor(code) {
  const res = await fetch(`${BASE_URL}/ai/analyze-and-refactor`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });

  if (!res.ok) throw new Error("Pipeline failed");
  return res.json();
}

/* =====================================================
   TEST CASES
===================================================== */
export async function generateTestCases(code) {
  const res = await fetch(`${BASE_URL}/ai/testcases`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });

  if (!res.ok) throw new Error("Testcase generation failed");
  const data = await res.json();
  return data.test_cases ?? [];
}

/* =====================================================
   VERSION HISTORY
===================================================== */
export async function getVersionHistory() {
  const res = await fetch(`${BASE_URL}/versions/${sessionId}`);
  if (!res.ok) return [];
  const data = await res.json();
  return data.history ?? [];
}

export async function getVersionDetails(versionId) {
  const res = await fetch(
    `${BASE_URL}/versions/version/${versionId}`
  );

  if (!res.ok) throw new Error("Get version failed");
  const data = await res.json();
  return data.version;
}

export async function saveVersion(snapshot) {
  const res = await fetch(`${BASE_URL}/versions/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId,
      ...snapshot,
    }),
  });

  if (!res.ok) throw new Error("Save version failed");
  return res.json();
}

export async function deleteVersion(versionId) {
  const res = await fetch(
    `${BASE_URL}/versions/version/${versionId}`,
    { method: "DELETE" }
  );

  if (!res.ok) throw new Error("Delete version failed");
  return res.json();
}

export async function clearAllVersions() {
  const res = await fetch(`${BASE_URL}/versions/${sessionId}`, {
    method: "DELETE",
  });

  if (!res.ok) throw new Error("Clear versions failed");
  return res.json();
}
