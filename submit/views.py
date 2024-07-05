import subprocess
from django.conf import settings
from django.shortcuts import render, redirect
from submit.forms import CodeSubmissionForm
from submit.models import CodeSubmission
from problems.models import Problem, TestCase, Solution
from pathlib import Path
import uuid


def submit(request):
    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.save()

            # Evaluate submission against test cases
            solution = evaluate_submission(submission)

            # Render result based on evaluation
            if solution.verdict == "Accepted":
                return render(request, "result.html", {"submission": submission, "solution": solution})
            else:
                return render(request, "result.html", {"submission": submission, "solution": solution, "error_message": "Wrong Answer"})

    else:
        form = CodeSubmissionForm()

    return render(request, "index.html", {"form": form})

# utils.py or wherever your evaluation logic resides


def evaluate_submission(submission):
    print(f"Evaluating submission: {submission}")

    # Initialize a Solution instance for storing results
    solution = Solution(problem=submission.problem, verdict="Pending")

    if not submission.input_data:
        # No input data provided, use test cases from the database
        test_cases = TestCase.objects.filter(problem=submission.problem)
        results = []

        print(f"Number of test cases: {test_cases.count()}")

        for test_case in test_cases:
            output = run_code(submission.language, submission.code, test_case.input)
            expected_output = test_case.output.strip()
            actual_output = output.strip()

            result = {
                "test_case": test_case,
                "expected_output": expected_output,
                "actual_output": actual_output,
                "verdict": "Accepted" if expected_output == actual_output else "Wrong Answer",
            }
            results.append(result)

        print(f"Results: {results}")

        # Determine overall verdict based on individual test case results
        all_passed = all(result["verdict"] == "Accepted" for result in results)
        solution.verdict = "Accepted" if all_passed else "Wrong Answer"
        solution.results = results

        print(f"Final solution: {solution}")

    else:
        # Input data provided, evaluate against the provided input data
        output = run_code(submission.language, submission.code, submission.input_data)
        expected_output = output.strip()
        actual_output = output.strip()
        results = []
        result = {
                "test_case": submission.input_data,
                "expected_output": expected_output,
                "actual_output": actual_output,
                "verdict": "Accepted" if expected_output == actual_output else "Wrong Answer",
            }
        results.append(result)

        if expected_output == actual_output:
            solution.verdict = "RanCode"
        

        solution.results = [{
            "expected_output": expected_output,
            "actual_output": actual_output,
            "verdict": solution.verdict,
        }]

        print(f"Final solution: {solution}")
    
    solution.save()

    return solution




def run_code(language, code, input_data):
    """
    Simulate running the code (placeholder for actual implementation).
    Replace this with your actual code execution logic.
    """
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
    codes_dir=project_path/"codes"
    inputs_dir=project_path/"inputs"
    outputs_dir=project_path/"outputs"


    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = project_path / "codes" / code_file_name
    input_file_path = project_path / "inputs" / input_file_name
    output_file_path = project_path / "outputs" / output_file_name

    try:
        # Write code to the code file
        with open(code_file_path, "w") as code_file:
            code_file.write(code)

        # Write input data to the input file
        with open(input_file_path, "w") as input_file:
            input_file.write(input_data)

        # Clear output file initially
        with open(output_file_path, "w") as output_file:
            pass

        # Simulate execution or compilation of code
        if language == "cpp":
            executable_path = codes_dir/ unique
            compile_result = subprocess.run(
                ["g++", str(code_file_path), "-o", str(executable_path)],
                stderr=subprocess.PIPE,  # Capture stderr for compilation errors
                stdout=subprocess.PIPE,  # Capture stdout for compilation success (if needed)
            )
            if compile_result.returncode == 0:
                try:
                    # Run the executable with input and capture output
                    with open(input_file_path, "r") as input_file:
                        with open(output_file_path, "w") as output_file:
                            subprocess.run(
                                [str(executable_path)],
                                stdin=input_file,
                                stdout=output_file,
                                stderr=subprocess.PIPE,  # Capture stderr for runtime errors
                            )
                except Exception as e:
                    # Handle runtime errors during code execution
                    print(f"Runtime Error: {str(e)}")
                    return str(e)  # Return the error message
        
            else:
                # Handle compilation error
                error_message = compile_result.stderr.decode("utf-8")
                print(f"Compilation Error: {error_message}")
                return error_message  # Return the error message
            
        if language == "c":
            executable_path = codes_dir/ unique
            compile_result = subprocess.run(
                ["gcc", str(code_file_path), "-o", str(executable_path)],
                stderr=subprocess.PIPE,  # Capture stderr for compilation errors
                stdout=subprocess.PIPE,  # Capture stdout for compilation success (if needed)
            )
            if compile_result.returncode == 0:
                try:
                    # Run the executable with input and capture output
                    with open(input_file_path, "r") as input_file:
                        with open(output_file_path, "w") as output_file:
                            subprocess.run(
                                [str(executable_path)],
                                stdin=input_file,
                                stdout=output_file,
                                stderr=subprocess.PIPE,  # Capture stderr for runtime errors
                            )
                except Exception as e:
                    # Handle runtime errors during code execution
                    print(f"Runtime Error: {str(e)}")
                    return str(e)  # Return the error message
        
            else:
                # Handle compilation error
                error_message = compile_result.stderr.decode("utf-8")
                print(f"Compilation Error: {error_message}")
                return error_message  # Return the error message    

        elif language=="py":
            with open(input_file_path,"r") as input_file:
                with open(output_file_path,"w") as output_file:
                    subprocess.run(
                        ["python3",str(code_file_path)],
                        stdin=input_file,
                        stdout=output_file,
                    )

        # Read output from output file (simulated)
        with open(output_file_path, "r") as output_file:
            output_data = output_file.read()
    
    except Exception as e:
        # Handle any other unexpected exceptions
        print(f"Error during code execution: {str(e)}")
        return str(e)  # Return the error message

    return output_data
