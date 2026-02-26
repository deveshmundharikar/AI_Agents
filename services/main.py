#!/usr/bin/env python3
"""
Core Service Entry Point
"""

import os
import sys
from pathlib import Path

# Add the services directory to Python path
services_path = Path(__file__).parent
sys.path.insert(0, str(services_path))

from core.logger import get_logger
from core.config import settings
from core.langsmith import setup_langsmith
from core.llm import get_llm

def main():
    """Main entry point for core service"""
    
    # Setup logging
    logger = get_logger("core_service")
    logger.info("Starting Core Service...")
    
    # Setup LangSmith tracing
    try:
        setup_langsmith()
        logger.info("LangSmith tracing configured")
    except Exception as e:
        logger.error(f"Failed to setup LangSmith: {e}")
    
    # Test LLM connection
    try:
        llm = get_llm()
        logger.info(f"LLM initialized with model: {settings.MODEL_NAME}")
        
        # Test the LLM with a simple message
        response = llm.invoke("Hello, this is a test message.")
        logger.info("LLM test successful")
        logger.debug(f"Test response: {response}")
        
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        return 1
    
    logger.info("Core Service initialized successfully!")
    
    # Keep service running (you can add your actual service logic here)
    try:
        logger.info("Core Service is running. Press Ctrl+C to stop.")
        # Add your service logic here
        
    except KeyboardInterrupt:
        logger.info("Core Service stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Core Service error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
