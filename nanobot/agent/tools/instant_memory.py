from __future__ import annotations
from typing import Any
from pathlib import Path
from nanobot.agent.tools.base import BaseTool

class InstantMemoryTool(BaseTool):
    """Instantly updates USER.md or MEMORY.md."""
    
    name = "update_core_memory"
    description = "Use this tool to immediately save important facts, preferences, or rules to MEMORY.md or USER.md. Do not wait for the background consolidation cycle."
    parameters = {
        "type": "object",
        "properties": {
            "target_file": {
                "type": "string",
                "enum": ["MEMORY.md", "USER.md"],
                "description": "Which file to update."
            },
            "content_to_append": {
                "type": "string",
                "description": "The exact text or rule to permanently save."
            }
        },
        "required": ["target_file", "content_to_append"]
    }

    def __init__(self, workspace: Path):
        self.workspace = workspace

    async def execute(self, **kwargs: Any) -> str:
        target = kwargs["target_file"]
        content = kwargs["content_to_append"]
        
        file_path = self.workspace / target if target == "USER.md" else self.workspace / "memory" / target
        
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"\n{content}\n")
            return f"SUCCESS: I have instantly written to {target}. The memory is now permanent."
        except Exception as e:
            return f"FAILED to write to {target}: {str(e)}"