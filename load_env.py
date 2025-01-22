"""
Environment loader for the Crypto Trade System.
Configures Python paths and system settings.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def setup_environment():
    """Setup environment variables and Python paths"""
    # Load .env file
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)

    # Add project root to Python path
    root_dir = Path(__file__).parent
    if str(root_dir) not in sys.path:
        sys.path.append(str(root_dir))

    # Add component paths
    data_collection_path = root_dir / 'Data Collection Layer'
    data_processing_path = root_dir / 'Data Processing Layer'

    if str(data_collection_path) not in sys.path:
        sys.path.append(str(data_collection_path))
    if str(data_processing_path) not in sys.path:
        sys.path.append(str(data_processing_path))

    # Verify component status
    quicknode_status = os.getenv('QUICKNODE_STATUS', 'ACTIVE')
    helius_status = os.getenv('HELIUS_STATUS', 'ACTIVE')
    
    if quicknode_status == 'READ_ONLY':
        print("QuickNode component is in READ_ONLY mode")
    if helius_status == 'READ_ONLY':
        print("Helius component is in READ_ONLY mode")

    # Configure performance settings
    os.environ['MAX_WORKERS'] = os.getenv('MAX_WORKERS', '4')
    os.environ['BATCH_SIZE'] = os.getenv('BATCH_SIZE', '50')
    os.environ['VECTOR_CACHE_SIZE'] = os.getenv('VECTOR_CACHE_SIZE', '1000')
    os.environ['MEMORY_LIMIT'] = os.getenv('MEMORY_LIMIT', '2GB')

    # Setup logging
    import logging
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    return {
        'root_dir': root_dir,
        'data_collection_path': data_collection_path,
        'data_processing_path': data_processing_path,
        'quicknode_status': quicknode_status,
        'helius_status': helius_status,
        'max_workers': int(os.getenv('MAX_WORKERS', 4)),
        'batch_size': int(os.getenv('BATCH_SIZE', 50))
    }

if __name__ == '__main__':
    env = setup_environment()
    print("\nEnvironment Configuration:")
    print("-" * 50)
    for key, value in env.items():
        print(f"{key}: {value}")
    print("-" * 50)
