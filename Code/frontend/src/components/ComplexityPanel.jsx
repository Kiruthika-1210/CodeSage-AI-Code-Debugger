import React from "react";

function ComplexityPanel({ data }) {
  // Guard: nothing to render yet
  if (!data) return null;

  // Destructure with SAFE defaults
  const {
    nestingDepth = "—",
    loopDepth = "—",
    bigO = "—",
    score = 0,
    patterns = [],
  } = data;

  /* =======================
     Color & Label Helpers
  ======================= */

  const getScoreColor = (score) => {
    if (score >= 80) return "bg-green-500";
    if (score >= 50) return "bg-yellow-400";
    return "bg-red-500";
  };

  const getScoreTextColor = (score) => {
    if (score >= 80) return "text-green-400";
    if (score >= 50) return "text-yellow-400";
    return "text-red-400";
  };

  const getScoreText = (score) => {
    if (score >= 80) return "Good Complexity";
    if (score >= 50) return "Moderate Complexity";
    return "High Complexity";
  };

  const getBigOColor = (bigO) => {
    if (["O(1)", "O(log n)", "O(n)"].includes(bigO)) {
      return "text-green-400";
    }
    if (["O(n log n)", "O(n²)", "O(n^2)"].includes(bigO)) {
      return "text-yellow-400";
    }
    return "text-red-400";
  };

  /* =======================
     RENDER
  ======================= */

  return (
    <div className="mt-8 p-6 rounded-2xl bg-[#0d0d0f] border border-[#1a1a1d] shadow-xl text-white">

      <h2 className="text-xl font-semibold mb-6 text-[#d4a44d]">
        Complexity Analysis
      </h2>

      {/* Metrics */}
      <div className="space-y-3 mb-6">
        <div className="flex justify-between">
          <span className="text-gray-400">Nesting Depth</span>
          <span className="font-medium">{nestingDepth}</span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-400">Loop Depth</span>
          <span className="font-medium">{loopDepth}</span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-400">Estimated Big-O</span>
          <span className={`font-medium ${getBigOColor(bigO)}`}>
            {bigO}
          </span>
        </div>
      </div>

      {/* Patterns */}
      {patterns.length > 0 && (
        <div className="mb-6">
          <p className="text-gray-400 mb-2">Patterns Identified</p>
          <div className="flex flex-wrap gap-2">
            {patterns.map((pattern, index) => (
              <span
                key={index}
                className="px-3 py-1 rounded-full text-sm bg-[#1a1a1d] border border-[#262629] text-gray-300"
              >
                {pattern}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Score */}
      <div>
        <div className="flex justify-between mb-2">
          <span className="text-gray-400">Complexity Score</span>
          <span className={`font-medium ${getScoreTextColor(score)}`}>
            {score}/100
          </span>
        </div>

        <div className="w-full h-3 rounded-full bg-[#1a1a1d] overflow-hidden">
          <div
            className={`h-full ${getScoreColor(score)}`}
            style={{ width: `${score}%` }}
          />
        </div>

        <p className={`mt-2 text-sm ${getScoreTextColor(score)}`}>
          {getScoreText(score)}
        </p>
      </div>

    </div>
  );
}

export default ComplexityPanel;
