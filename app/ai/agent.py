# from openai import OpenAI
# import os
# from pydantic import BaseModel
# from typing import List

# client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))

# class Issue(BaseModel):
#     type: str 
#     line: int
#     description: str
#     suggestion: str

#     def dict(self):
#         return {
#             "type": self.type,
#             "line": self.line,
#             "description": self.description,
#             "suggestion": self.suggestion
#         }

# class FileIssues(BaseModel):
#     name: str
#     issues: List[Issue]

#     def dict(self):
#         return {
#             "name": self.name,
#             "issues": [issue.dict() for issue in self.issues]
#         }

# class ReviewSummary(BaseModel):
#     total_files: int
#     total_issues: int 
#     critical_issues: int

#     def dict(self):
#         return {
#             "total_files": self.total_files,
#             "total_issues": self.total_issues,
#             "critical_issues": self.critical_issues
#         }

# class CodeReview(BaseModel):
#     files: List[FileIssues]
#     summary: ReviewSummary

#     def dict(self):
#         return {
#             "files": [file.dict() for file in self.files],
#             "summary": self.summary.dict()
#         }

# def run_ai_agent(files):
#     all_issues = []
#     total_issues = 0
#     critical_issues = 0
    
#     for file in files:
#         try:
#             prompt = f"""You are a senior code reviewer. 
#             Review the following diff and return issues in JSON format with:
#             - type (bug/style/security/performance/other)
#             - line number
#             - description
#             - suggestion for fix
            
#             Return the response in JSON format. 
#             Example:
#             [
#                 {
#                     "type": "bug",
#                     "line": 10,
#                     "description": "This is a bug",
#                     "suggestion": "Fix the bug"
#                 }
#             ]

#             Only add issues that are actually present in the diff. else return empty list. Give the correct review.
#             if No issues are found, return empty list.
#             Diff from {file['filename']}:
#             {file['patch']}"""

#             print("prompt", prompt)
            
#             completion = client.chat.completions.create(
#                 model="gpt-4o-mini",  # Using stable model name
#                 messages=[{"role": "user", "content": prompt}],
#                 # response_format=List[Issue]
#             )
#             print("completion", (completion.choices[0].message.content))

#             file_issues = []
#             if not completion.refusal:
#                 file_issues = completion.parsed
#                 total_issues += len(file_issues)
#                 critical_issues += sum(1 for issue in file_issues 
#                                     if issue.type in ["bug", "security"])
                        
#             all_issues.append(FileIssues(
#                 name=file["filename"],
#                 issues=file_issues
#             ))
            
#         except Exception as e:
#             # Add to total_issues when there's an error
#             total_issues += 1
#             all_issues.append(FileIssues(
#                 name=file["filename"],
#                 issues=[Issue(
#                     type="error",
#                     line=0,
#                     description=f"Error analyzing file: {str(e)}",
#                     suggestion="Check logs for details"
#                 )]
#             ))

#     review = CodeReview(
#         files=all_issues,
#         summary=ReviewSummary(
#             total_files=len(files),
#             total_issues=total_issues,
#             critical_issues=critical_issues
#         )
#     )
#     return review.dict()


from openai import OpenAI
import os
import json
from pydantic import BaseModel
from typing import List

client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))

class Issue(BaseModel):
    type: str 
    line: int
    description: str
    suggestion: str

    def dict(self):
        return {
            "type": self.type,
            "line": self.line,
            "description": self.description,
            "suggestion": self.suggestion
        }

class FileIssues(BaseModel):
    name: str
    issues: List[Issue]

    def dict(self):
        return {
            "name": self.name,
            "issues": [issue.dict() for issue in self.issues]
        }

class ReviewSummary(BaseModel):
    total_files: int
    total_issues: int 
    critical_issues: int

    def dict(self):
        return {
            "total_files": self.total_files,
            "total_issues": self.total_issues,
            "critical_issues": self.critical_issues
        }

class CodeReview(BaseModel):
    files: List[FileIssues]
    summary: ReviewSummary

    def dict(self):
        return {
            "files": [file.dict() for file in self.files],
            "summary": self.summary.dict()
        }

def run_ai_agent(files):
    all_issues = []
    total_issues = 0
    critical_issues = 0
    
    for file in files:
        try:
            prompt = f"""You are a senior code reviewer. 
            Review the following diff and return issues in JSON format with:
            - type (bug/style/security/performance/other)
            - line number
            - description
            - suggestion for fix
            
            Return the response in JSON format. 
            Example:
            [
                {{
                    "type": "bug",
                    "line": 10,
                    "description": "This is a bug",
                    "suggestion": "Fix the bug"
                }}
            ]

            Only add issues that are actually present in the diff. If no issues are found, return empty list [].
            Give the correct review.
            
            Diff from {file['filename']}:
            {file['patch']}"""

            # print("prompt", prompt)
            
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            # print("completion", completion.choices[0].message.content)

            file_issues = []
            if completion.choices[0].message.content:
                try:
                    # Parse the JSON response
                    response_data = json.loads(completion.choices[0].message.content)
                    
                    # Handle different response formats
                    if isinstance(response_data, list):
                        issues_data = response_data
                    elif isinstance(response_data, dict) and 'issues' in response_data:
                        issues_data = response_data['issues']
                    else:
                        issues_data = []
                    
                    # Convert to Issue objects
                    for issue_data in issues_data:
                        if isinstance(issue_data, dict) and all(key in issue_data for key in ['type', 'line', 'description', 'suggestion']):
                            file_issues.append(Issue(**issue_data))

                    total_issues += len(file_issues)
                    critical_issues += sum(1 for issue in file_issues 
                                        if issue.type in ["bug", "security"])
                                        
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error for {file['filename']}: {e}")
                    # Don't add to total_issues for JSON errors, just log it
                    file_issues = []
                        
            if(len(file_issues) > 0):            
                all_issues.append(FileIssues(
                    name=file["filename"],
                    issues=file_issues
                ))
            
        except Exception as e:
            print(f"Error analyzing file {file['filename']}: {e}")
            # Add error issue but don't increment total_issues counter
            all_issues.append(FileIssues(
                name=file["filename"],
                issues=[Issue(
                    type="error",
                    line=0,
                    description=f"Error analyzing file: {str(e)}",
                    suggestion="Check logs for details"
                )]
            ))

    review = CodeReview(
        files=all_issues,
        summary=ReviewSummary(
            total_files=len(files),
            total_issues=total_issues,
            critical_issues=critical_issues
        )
    )
    return review.dict()