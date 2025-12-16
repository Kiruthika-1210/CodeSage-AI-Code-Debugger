import React, { useState } from "react";
import { getVersionDetails } from "../utils/api";

function VersionHistory({
  versions,
  onSaveVersion,
  onDeleteVersion,
  onClearAll,
  canSave,
}) {
  const [selectedVersion, setSelectedVersion] = useState(null);

  return (
    <div className="mt-8 p-6 rounded-2xl bg-[#0d0d0f] border border-[#1a1a1d] shadow-xl text-white">

      {/* HEADER */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="flex items-center gap-2 text-xl font-semibold text-[#d4a44d]">
          Version History
          <span className="px-2 py-0.5 rounded-full text-xs bg-[#1a1a1d] border border-[#262629] text-gray-300">
            {versions.length}
          </span>
        </h2>

        <div className="flex items-center gap-3">
          <button
            onClick={onClearAll}
            disabled={versions.length === 0}
            className={`px-3 py-1 rounded-lg text-sm font-medium transition
              ${
                versions.length
                  ? "text-red-400 border border-red-400/60 hover:bg-red-400/10"
                  : "text-neutral-500 border border-neutral-700 cursor-not-allowed"
              }`}
          >
             Clear All
          </button>

          <button
            onClick={onSaveVersion}
            disabled={!canSave}
            className={`px-4 py-1 rounded-lg text-sm font-medium transition
              ${
                canSave
                  ? "text-black bg-yellow-500 hover:bg-yellow-400"
                  : "bg-neutral-700 text-neutral-400 cursor-not-allowed"
              }`}
          >
             Save Version
          </button>
        </div>
      </div>

      {/* TIMELINE */}
      {versions.length === 0 ? (
        <p className="text-gray-500 text-sm">No versions saved yet.</p>
      ) : (
        <div className="space-y-4">
          {versions.map((version, index) => (
            <div
              key={version.version_id}
              className="flex justify-between items-center p-4 rounded-xl
                         bg-[#101012] border border-[#1f1f22]"
            >
              <div>
                <p className="font-medium text-gray-200">v{index + 1}</p>
                <p className="text-sm text-gray-500">
                  {new Date(version.created_at).toLocaleString()}
                </p>
              </div>

              <div className="flex items-center gap-3">
                <button
                  onClick={() => onDeleteVersion(version.version_id)}
                  className="text-red-400 hover:text-red-300"
                  title="Delete version"
                >
                  🗑️
                </button>

                <button
                  onClick={async () => {
                    const fullVersion = await getVersionDetails(
                      version.version_id
                    );
                    setSelectedVersion(fullVersion);
                  }}
                  className="px-4 py-1 rounded-lg text-sm font-medium
                             text-[#d4a44d] border border-[#d4a44d]/60
                             hover:bg-black transition"
                >
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* MODAL */}
      {selectedVersion && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
          <div className="w-[90%] max-w-3xl bg-[#0d0d0f]
                          border border-[#1a1a1d]
                          rounded-2xl shadow-2xl
                          max-h-[80vh] flex flex-col">

            {/* Header */}
            <div className="flex justify-between items-center px-6 py-4 border-b border-[#1a1a1d]">
              <h3 className="text-lg font-semibold text-[#d4a44d]">
                Version Details
              </h3>
              <button
                onClick={() => setSelectedVersion(null)}
                className="text-gray-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            {/* Scrollable content */}
            <div className="px-6 py-4 overflow-y-auto">

              {/* Code Snapshot */}
              <div className="mb-4">
                <p className="text-gray-400 mb-1">Code Snapshot</p>
                <pre className="bg-[#101012] border border-[#1f1f22]
                                rounded-lg p-4 text-sm text-gray-300
                                max-h-[220px] overflow-y-auto">
{selectedVersion.refactored_code ??
 selectedVersion.original_code ??
 "—"}
                </pre>
              </div>

              {/* Issues */}
              <div className="mb-4">
                <p className="text-gray-400 mb-1">Issues</p>
                {selectedVersion.issues?.length === 0 ? (
                  <p className="text-green-400 text-sm">No issues</p>
                ) : (
                  <ul className="list-disc list-inside text-sm text-gray-300">
                    {selectedVersion.issues?.map((issue, idx) => (
                      <li key={idx}>
                        {issue.type} — {issue.message}
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              <hr className="my-4 border-[#1f1f22]" />

              {/* Diff */}
              <div>
                <p className="text-gray-400 mb-1">Diff</p>
                <pre className="bg-[#101012] border border-[#1f1f22]
                                rounded-lg p-4 text-sm text-gray-300
                                max-h-[300px] overflow-y-auto">
{selectedVersion.diff || "No changes"}
                </pre>
              </div>

            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default VersionHistory;
