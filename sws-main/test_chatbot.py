#!/usr/bin/env python3
"""
Test script to verify chatbot works with all knowledge base questions
"""
import os
from dotenv import load_dotenv
from knowledge_base import KNOWLEDGE_BASE, get_answer

# Load environment variables
load_dotenv()

def test_knowledge_base():
    """Test all questions in knowledge base"""
    print("=" * 80)
    print("TESTING KNOWLEDGE BASE - ALL QUESTIONS")
    print("=" * 80)
    
    total_questions = 0
    successful_answers = 0
    
    # Group by category
    categories = {}
    for key, data in KNOWLEDGE_BASE.items():
        question = data["question"]
        answer = data["answer"]
        source = data["source"]
        
        # Extract category from source
        category = source.split("-")[1] if "-" in source else "Other"
        if category not in categories:
            categories[category] = []
        categories[category].append((key, question, answer, source))
    
    # Test each category
    for category, items in sorted(categories.items()):
        print(f"\n{'='*80}")
        print(f"CATEGORY: {category.upper()}")
        print(f"{'='*80}")
        
        for key, question, answer, source in items:
            total_questions += 1
            
            # Get answer from knowledge base
            result = get_answer(question)
            
            # Check if answer was found
            if result["answer"] != "I don't have that information in the knowledge base.":
                successful_answers += 1
                status = "✓ PASS"
            else:
                status = "✗ FAIL"
            
            print(f"\n{status} | Q{total_questions}: {question}")
            print(f"   Source: {result['source']}")
            print(f"   Answer: {result['answer'][:150]}...")
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total Questions: {total_questions}")
    print(f"Successful Answers: {successful_answers}")
    print(f"Success Rate: {(successful_answers/total_questions)*100:.1f}%")
    print(f"{'='*80}\n")
    
    return successful_answers == total_questions

if __name__ == "__main__":
    success = test_knowledge_base()
    exit(0 if success else 1)
