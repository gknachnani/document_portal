import os
from pathlib import Path
from io import BytesIO
from archive.src.document_analyzer.data_ingestion import DocumentHandler
from archive.src.document_analyzer.data_analysis import DocumentAnalyzer

    
pdf_path=r"C:\\Users\\giris\document_portal\\data\\document_analysis\\sample.pdf"

class DummyFile:
    def __init__(self,file_path):
        self.name = Path(file_path).name
        self._file_path = file_path
    def getbuffer(self):
        return open(self._file_path, "rb").read()
    

def main():
    try:
        # ---------- STEP 1: DATA INGESTION ----------
        print("Starting PDF ingestion...")
        dummy_pdf = DummyFile(pdf_path)
        
        handler = DocumentHandler(session_id="test_ingestion_analysis")
        saved_path = handler.save_pdf(dummy_pdf)
        print(f"PDF saved at: {saved_path}")
        
        text_content = handler.read_pdf(saved_path)
        print(f"Extracted text length: {len(text_content)} chars\n")
        
        
        # ---------- STEP 2: DATA ANALYSIS ----------
        print("Starting document analysis...")
        analyzer = DocumentAnalyzer()
        analysis_result = analyzer.analyze_document(text_content)
        
        # ---------- STEP 3: DISPLAY RESULTS ----------
        print("\n=== METADATA ANALYSIS RESULT ===")
        for key, value in analysis_result.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Test Failed: {e}")
        
if __name__ == "__main__":
    main()