# AI_Innovation_Hub\storage_vault\vault_service.py

from PyPDF2 import PdfReader
import boto3
import io
from ..logger import create_logger
from botocore.exceptions import ClientError
from ..text_manager.text_refiner_engine import TextRefiner

logger = create_logger(__name__)

class AmazonS3Service:
    """Service class to interact with Amazon S3 for file operations."""

    def __init__(self) -> None:
        self.s3_client = boto3.client("s3")

    def list_files(self, bucket_name: str, prefix_path: str = "") -> list:
        """List all files in the specified S3 bucket."""
        try:
            logger.info(f"Fetching files from bucket '{bucket_name}' with prefix '{prefix_path}'")
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix_path)
            return [obj['Key'] for obj in response.get('Contents', [])] or []
        except Exception as error:
            logger.exception("Error listing files in S3 bucket")
            return []

    def extract_text_from_pdf(self, bucket_name: str, file_key: str, preprocess: bool = False) -> str:
        """Extract text from a PDF file stored in S3."""
        try:
            s3_object = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
            pdf_stream = io.BytesIO(s3_object['Body'].read())
            reader = PdfReader(pdf_stream)

            text_content = ""
            for page in reader.pages:
                page_text = page.extract_text() or ""
                if preprocess:
                    page_text = TextRefiner.refine_text(page_text)
                text_content += page_text

            logger.info(f"Extracted text from PDF '{file_key}' in bucket '{bucket_name}'")
            return text_content
        except Exception as error:
            logger.exception("Error reading PDF from S3")
            return ""

    def transfer_file(self, source_bucket: str, dest_bucket: str, file_key: str) -> None:
        """Transfer a file from one S3 bucket to another."""
        try:
            self._ensure_bucket_exists(dest_bucket)
            copy_source = {'Bucket': source_bucket, 'Key': file_key}
            self.s3_client.copy(copy_source, dest_bucket, file_key)

            self.s3_client.delete_object(Bucket=source_bucket, Key=file_key)
            logger.info(f"Successfully transferred file '{file_key}' from '{source_bucket}' to '{dest_bucket}'")
        except Exception as error:
            logger.error(f"Failed to transfer file from '{source_bucket}' to '{dest_bucket}'")
            logger.exception(error)

    def _ensure_bucket_exists(self, bucket_name: str, region: str = "eu-west-2") -> None:
        """Ensure that the specified S3 bucket exists, creating it if necessary."""
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            logger.info(f"Bucket '{bucket_name}' already exists.")
        except ClientError:
            logger.info(f"Bucket '{bucket_name}' does not exist. Creating bucket...")
            try:
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
                logger.info(f"Bucket '{bucket_name}' successfully created.")
            except Exception as error:
                logger.error(f"Failed to create bucket '{bucket_name}': {error}")