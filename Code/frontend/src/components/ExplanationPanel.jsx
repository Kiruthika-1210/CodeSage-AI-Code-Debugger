import React from "react";

function ExplanationPanel({ data }) {
  // Guard: nothing to show
  if (!data) return null;

  // STRING EXPLANATION
  if (typeof data === "string") {
    return (
      <div className="mt-8 p-6 rounded-2xl bg-[#0d0d0f] border border-[#1a1a1d] shadow-xl text-white">
        <h2 className="text-xl font-semibold mb-4 text-[#d4a44d]">
          Refactoring Explanation
        </h2>
        <p className="text-gray-400 leading-relaxed">
          {data}
        </p>
      </div>
    );
  }

  // OBJECT EXPLANATION
  return (
    <div className="mt-8 p-6 rounded-2xl bg-[#0d0d0f] border border-[#1a1a1d] shadow-xl text-white">

      {/* Title */}
      <h2 className="text-xl font-semibold mb-6 text-[#d4a44d]">
        Refactoring Explanation
      </h2>

      {/* Why Refactoring */}
      {data.why?.length > 0 && (
        <section className="mb-6">
          <h3 className="text-lg font-medium mb-2 text-gray-200">
            Why Refactoring Was Done
          </h3>
          <ul className="list-disc list-inside space-y-1 text-gray-400">
            {data.why.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </section>
      )}

      {/* Improvements */}
      {data.improvements?.length > 0 && (
        <section className="mb-6">
          <h3 className="text-lg font-medium mb-2 text-gray-200">
            Improvements Made
          </h3>
          <ul className="list-disc list-inside space-y-1 text-gray-400">
            {data.improvements.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </section>
      )}

      {/* Suggestions */}
      {data.suggestions?.length > 0 && (
        <section className="mb-6">
          <h3 className="text-lg font-medium mb-2 text-gray-200">
            Future Suggestions
          </h3>
          <ul className="list-disc list-inside space-y-1 text-gray-400">
            {data.suggestions.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </section>
      )}

      {/* Test Cases */}
      {data.testCases?.length > 0 && (
        <section>
          <h3 className="text-lg font-medium mb-2 text-gray-200">
            Suggested Test Cases
          </h3>
          <div className="space-y-2">
            {data.testCases.map((test, index) => (
              <div
                key={index}
                className="px-4 py-2 rounded-lg bg-[#101012] border border-[#1f1f22] text-gray-300 font-mono text-sm"
              >
                {test}
              </div>
            ))}
          </div>
        </section>
      )}

    </div>
  );
}

export default ExplanationPanel;
