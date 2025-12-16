import React, { useState } from "react";

function RefactoredCode({ originalCode, refactoredCode }) {
  const [view, setView] = useState("single"); // single | compare
  const [copied, setCopied] = useState(false);

  if (!refactoredCode) return null;

  // COPY
  function handleCopy() {
    navigator.clipboard.writeText(refactoredCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  // DOWNLOAD
  function handleDownload() {
    const blob = new Blob([refactoredCode], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "refactored_code.py";
    a.click();

    URL.revokeObjectURL(url);
  }

  // DIFF LOGIC 
  function getDiffLines(original = "", refactored = "") {
    const originalLines = original.split("\n");
    const refactoredLines = refactored.split("\n");

    const maxLength = Math.max(
      originalLines.length,
      refactoredLines.length
    );

    const diff = [];

    for (let i = 0; i < maxLength; i++) {
      const oldLine = originalLines[i];
      const newLine = refactoredLines[i];

      if (oldLine === undefined) {
        diff.push({ type: "added", text: newLine });
      } else if (newLine === undefined) {
        diff.push({ type: "removed", text: oldLine });
      } else if (oldLine !== newLine) {
        diff.push({ type: "removed", text: oldLine });
        diff.push({ type: "added", text: newLine });
      } else {
        diff.push({ type: "same", text: oldLine });
      }
    }

    return diff;
  }

  const diffLines = getDiffLines(originalCode, refactoredCode);

  // RENDER
  return (
    <div className="mt-8 p-6 rounded-2xl bg-[#0d0d0f] border border-[#1a1a1d] shadow-xl text-white">

      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-[#d4a44d]">
          Refactored Code
        </h2>

        <div className="flex gap-3">
          <button
            onClick={() =>
              setView(view === "single" ? "compare" : "single")
            }
            className="px-4 py-1 rounded-lg text-sm font-medium
                       text-[#d4a44d] border border-[#d4a44d]/60
                       hover:bg-black transition"
          >
            {view === "single" ? "Show Diff" : "Single View"}
          </button>

          <button
            onClick={handleCopy}
            className="px-3 py-1 rounded-lg text-sm font-medium
                       text-[#d4a44d] border border-[#d4a44d]/60
                       hover:bg-black transition"
          >
            {copied ? "Copied" : "Copy"}
          </button>

          <button
            onClick={handleDownload}
            className="px-3 py-1 rounded-lg text-sm font-medium
                       text-black bg-yellow-500 hover:bg-yellow-400 transition"
          >
             Download
          </button>
        </div>
      </div>

      {/* SINGLE VIEW */}
      {view === "single" && (
        <pre className="bg-[#101012] border border-[#1f1f22]
                        rounded-xl p-4 text-sm text-gray-200
                        overflow-x-auto font-mono">
{refactoredCode}
        </pre>
      )}

      {/* DIFF VIEW */}
      {view === "compare" && (
        <pre className="bg-[#101012] border border-[#1f1f22]
                        rounded-xl p-4 text-sm font-mono overflow-x-auto">
          {diffLines.map((line, index) => (
            <div
              key={index}
              className={
                line.type === "added"
                  ? "text-green-400"
                  : line.type === "removed"
                  ? "text-red-400"
                  : "text-gray-300"
              }
            >
              {line.type === "added"
                ? "+ "
                : line.type === "removed"
                ? "- "
                : "  "}
              {line.text}
            </div>
          ))}
        </pre>
      )}
    </div>
  );
}

export default RefactoredCode;
