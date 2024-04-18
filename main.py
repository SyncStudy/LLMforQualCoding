import openai
import time
import pandas as pd


import os
openai.api_key = ""

journal_name = "Journal of Operations Management"
special_issue_name = "Innovations, Technologies, and the Economics of Last-Mile Operations"


def generate_text(prompt, retries=5, initial_backoff=2):
    messages = [
        {"role": "system", "content": f"You are a top-tier and prestigious researcher who writes for {journal_name} {special_issue_name} special issue"},
        {"role": "user", "content": prompt},
    ]

    backoff = initial_backoff

    for retry in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=messages,
                max_tokens=500,
                n=1,
                temperature=0.7,
            )
            assistant_message = response['choices'][0]['message']['content']
            return assistant_message.strip()

        except openai.error.RateLimitError as e:
            if retry < retries - 1:
                print(f"Rate limit error: {e}. Retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2
            else:
                raise

# Define the research question
research_question = "Design thinking applications to the development of operations in last-mile delivery services that are focused on addressing end recipients’ needs "

# List of file names

# file_names = ['split_1.md','split_2.md','split_3.md','split_4.md','split_5.md','split_6.md','split_7.md','split_8.md','split_9.md']

folder_path = '.'
markdown_files = [file for file in os.listdir(folder_path) if file.startswith('split_') and file.endswith('.md')]
markdown_files.sort()
file_names = markdown_files


print("Read everything")

for file_name in file_names:
    # Read the interview transcript from the markdown file
    with open(file_name, 'r') as file:
        interview_transcript = file.read()
    print("In the loop")

    # Generate the different elements of the analysis
    representative_quotes = generate_text(f'{interview_transcript}\n\nResearch Question: {research_question}\n\nExtract Representative Quotes:')
    print("Quotes done")
    first_order_codes = generate_text(f'Please summarize the first order codes based on the {representative_quotes} with around 4-14 words')
    print("1st done")
    second_order_codes = generate_text(f'Please summarize the second order codes based on the {first_order_codes} with around 2-6 words:')
    print("2nd done")
    third_order_theoretical_dimensions = generate_text(f'Please summarize the third order codes (theoretical dimensions) based on the {second_order_codes} with around 1-4 words')
    print("3rd done")
    print("Generate the different elements of the analysis")

    # Split each category by new lines into lists
    representative_quotes_list = representative_quotes.strip().split('\n')
    first_order_codes_list = first_order_codes.strip().split('\n')
    second_order_codes_list = second_order_codes.strip().split('\n')
    third_order_theoretical_dimensions_list = third_order_theoretical_dimensions.strip().split('\n')
    print("Splited each category by new lines into lists")

    # Determine the length of the longest list
    max_length = max(len(representative_quotes_list), len(first_order_codes_list), len(second_order_codes_list),
                     len(third_order_theoretical_dimensions_list))

    # Pad the shorter lists with None
    representative_quotes_list.extend([None] * (max_length - len(representative_quotes_list)))
    first_order_codes_list.extend([None] * (max_length - len(first_order_codes_list)))
    second_order_codes_list.extend([None] * (max_length - len(second_order_codes_list)))
    third_order_theoretical_dimensions_list.extend([None] * (max_length - len(third_order_theoretical_dimensions_list)))

    # Now you can create the DataFrame
    df = pd.DataFrame(
        {
            "Representative Quotes": representative_quotes_list,
            "First Order Codings": first_order_codes_list,
            "Second Order Codings": second_order_codes_list,
            "Theoretical Dimensions": third_order_theoretical_dimensions_list
        }
    )
    print("Representative Quotes")
    print(representative_quotes_list)
    print("-----------------------------------")

    print("First Order Codings")
    print(first_order_codes_list)
    print("-----------------------------------")

    print("Second Order Codings")
    print(second_order_codes_list)
    print("-----------------------------------")

    print("Theoretical Dimensions")
    print(third_order_theoretical_dimensions_list)
    print("-----------------------------------")

    print("Create a DataFrame")



    # Convert DataFrame to markdown and append to file
    with open('analysis_table_1.md', 'a') as f:
        f.write(df.to_markdown(index=False))
