"""
Test minimal processor performance with live QuickNode data.
"""

import os
import sys
import asyncio
import time
import logging
import json
from datetime import datetime
from typing import List, Dict, Any

# Configure logging to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Import local modules directly
import importlib.util
import pathlib

def import_from_path(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Import required modules
base_path = pathlib.Path(__file__).parent
minimal_processor = import_from_path(
    "minimal_swap_processor",
    str(base_path / "Data Processing Layer" / "vector_processing" / "minimal_swap_processor.py")
)
memory_store = import_from_path(
    "memory_vector_store",
    str(base_path / "Data Processing Layer" / "database" / "memory_vector_store.py")
)
live_proc = import_from_path(
    "live_processor",
    str(base_path / "Data Processing Layer" / "live_processor.py")
)

MinimalSwapProcessor = minimal_processor.MinimalSwapProcessor
MemoryVectorStore = memory_store.MemoryVectorStore
LiveProcessor = live_proc.LiveProcessor

class ProcessingTest:
    """Test harness for minimal processor with live data"""
    
    def __init__(self):
        self.processor = LiveProcessor(max_workers=4)
        self.trade_buffer: List[Dict[str, Any]] = []
        self.processing_times: List[float] = []
        
    async def process_buffer(self):
        """Process buffered trades and measure time"""
        if not self.trade_buffer:
            return
            
        try:
            # Measure processing time
            start_time = time.time()
            
            # Process trades
            vector_ids = self.processor.process_swaps(self.trade_buffer)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            self.processing_times.append(processing_time)
            
            # Log results
            logger.info(f"\nProcessing Results:")
            logger.info(f"Trades processed: {len(self.trade_buffer)}")
            logger.info(f"Processing time: {processing_time:.3f} seconds")
            logger.info(f"Average time: {sum(self.processing_times)/len(self.processing_times):.3f} seconds")
            logger.info(f"Vector IDs: {vector_ids}")
            logger.info("-" * 80)
            
            # Clear buffer
            self.trade_buffer = []
            
        except Exception as e:
            logger.error(f"Error processing buffer: {str(e)}")
            self.trade_buffer = []

async def run_test():
    """Run test with sample data"""
    test = ProcessingTest()
    
    # Sample trade data
    sample_trades = []
    for i in range(50):  # Generate 50 sample trades
        trade = {
            "swap_data": {
                "timestamp": int(time.time()) + i,
                "signature": f"test_sig_{i}",
                "type": "swap",
                "program_id": "program1",
                "slot": 12345 + i,
                "success": True,
                "instructions": ["instruction1", "instruction2"],
                "inner_instructions": ["inner1"],
                "program_ids": ["program1", "program2"]
            },
            "token_balances": {
                "token_in": {"decimals": 9},
                "token_out": {"decimals": 6},
                "pre_token_balance_in": 5000000000 + i * 1000000,
                "post_token_balance_in": 4000000000 + i * 1000000,
                "pre_token_balance_out": 10000000 + i * 1000,
                "post_token_balance_out": 12000000 + i * 1000
            }
        }
        sample_trades.append(trade)
    
    # Process in batches of 10
    for i in range(0, len(sample_trades), 10):
        batch = sample_trades[i:i+10]
        test.trade_buffer = batch
        await test.process_buffer()
        await asyncio.sleep(0.1)  # Small delay between batches

if __name__ == "__main__":
    try:
        asyncio.run(run_test())
    except KeyboardInterrupt:
        pass
