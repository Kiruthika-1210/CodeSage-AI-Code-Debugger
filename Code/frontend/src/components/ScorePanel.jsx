import React from "react";

function ScorePanel({ data }) {

  const getBarColor = (score) => {
    if (score >= 75) return "bg-green-500";
    if (score >= 50) return "bg-yellow-400";
    return "bg-red-500";
  };

  const getTextColor = (score) => {
    if (score >= 80) return "text-green-400";
    if (score >= 50) return "text-yellow-400";
    return "text-red-400";
  };

  const getLabel = (score) => {
    if (score >= 85) return "Excellent";
    if (score >= 70) return "Good";
    if (score >= 50) return "Fair";
    return "Poor";
  };
  
  const ScoreRow = ({ label, value, tooltip }) => {
    const safeValue = typeof value === "number" ? value : 0;
    
    const barColor = getBarColor(safeValue);
    const textColor = getTextColor(safeValue);
    
    return (
    <div className="space-y-1">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-2">
          <span className="text-gray-300">{label}</span>

          <span className="relative group text-gray-500 cursor-help text-sm">
            ⓘ
            <span
              className="
                absolute left-1/2 -translate-x-1/2 top-6
                hidden group-hover:block
                bg-black text-gray-300 text-xs
                px-3 py-1 rounded-md
                border border-[#262629]
                whitespace-nowrap z-10
              "
            >
              {tooltip}
            </span>
          </span>
        </div>

        {/* SCORE + LABEL */}
        <div className="flex items-center gap-3">
          <span className={`font-medium ${textColor}`}>
            {safeValue}/100
          </span>
          <span className={`text-xs ${textColor}`}>
            {getLabel(safeValue)}
          </span>
        </div>
      </div>

      <div className="w-full h-3 rounded-full bg-[#1a1a1d] overflow-hidden">
        <div
          className={`h-full ${barColor}`}
          style={{ width: `${safeValue}%` }}
        />
      </div>
    </div>
    );
  };


  return (
    <div className="mt-8 p-6 rounded-2xl bg-[#0d0d0f] border border-[#1a1a1d] shadow-xl text-white">

      <h2 className="text-xl font-semibold mb-6 text-[#d4a44d]">
        Quality Scores
      </h2>

      <div className="space-y-5 mb-8">
        <ScoreRow
          label="Readability"
          value={data.readability}
          tooltip="How easy the code is to understand"
        />

        <ScoreRow
          label="Maintainability"
          value={data.maintainability}
          tooltip="Ease of modifying and extending the code"
        />

        <ScoreRow
          label="Style"
          value={data.style}
          tooltip="Code formatting and naming conventions"
        />

        <ScoreRow
          label="Documentation"
          value={data.documentation}
          tooltip="Presence and quality of comments/docstrings"
        />
      </div>

      <div>
        <div className="flex justify-between mb-2">
          <span className="text-gray-400">Final Score</span>
          <span className={`font-bold text-lg ${getTextColor(data.finalScore)}`}>
            {data.finalScore}/100
          </span>
        </div>

        <div className="w-full h-5 rounded-full bg-[#1a1a1d] overflow-hidden">
          <div
            className={`h-full ${getBarColor(data.finalScore)}`}
            style={{ width: `${data.finalScore}%` }}
          />
        </div>
      </div>

    </div>
  );
}

export default ScorePanel;
