import React, { useRef } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { python } from "@codemirror/lang-python";
import { indentUnit } from "@codemirror/language";

function CodeEditor({
    code,
    onCodeChange,
    onAnalyze,
    onRefactor,
    onFullPipeline,
    onGenerateTests,
}) {
    const fileInputRef = useRef(null);

    // When user edits code in CodeMirror
    function handleEditorChange(value) {
        onCodeChange(value);   // send to Home.jsx
    }

    // File upload logic (Step 4)
    function handleFileSelected(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            const text = e.target.result;
            onCodeChange(text); // send file text to Home.jsx
        };
        reader.readAsText(file);
    }

    return (
        <div className="p-6 bg-[#0d0d0f] rounded-2xl border border-[#1a1a1d] shadow-xl text-white space-y-6">

            {/* Toolbar */}
            <div className="flex justify-between items-center bg-[#1a1a1d] p-4 rounded-xl border border-[#262629]">
                
                {/* Buttons */}
                <div className="flex gap-4">

                    <button onClick={onAnalyze} className="btn">
                        Analyze
                    </button>

                    <button onClick={onRefactor} className="btn">
                        Refactor
                    </button>

                    <button onClick={onFullPipeline} className="btn">
                        Full Pipeline
                    </button>

                    <button onClick={onGenerateTests} className="btn">
                        Generate Tests
                    </button>

                </div>

                {/* Upload Button */}
                <div>
                    <button
                        onClick={() => fileInputRef.current.click()}
                        className="px-5 py-2 rounded-lg font-medium text-[#d4a44d] border border-[#d4a44d]/60 bg-transparent transition-all duration-300 hover:bg-black hover:text-[#d4a44d] hover:border-[#d4a44d]"
                    >
                        Upload File
                    </button>

                    <input
                        type="file"
                        hidden
                        ref={fileInputRef}
                        onChange={handleFileSelected}
                    />
                </div>
            </div>

            {/* Code Editor */}
            <div className="bg-[#101012] rounded-xl p-4 border border-[#1f1f22]">
                <CodeMirror
                    value={code}
                    height="500px"
                    theme="dark"
                    extensions={[
                        python(),
                        indentUnit.of("    ")
                    ]}
                    onChange={handleEditorChange}
                />
            </div>

        </div>
    );
}

export default CodeEditor;
