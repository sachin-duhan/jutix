import pandas as pd
from pathlib import Path
import glob
from typing import List
import logging
from tqdm import tqdm
import os

class JTLDataLoader:
    def __init__(self, output_dir: Path, logger: logging.Logger):
        self.output_dir = Path(output_dir)
        self.logger = logger

    def load_jtl_files(self, enabled_files: List[str], exclude_files: List[str] = None) -> pd.DataFrame:
        """Load JTL files based on config"""
        all_files = []
        exclude_files = exclude_files or []
        
        self.logger.info("Starting to load JTL files...")
        
        # Log the current directory and search path
        self.logger.debug(f"Current directory: {os.getcwd()}")
        self.logger.debug(f"Looking for files in: {self.output_dir}")
        
        # If specific files are provided, use them directly
        if enabled_files and not any('*' in f for f in enabled_files):
            for file in enabled_files:
                file_path = self.output_dir / file
                if file_path.exists():
                    all_files.append(str(file_path))
                    self.logger.debug(f"Found file: {file_path}")
                else:
                    self.logger.warning(f"File not found: {file_path}")
            self.logger.info(f"Found {len(all_files)} specific files to analyze")
        else:
            for pattern in tqdm(enabled_files, desc="Processing file patterns"):
                glob_pattern = str(self.output_dir / pattern)
                found_files = glob.glob(glob_pattern)
                all_files.extend(found_files)
                self.logger.debug(f"Found {len(found_files)} files matching pattern: {pattern}")
                for f in found_files:
                    self.logger.debug(f"Found file: {f}")
            
        # Remove excluded files
        for exclude in exclude_files:
            all_files = [f for f in all_files if exclude not in f]
            
        dfs = []
        self.logger.info(f"Loading {len(all_files)} JTL files...")
        
        for file in tqdm(all_files, desc="Loading JTL files"):
            try:
                # Read CSV with proper parsing of timestamps
                self.logger.debug(f"Reading file: {file}")
                df = pd.read_csv(file, 
                               parse_dates=['timeStamp'],
                               na_values=['NA'],
                               dtype={
                                   'elapsed': 'float64',
                                   'responseCode': 'str',
                                   'success': 'str',
                                   'bytes': 'float64',
                                   'sentBytes': 'float64',
                                   'Latency': 'float64',
                                   'Connect': 'float64'
                               })
                
                # Convert boolean columns
                df['success'] = df['success'].map({'TRUE': True, 'FALSE': False})
                
                # Add file metadata
                df['file'] = Path(file).name
                
                # Add additional time columns for analysis
                df['second'] = df['timeStamp'].dt.floor('S')
                df['minute'] = df['timeStamp'].dt.floor('T')
                df['hour'] = df['timeStamp'].dt.floor('H')
                
                dfs.append(df)
                self.logger.info(f"Successfully loaded {Path(file).name} with {len(df)} records")
            except Exception as e:
                self.logger.exception(f"Error loading {file}: {e}")
                
        if dfs:
            final_df = pd.concat(dfs, ignore_index=True)
            self.logger.info(f"Total records loaded: {len(final_df)}")
            return final_df
        return pd.DataFrame() 