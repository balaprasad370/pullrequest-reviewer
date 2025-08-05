import json
from app.crew_agent.run import CodeReview


def run_ai_agent(files):
    final_response = {
        "files": [],
        "summary": {
            "total_files": 0,
            "total_issues": 0,
            "critical_issues": 0,
        },
    }

    def update_final_response(response):
        final_response["files"].append(response)
        final_response["summary"]["total_files"] += 1
        final_response["summary"]["total_issues"] += len(response["issues"])
        for issue in response["issues"]:
            if issue["type"] == "bug":
                final_response["summary"]["critical_issues"] += 1

    for file in files:
        try:
            code_review = CodeReview(file)
            results = code_review.run_crew()
            response = json.loads(results.tasks_output[0].raw)
            update_final_response(response)
        except Exception as e:
            print(f"Error analyzing file {file['filename']}: {e}")
            # Add error issue but don't increment total_issues counter
            update_final_response(
                {
                    "name": file["filename"],
                    "issues": [
                        {
                            "type": "error",
                            "line": 0,
                            "description": f"Error analyzing file: {str(e)}",
                            "suggestion": "Check logs for details",
                        }
                    ],
                }
            )

    return final_response
