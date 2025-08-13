## testing for multidoc chat
import sys
from pathlib import Path
from src.multi_document_chat.data_ingestion import DocumentIngestor
from src.multi_document_chat.retrieval import ConversationalRAG

def test_document_ingestion_and_rag():
    print("Inside test_document_ingestion_and_rag ")
    try:
        test_files = [
            r"data\multi_doc_chat\market_analysis_report.docx",
            r"data\multi_doc_chat\NIPS-2017-attention-is-all-you-need-Paper.pdf",
            r"data\multi_doc_chat\sample.pdf",
            r"data\multi_doc_chat\state_of_the_union.txt"
        ]
        uploaded_files =[]
        print("Uploading files")
        for file_path in test_files:
            if Path(file_path).exists():
                # with open(file_path, "rb") as f:
                #     uploaded_files.append(f)
                uploaded_files.append(open(file_path, "rb"))
            else:
                print(f"File does not exist: {file_path}")
                
        print("Uploaded files")
        if not uploaded_files:
            print("No valid files to upload")
            sys.exit(1)
            
        ingestor = DocumentIngestor()
        retiever = ingestor.ingest_files(uploaded_files)
        
        for f in uploaded_files:
            f.close()
        
        session_id = "test_multi_doc_chat"
        rag = ConversationalRAG(retriever=retiever, session_id=session_id)
        #question = "What is attention is all you need paper about?"
        #question = "What did President Zelenskyy said in his speech to the European Parliament?"
        question = "What is President Zelenskyy said in their speech in parliament?"
        
        answer = rag.invoke(question)
        print(f"\nQuestion: {question}\nAnswer: {answer}")
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"Test Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_document_ingestion_and_rag()
        

    