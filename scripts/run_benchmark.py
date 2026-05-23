#!/usr/bin/env python
"""Run performance benchmarks"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import aiohttp
import time
from typing import List, Dict
import statistics

async def benchmark_api(url: str, num_requests: int = 100):
    """Benchmark API performance"""
    
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        
        tasks = []
        for i in range(num_requests):
            task = session.get(url)
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        return {
            'total_requests': num_requests,
            'total_time': total_time,
            'requests_per_second': num_requests / total_time,
            'success_rate': sum(1 for r in responses if r.status == 200) / num_requests * 100
        }

async def main():
    """Run benchmarks"""
    print("Running performance benchmarks...")
    
    # Benchmark health endpoint
    result = await benchmark_api("http://localhost:8000/health", 100)
    print(f"Health endpoint: {result['requests_per_second']:.2f} req/sec")
    
    # Benchmark validation endpoint
    print("Benchmarking validation endpoint...")
    # Add validation benchmark here
    
    print("Benchmark complete!")

if __name__ == "__main__":
    asyncio.run(main())