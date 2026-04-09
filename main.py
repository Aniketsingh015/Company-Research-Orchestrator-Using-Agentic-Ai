"""
Main entry point for the Company Research Agent system.
"""

import sys
from pathlib import Path
from typing import Optional
from graph.workflow import company_research_workflow
from config.settings import settings, validate_settings
from utils.logger import main_logger


def print_banner():
    """Print application banner."""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        COMPANY RESEARCH AGENT - Multi-Agent System             ║
║                                                                ║
║  Agent 1: Data Generator (163 Parameters)                     ║
║  Agent 2: Validator (22 Metadata + 65 Test Cases)            ║
║  Agent 3: Supabase Normalizer (Coming Soon)                   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_results(final_state):
    """Print workflow results."""
    print("\n" + "="*70)
    print("WORKFLOW RESULTS")
    print("="*70)
    
    print(f"\n📊 Company: {final_state['company_name']}")
    print(f"📈 Status: {final_state['status']}")
    print(f"🔄 Regeneration Attempts: {final_state['regeneration_count']}")
    print(f"✅ Validation Passed: {'Yes' if final_state['validation_passed'] else 'No'}")
    
    if final_state.get('validation_report'):
        report = final_state['validation_report']
        print(f"\n📋 Validation Report:")
        print(f"   Total Tests: {report.total_tests}")
        print(f"   Passed: {report.passed_tests}")
        print(f"   Failed: {report.failed_tests}")
        print(f"   Overall Status: {report.overall_status}")
    
    if final_state.get('data_file_path'):
        print(f"\n💾 Data File: {final_state['data_file_path']}")
    
    if final_state.get('report_file_path'):
        print(f"📄 Report File: {final_state['report_file_path']}")
    
    if final_state.get('error'):
        print(f"\n❌ Error: {final_state['error']}")
    
    print("\n" + "="*70)


def run_for_company(company_name: str):
    """
    Run the workflow for a single company.
    
    Args:
        company_name: Name of the company to research
    """
    main_logger.info(f"Starting research for company: {company_name}")
    
    try:
        # Run workflow
        final_state = company_research_workflow.run(company_name)
        
        # Print results
        print_results(final_state)
        
        return final_state
    
    except Exception as e:
        main_logger.error(f"Error running workflow: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        raise


def run_batch(company_names: list):
    """
    Run the workflow for multiple companies.
    
    Args:
        company_names: List of company names
    """
    results = []
    
    print(f"\n🚀 Processing {len(company_names)} companies...\n")
    
    for i, company_name in enumerate(company_names, 1):
        print(f"\n{'='*70}")
        print(f"Processing {i}/{len(company_names)}: {company_name}")
        print(f"{'='*70}\n")
        
        try:
            final_state = run_for_company(company_name)
            results.append({
                "company": company_name,
                "status": final_state["status"],
                "success": final_state["validation_passed"]
            })
        except Exception as e:
            main_logger.error(f"Failed to process {company_name}: {str(e)}")
            results.append({
                "company": company_name,
                "status": "failed",
                "success": False
            })
    
    # Print summary
    print("\n" + "="*70)
    print("BATCH PROCESSING SUMMARY")
    print("="*70)
    
    for result in results:
        status_icon = "✅" if result["success"] else "❌"
        print(f"{status_icon} {result['company']}: {result['status']}")
    
    print("="*70 + "\n")


def main():
    """Main entry point."""
    print_banner()
    
    # Validate settings
    try:
        validate_settings()
        print("✅ Configuration validated successfully\n")
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        company_name = " ".join(sys.argv[1:])
        run_for_company(company_name)
    else:
        # Interactive mode
        print("Enter company name (or 'batch' for multiple companies):")
        user_input = input("> ").strip()
        
        if user_input.lower() == 'batch':
            print("\nEnter company names (comma-separated):")
            companies_input = input("> ").strip()
            company_names = [c.strip() for c in companies_input.split(",") if c.strip()]
            
            if company_names:
                run_batch(company_names)
            else:
                print("❌ No company names provided")
        elif user_input:
            run_for_company(user_input)
        else:
            print("❌ No company name provided")


if __name__ == "__main__":
    main()
