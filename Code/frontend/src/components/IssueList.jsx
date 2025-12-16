function IssueList({ issues, activeFilter, setActiveFilter, onIssueClick }) {

  const ISSUE_CATEGORY_MAP = {
    "missing-docstring": "documentation",
    "bad-naming": "error",
    "naming-convention": "error",
    "unused-variable": "warning",
    "unused-import": "warning",
    "duplicate-logic": "warning",
    "dead-code": "warning",
    "long-function": "warning",
    "deep-nesting": "error",
  };

  const getCategory = (issue) =>
    ISSUE_CATEGORY_MAP[issue.type] ?? "warning";


  const filteredIssues = issues.filter((issue) => {
    if (activeFilter === "all") return true;
    return getCategory(issue) === activeFilter;
  });

  const categoryColors = {
    error: "text-red-400 border-red-400/40",
    warning: "text-yellow-400 border-yellow-400/40",
    documentation: "text-blue-400 border-blue-400/40",
  };

  return (
    <div className="mt-8 p-6 rounded-2xl bg-[#0d0d0f] border border-[#1a1a1d] shadow-xl text-white">

      <h2 className="text-xl font-semibold mb-4 text-[#d4a44d]">Issues</h2>

      <div className="flex gap-3 mb-6">
        {["all", "error", "warning", "documentation"].map((filter) => (
          <button
            key={filter}
            onClick={() => setActiveFilter(filter)}
            className={`px-3 py-1 rounded-md text-sm capitalize transition 
              ${
                activeFilter === filter
                  ? "bg-[#d4a44d] text-black shadow-md"
                  : "bg-transparent border border-[#444] text-gray-300 hover:bg-black hover:text-[#d4a44d]"
              }`}
          >
            {filter}
          </button>
        ))}
      </div>

      <div className="space-y-3">
        {filteredIssues.map((issue, index) => {
          const category = getCategory(issue);

          return (
            <div
              key={index}
              onClick={() => onIssueClick(issue.line)}
              className="p-4 rounded-xl bg-[#1a1a1d] border border-[#262629] cursor-pointer hover:border-[#d4a44d]/60 transition"
            >
              <div className="flex justify-between items-center mb-1">
                <span className="font-medium">{issue.type}</span>

                <span className={`px-2 py-0.5 rounded-md text-xs border ${categoryColors[category]}`}>
                  {category}
                </span>
              </div>

              <p className="text-sm text-gray-400">Line {issue.line}</p>
              <p className="text-gray-300 text-sm mt-1">{issue.message}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default IssueList
