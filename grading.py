import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]  

def evaluate_answer(student_answer, grading_rubric, ground_truth_answer):
    prompt = f"""
    You are an intelligent grading assistant tasked with evaluating a student's answer based on the provided grading rubric and ground truth answer (if available). Follow these steps to provide a comprehensive evaluation:

    Step 1: Carefully read and understand the student's answer, paying attention to key points, reasoning, and evidence provided.

    Step 2: Analyze the grading rubric to identify the criteria and expectations for a high-quality answer. Consider the weightage of each criterion mentioned in the rubric.

    Step 3: If a ground truth answer is provided, compare the student's answer with the ground truth answer to assess the level of understanding, accuracy, and completeness.

    Step 4: Evaluate the student's answer against each criterion in the grading rubric. Assign scores for each criterion based on how well the student's answer meets the expectations outlined in the rubric.

    Step 5: Provide a detailed explanation for each assigned score, highlighting the strengths and weaknesses of the student's answer. Offer specific examples and evidence from the student's answer to support your evaluation.

    Step 6: Identify areas where the student lost marks and provide constructive feedback on how they can improve their answer. Give clear and actionable suggestions for each area of improvement.

    Step 7: Calculate the total score out of 100 based on the individual scores assigned for each criterion in the grading rubric. Ensure that the total score reflects the overall quality and completeness of the student's answer.

    Step 8: Summarize your evaluation by providing an overall assessment of the student's answer, highlighting the main strengths, areas for improvement, and the final score.

    Please provide the final score in the first line of your response, followed by the detailed report/answer review.

    Student's Answer:
    {student_answer}

    Grading Rubric:
    {grading_rubric}

    Ground Truth Answer (optional):
    {ground_truth_answer}

    Provide your evaluation below, following the steps outlined above. Ensure that your feedback is clear, specific, and actionable, enabling the student to understand their performance and identify areas for improvement.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an intelligent grading assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message['content'].strip()

def main():
    st.title("Intelligent Grading Assistant")

    col1, col2, col3 = st.columns(3)

    with col1:
        student_answer = st.text_area("Student's Answer", height=300)

    with col2:
        grading_rubric = st.text_area("Grading Rubric", height=300)

    with col3:
        ground_truth_answer = st.text_area("Ground Truth Answer (optional)", height=300)

    if st.button("Evaluate"):
        if student_answer and grading_rubric:
            evaluation_result = evaluate_answer(student_answer, grading_rubric, ground_truth_answer)
            final_score = evaluation_result.split('\n', 1)[0]
            report = evaluation_result.split('\n', 1)[1]

            st.markdown("## Evaluation Result")
            st.markdown(f"**Final Score: {final_score}**")
            st.write(report)
        else:
            st.warning("Please provide the student's answer and grading rubric.")

if __name__ == "__main__":
    main()