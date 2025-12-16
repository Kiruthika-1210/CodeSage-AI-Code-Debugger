import { useState } from "react";

function TestCasesPanel({ testCases }) {
  const [activeIndex, setActiveIndex] = useState(0);

  if (!Array.isArray(testCases) || testCases.length === 0) {
    return null;
  }

  const activeCase = testCases[activeIndex];

  return (
    <div className="mt-8 p-6 rounded-2xl bg-[#0d0d0f] border border-[#1a1a1d] shadow-xl text-white">

      {/* Header */}
      <h2 className="flex items-center gap-2 text-xl font-semibold text-[#d4a44d] mb-4">
        🧪 Test Cases
      </h2>

      {/* Tabs (LeetCode style) */}
      <div className="flex gap-2 mb-6">
        {testCases.map((_, idx) => (
          <button
            key={idx}
            onClick={() => setActiveIndex(idx)}
            className={`px-3 py-1 rounded-md text-sm font-medium transition
              ${
                activeIndex === idx
                  ? "bg-yellow-500 text-black"
                  : "bg-neutral-800 text-gray-300 hover:bg-neutral-700"
              }`}
          >
            Case {idx + 1}
          </button>
        ))}
      </div>

      {/* Active Test Case */}
      <div className="rounded-xl border border-[#1f1f22] bg-[#101012] p-5 space-y-4">

        {/* Case Name */}
        {activeCase.name && (
          <h3 className="text-yellow-400 font-semibold">
            {activeCase.name}
          </h3>
        )}

        {/* Input (DISPLAY ONLY — no raw JSON) */}
        <div>
          <p className="text-gray-400 text-sm mb-1">Input</p>
          <pre className="bg-black rounded-md p-3 text-sm overflow-x-auto">
{activeCase.input?.display ?? "—"}
          </pre>
        </div>

        {/* Expected Output */}
        <div>
          <p className="text-gray-400 text-sm mb-1">Expected</p>
          <pre className="bg-black rounded-md p-3 text-sm overflow-x-auto">
{Array.isArray(activeCase.expected)
  ? `[${activeCase.expected.join(", ")}]`
  : String(activeCase.expected)}
          </pre>
        </div>

      </div>
    </div>
  );
}

export default TestCasesPanel;
