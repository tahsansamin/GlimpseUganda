
import time
import json
import os
import redis
from create_cache import create_cache, redis_call
from app_main import run_query_test,run_query

def time_llm_response():
    from app_main import run_query_test
    start_time = time.time()
    value = run_query_test("kampala","Kampala", "What's the best time to visit?",[])
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time, value

def time_redis_response():
    start_time = time.time()
    value = run_query("kampala","Kampala", "What's the best time to visit?",[])
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time, value

# time_taken, value = time_redis_response()
# time_taken_llm, value_llm = time_llm_response()
# print(f"Time taken for Redis response: {time_taken:.6f} seconds")
# print(f"Time taken for LLM response: {time_taken_llm:.6f} seconds")

