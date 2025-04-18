import os
import json
from pathlib import Path
from mistralai import Mistral
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator, ValidationError
import re

# Load API key
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("❌ API Key not found in .env file!")

client = Mistral(api_key=api_key)

class PatientInfo(BaseModel):
    name: str
    sex: str
    age: int
    summary: str

    @field_validator('age', mode='before')
    def validate_age(cls, value):
        if isinstance(value, str):
            match = re.search(r'\d+', value)
            if match:
                return int(match.group())
        return value

def process_pdf_and_generate_summary(pdf_path):
    pdf_file = Path(pdf_path)
    assert pdf_file.is_file(), f"{pdf_path} does not exist!"

    uploaded_file = client.files.upload(
        file={
            "file_name": pdf_file.stem,
            "content": pdf_file.read_bytes(),
        },
        purpose="ocr",
    )

    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

    pdf_response = client.ocr.process(
        document={"document_url": signed_url.url},
        model="mistral-ocr-latest",
        include_image_base64=False
    )

    response_dict = json.loads(pdf_response.model_dump_json())

    markdown_blocks = []
    if 'pages' in response_dict:
        for page in response_dict['pages']:
            if 'markdown' in page and page['markdown'].strip():
                markdown_blocks.append(page['markdown'].strip())

    md_output_path = pdf_file.with_suffix('.md')
    with open(md_output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Summary of {pdf_file.name}\n\n")
        if markdown_blocks:
            f.write("\n\n---\n\n".join(markdown_blocks))
        else:
            f.write("❌ No markdown content extracted from the PDF.")
    print(f"✅ Markdown summary saved to: {md_output_path}")

    full_markdown = "\n".join(markdown_blocks)
    prompt = generate_prompt_from_markdown(full_markdown)

    response = client.chat.complete(
        model="mistral-medium",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    try:
        patient_data = extract_patient_info(response.choices[0].message.content)
        structured_output = PatientInfo(**patient_data)
    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        return

    structured_output_path = pdf_file.with_name(pdf_file.stem + '_structured.json')
    with open(structured_output_path, 'w', encoding='utf-8') as f:
        json.dump(structured_output.model_dump(), f, indent=4, ensure_ascii=False)
    print(f"✅ Structured JSON saved to: {structured_output_path}")

def generate_prompt_from_markdown(markdown_text):
    return f"Extract the patient's name, sex, age, and medical summary from the following text:\n\n{markdown_text}"

def extract_patient_info(markdown_summary):
    lines = markdown_summary.strip().split("\n")
    patient_info = {
        "name": lines[0].strip() if len(lines) > 0 else "Unknown",
        "sex": lines[1].strip() if len(lines) > 1 else "Unknown",
        "age": lines[2].strip() if len(lines) > 2 else "0",
        "summary": "\n".join(lines[3:]).strip() if len(lines) > 3 else ""
    }
    return patient_info

if __name__ == "__main__":
    process_pdf_and_generate_summary("pet_ct_2.pdf")
