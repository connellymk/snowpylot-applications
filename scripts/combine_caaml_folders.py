#!/usr/bin/env python3
"""
Script to combine all CAAML files from subfolders in 2004_2025/ and remove duplicates.

This script:
1. Traverses all subdirectories in the snowpits/2004_2025/ folder
2. Finds all .xml CAAML files 
3. Copies them to a combined output directory
4. Removes duplicate files based on filename
5. Provides detailed logging of the process
"""

import os
import shutil

import logging
from pathlib import Path
from collections import defaultdict
import argparse

def setup_logging(log_level='INFO'):
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('combine_caaml_folders.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def find_caaml_files(source_dir):
    """
    Find all CAAML (.xml) files in the source directory and its subdirectories.
    
    Args:
        source_dir (Path): Source directory to search
        
    Returns:
        list: List of Path objects for found CAAML files
    """
    caaml_files = []
    
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.xml') and 'caaml' in file.lower():
                caaml_files.append(Path(root) / file)
    
    return caaml_files

def combine_and_deduplicate_files(source_dir, output_dir, dry_run=False):
    """
    Combine all CAAML files from source directory and remove duplicates based on filename.
    
    Args:
        source_dir (Path): Source directory containing subfolders with CAAML files
        output_dir (Path): Output directory for combined files
        dry_run (bool): If True, only show what would be done without actually copying files
        
    Returns:
        dict: Statistics about the operation
    """
    logger = logging.getLogger(__name__)
    
    # Create output directory if it doesn't exist
    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all CAAML files
    logger.info(f"Searching for CAAML files in {source_dir}")
    caaml_files = find_caaml_files(source_dir)
    logger.info(f"Found {len(caaml_files)} CAAML files")
    
    # Group files by filename to identify duplicates
    files_by_name = defaultdict(list)
    for file_path in caaml_files:
        filename = file_path.name
        files_by_name[filename].append(file_path)
    
    logger.info(f"Found {len(files_by_name)} unique filenames")
    
    # Statistics
    unique_files = 0
    duplicate_files = 0
    copied_files = 0
    errors = 0
    
    # Process files
    logger.info("Processing files and removing duplicates...")
    for filename, file_paths in files_by_name.items():
        if len(file_paths) == 1:
            # Unique file
            unique_files += 1
            source_file = file_paths[0]
        else:
            # Duplicate files - keep the one with the shortest path or lexicographically first
            duplicate_files += len(file_paths) - 1
            unique_files += 1
            source_file = min(file_paths, key=lambda x: (len(str(x)), str(x)))
            
            logger.info(f"Found {len(file_paths)} copies of '{filename}':")
            logger.info(f"  Keeping: {source_file}")
            for dup_file in file_paths:
                if dup_file != source_file:
                    logger.info(f"  Duplicate: {dup_file}")
        
        # Copy the file to output directory
        try:
            output_file = output_dir / filename
            
            if dry_run:
                logger.info(f"Would copy: {source_file} -> {output_file}")
            else:
                shutil.copy2(source_file, output_file)
                logger.debug(f"Copied: {source_file} -> {output_file}")
            
            copied_files += 1
            
        except Exception as e:
            logger.error(f"Error copying {source_file}: {e}")
            errors += 1
    
    # Return statistics
    stats = {
        'total_files_found': len(caaml_files),
        'unique_files': unique_files,
        'duplicate_files': duplicate_files,
        'copied_files': copied_files,
        'errors': errors
    }
    
    return stats

def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description='Combine CAAML files and remove duplicates')
    parser.add_argument('--source', '-s', type=str, 
                       default='../snowpits/2004_2025',
                       help='Source directory containing CAAML files (default: ../snowpits/2004_2025)')
    parser.add_argument('--output', '-o', type=str,
                       default='../snowpits/combined_caaml_files',
                       help='Output directory for combined files (default: ../snowpits/combined_caaml_files)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                       help='Show what would be done without actually copying files')
    parser.add_argument('--log-level', '-l', type=str, default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level (default: INFO)')
    
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_logging(args.log_level)
    
    # Convert paths to Path objects and make them absolute
    script_dir = Path(__file__).parent
    source_dir = Path(args.source)
    if not source_dir.is_absolute():
        source_dir = script_dir / source_dir
    source_dir = source_dir.resolve()
    
    output_dir = Path(args.output)
    if not output_dir.is_absolute():
        output_dir = script_dir / output_dir
    output_dir = output_dir.resolve()
    
    logger.info("Starting CAAML file combination process")
    logger.info(f"Source directory: {source_dir}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Dry run: {args.dry_run}")
    
    if args.dry_run:
        logger.info("DRY RUN MODE - No files will be copied")
    
    try:
        # Run the combination process
        stats = combine_and_deduplicate_files(source_dir, output_dir, args.dry_run)
        
        # Print summary
        logger.info("="*50)
        logger.info("SUMMARY")
        logger.info("="*50)
        logger.info(f"Total files found: {stats['total_files_found']}")
        logger.info(f"Unique files: {stats['unique_files']}")
        logger.info(f"Duplicate files removed: {stats['duplicate_files']}")
        logger.info(f"Files copied: {stats['copied_files']}")
        logger.info(f"Errors: {stats['errors']}")
        
        if not args.dry_run:
            logger.info(f"Combined files saved to: {output_dir}")
        
        logger.info("Process completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during processing: {e}")
        raise

if __name__ == "__main__":
    main()
