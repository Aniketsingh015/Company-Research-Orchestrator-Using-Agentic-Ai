"""
Excel handler for reading and writing company data.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from models.company_schema import CompanyData


class ExcelHandler:
    """Handle Excel file operations for company data."""
    
    @staticmethod
    def load_csv(file_path: Path) -> pd.DataFrame:
        """
        Load CSV file into DataFrame.
        
        Args:
            file_path: Path to CSV file
        
        Returns:
            Pandas DataFrame
        """
        try:
            # Try UTF-8 first
            return pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                # Try with latin-1 encoding for special characters
                return pd.read_csv(file_path, encoding='latin-1')
            except Exception as e2:
                try:
                    # Try with ISO-8859-1
                    return pd.read_csv(file_path, encoding='ISO-8859-1')
                except Exception as e3:
                    print(f"❌ Error loading CSV {file_path}: {str(e3)}")
                    raise
        except pd.errors.EmptyDataError:
            # Handle empty CSV files
            print(f"⚠️  CSV file is empty or has no columns: {file_path}")
            return pd.DataFrame()
        except Exception as e:
            print(f"❌ Error loading CSV {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def save_to_excel(
        data: Dict[str, Any],
        output_path: Path,
        sheet_name: str = "Company Data"
    ):
        """
        Save company data to Excel file.
        
        Args:
            data: Company data dictionary
            output_path: Path to output Excel file
            sheet_name: Name of the Excel sheet
        """
        try:
            # Convert data to DataFrame
            df = pd.DataFrame([data])
            
            # Save to Excel
            df.to_excel(output_path, sheet_name=sheet_name, index=False)
            print(f"✅ Data saved to {output_path}")
        
        except Exception as e:
            print(f"❌ Error saving to Excel: {str(e)}")
            raise
    
    @staticmethod
    def save_multiple_to_excel(
        data_list: List[Dict[str, Any]],
        output_path: Path,
        sheet_name: str = "Company Data"
    ):
        """
        Save multiple company records to Excel.
        
        Args:
            data_list: List of company data dictionaries
            output_path: Path to output Excel file
            sheet_name: Name of the Excel sheet
        """
        try:
            df = pd.DataFrame(data_list)
            df.to_excel(output_path, sheet_name=sheet_name, index=False)
            print(f"✅ {len(data_list)} records saved to {output_path}")
        
        except Exception as e:
            print(f"❌ Error saving multiple records: {str(e)}")
            raise
    
    @staticmethod
    def append_to_excel(
        data: Dict[str, Any],
        output_path: Path,
        sheet_name: str = "Company Data"
    ):
        """
        Append data to existing Excel file.
        
        Args:
            data: Company data dictionary
            output_path: Path to Excel file
            sheet_name: Name of the Excel sheet
        """
        try:
            # Load existing data if file exists
            if output_path.exists():
                existing_df = pd.read_excel(output_path, sheet_name=sheet_name)
                new_df = pd.DataFrame([data])
                df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                df = pd.DataFrame([data])
            
            # Save to Excel
            df.to_excel(output_path, sheet_name=sheet_name, index=False)
            print(f"✅ Data appended to {output_path}")
        
        except Exception as e:
            print(f"❌ Error appending to Excel: {str(e)}")
            raise
    
    @staticmethod
    def create_validation_report_excel(
        company_name: str,
        validation_results: List[Dict[str, Any]],
        output_path: Path
    ):
        """
        Create Excel file with validation report.
        
        Args:
            company_name: Name of the company
            validation_results: List of validation result dictionaries
            output_path: Path to output Excel file
        """
        try:
            # Create DataFrame
            df = pd.DataFrame(validation_results)
            
            # Add company name column
            df.insert(0, "Company", company_name)
            
            # Save to Excel with formatting
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name="Validation Results", index=False)
                
                # Get workbook and worksheet
                worksheet = writer.sheets["Validation Results"]
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            print(f"✅ Validation report saved to {output_path}")
        
        except Exception as e:
            print(f"❌ Error creating validation report: {str(e)}")
            raise
    
    @staticmethod
    def generate_output_filename(company_name: str, suffix: str = "") -> str:
        """
        Generate standardized output filename.
        
        Args:
            company_name: Name of the company
            suffix: Optional suffix to add
        
        Returns:
            Formatted filename
        """
        # Clean company name
        clean_name = "".join(c if c.isalnum() or c in (" ", "_") else "" for c in company_name)
        clean_name = clean_name.replace(" ", "_")
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create filename
        if suffix:
            return f"{clean_name}_{suffix}_{timestamp}.xlsx"
        else:
            return f"{clean_name}_{timestamp}.xlsx"


# Global Excel handler instance
excel_handler = ExcelHandler()