
# import os
# from pathlib import Path
# from io import BytesIO
# from src.document_analyzer.data_ingestion import DocumentHandler
# from src.document_analyzer.data_analysis import DocumentAnalyzer

    
# pdf_path=r"C:\\Users\\giris\document_portal\\data\\document_analysis\\sample.pdf"

# class DummyFile:
#     def __init__(self,file_path):
#         self.name = Path(file_path).name
#         self._file_path = file_path
#     def getbuffer(self):
#         return open(self._file_path, "rb").read()
    

# def main():
#     try:
#         # ---------- STEP 1: DATA INGESTION ----------
#         print("Starting PDF ingestion...")
#         dummy_pdf = DummyFile(pdf_path)
        
#         handler = DocumentHandler(session_id="test_ingestion_analysis")
#         saved_path = handler.save_pdf(dummy_pdf)
#         print(f"PDF saved at: {saved_path}")
        
#         text_content = handler.read_pdf(saved_path)
#         print(f"Extracted text length: {len(text_content)} chars\n")
        
        
#         # ---------- STEP 2: DATA ANALYSIS ----------
#         print("Starting document analysis...")
#         analyzer = DocumentAnalyzer()
#         analysis_result = analyzer.analyze_document(text_content)
        
#         # ---------- STEP 3: DISPLAY RESULTS ----------
#         print("\n=== METADATA ANALYSIS RESULT ===")
#         for key, value in analysis_result.items():
#             print(f"{key}: {value}")

#     except Exception as e:
#         print(f"Test Failed: {e}")
        
# if __name__ == "__main__":
#     main()
        

import io
from pathlib import Path
from src.document_compare.data_ingestion import DocumentIngestion
from src.document_compare.document_comparator import DocumentComparatorLLM

# ---- Setup: Load local PDF files as if they were "uploaded" ---- #
def load_fake_uploaded_file(file_path: Path):
    return io.BytesIO(file_path.read_bytes())

# ---- Step 1: Save and combine PDFs ---- #
def test_compare_documents():
    ref_path = Path("C:\\Users\\giris\\document_portal\\data\\document_compare\\Long_Report_V1.pdf")
    act_path = Path("C:\\Users\\giris\\document_portal\\data\\document_compare\\Long_Report_V2.pdf")
    
    # Wrap them like Streamlit UploadedFile-style    
    class FakeUpload:
        def __init__(self,file_path:Path):
            self.name = file_path.name
            self._buffer = file_path.read_bytes()
            
        def getbuffer(self):
            return self._buffer
        
    comparator = DocumentIngestion()
    ref_upload = FakeUpload(ref_path)
    act_upload = FakeUpload(act_path)
    
    ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)
    combined_text = comparator.combine_documents()
    comparator.clean_old_sessions(keep_latest=3)
    
    print("\n Combined Text Preview (First 1000 chars):\n")
    print(combined_text[:1000])
    
    llm_comparator = DocumentComparatorLLM()
    comparision_df = llm_comparator.compare_documents(combined_text)
    
    print("\n=== COMPARISION RESULT ===")
    print(comparision_df.head())
    
if __name__ == "__main__":
    test_compare_documents()
    print("\nTest completed successfully!")
    
        

