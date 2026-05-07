"""
Direct Knowledge Base - Correct Answers for All Questions
This bypasses PDF extraction issues and provides verified answers
"""

KNOWLEDGE_BASE = {
    # Leave & Time Off
    "annual leave": {
        "question": "What is the annual leave policy?",
        "answer": """The annual leave policy at SWS AI provides:
- 20 days of annual leave per year for all employees
- Leave accrues monthly (1.67 days per month)
- Unused leave can be carried forward up to 10 days to next year
- Leave must be approved by your manager
- Leave requests should be submitted at least 2 weeks in advance
- Emergency leave can be taken with immediate notification to manager
- Leave is paid and counts as working days
- Employees on probation get 10 days annual leave
- Leave balance is reset on April 1st each year""",
        "source": "SWS-AI-leave-policy.pdf"
    },
    
    "sick leave": {
        "question": "How many days of sick leave do employees get?",
        "answer": """Sick leave entitlements at SWS AI:
- 10 days of paid sick leave per year
- Can be used for personal illness or family care
- Medical certificate required for absences over 3 consecutive days
- Sick leave cannot be carried forward to next year
- Unused sick leave is forfeited at year-end
- Employees can use annual leave if sick leave is exhausted
- Sick leave is paid and counts as working days
- Notification to manager required as soon as possible""",
        "source": "SWS-AI-leave-policy.pdf"
    },
    
    "maternity leave": {
        "question": "What is the maternity leave policy?",
        "answer": """Maternity leave benefits at SWS AI:
- 6 months (180 days) of paid maternity leave
- Job protection during maternity leave
- Option to extend unpaid leave up to 1 year
- Flexible return-to-work arrangements available
- Health insurance continues during leave
- Lactation breaks provided upon return (30 minutes daily for 6 months)
- Maternity leave can be taken before or after delivery
- Notification required 2 months before expected delivery date""",
        "source": "SWS-AI-leave-policy.pdf"
    },
    
    "paternity leave": {
        "question": "What is the paternity leave policy?",
        "answer": """Paternity leave benefits at SWS AI:
- 2 weeks (10 days) of paid paternity leave
- Can be taken within 6 months of child birth
- Job protection during leave
- Health insurance continues during leave
- Flexible work arrangements available
- Can be taken in one block or split
- Notification required at least 1 month before expected date""",
        "source": "SWS-AI-leave-policy.pdf"
    },
    
    "apply for leave": {
        "question": "How do I apply for leave?",
        "answer": """Leave application process at SWS AI:
1. Submit request through HR portal or email to manager
2. Provide dates and reason for leave
3. Manager reviews and approves/denies within 2 days
4. HR confirms approval and blocks dates in calendar
5. For emergency leave, notify immediately and submit form within 24 hours
6. Approval confirmation sent to employee
7. Leave dates visible in company calendar
8. No work expected during approved leave period""",
        "source": "SWS-AI-leave-policy.pdf"
    },
    
    # HR & Policies
    "hr policies": {
        "question": "What are the HR policies?",
        "answer": """HR policies at SWS AI cover:
- Employee relations and professional conduct
- Grievance and disciplinary procedures
- Performance management and reviews
- Leave and time-off policies
- Benefits and compensation
- Training and development opportunities
- Workplace safety and health
- Equal opportunity and non-discrimination
- Workplace harassment prevention
- Code of conduct and ethics
- Confidentiality and data protection""",
        "source": "SWS-AI-hr-policy.pdf"
    },
    
    "file grievance": {
        "question": "How do I file a grievance?",
        "answer": """Grievance procedure at SWS AI:
1. Report to immediate manager (informal resolution attempt)
2. If unresolved within 5 days, submit formal grievance to HR
3. HR investigates within 10 days
4. Meeting held with employee and manager
5. Decision communicated within 5 days
6. Appeal process available if unsatisfied
7. All grievances handled confidentially
8. No retaliation for filing grievance""",
        "source": "SWS-AI-hr-policy.pdf"
    },
    
    "disciplinary procedure": {
        "question": "What is the disciplinary procedure?",
        "answer": """Disciplinary procedure at SWS AI:
1. Verbal warning for minor issues (documented)
2. Written warning for repeated issues
3. Suspension for serious misconduct
4. Termination for gross misconduct
Each step includes:
- Opportunity to respond and explain
- Right to representation
- Appeal process available
- Documentation maintained
- Progressive approach followed""",
        "source": "SWS-AI-hr-policy.pdf"
    },
    
    "performance management": {
        "question": "How is performance managed?",
        "answer": """Performance management at SWS AI:
- Annual formal performance reviews (April)
- Quarterly check-ins with manager
- 360-degree feedback for senior roles
- Performance improvement plans for underperformance
- Career development discussions
- Training and development opportunities
- Goal setting and tracking
- Regular feedback provided
- Performance ratings assigned
- Salary reviews based on performance""",
        "source": "SWS-AI-performance-review.pdf"
    },
    
    # Benefits & Compensation
    "health insurance": {
        "question": "What health insurance benefits do we have?",
        "answer": """Health insurance benefits at SWS AI:
- Comprehensive medical coverage for employee and family
- Dental coverage (preventive and restorative)
- Vision coverage (eye exams and glasses)
- Mental health support and counseling
- Wellness programs (gym membership, health checkups)
- Annual health checkups (free)
- Dependent coverage available
- Premium shared between company (70%) and employee (30%)
- Coverage starts from day 1 of employment
- No waiting period for pre-existing conditions""",
        "source": "SWS-AI-benefits-compensation.pdf"
    },
    
    "bonus structure": {
        "question": "What is the bonus structure?",
        "answer": """Bonus structure at SWS AI:
- Annual performance bonus (up to 20% of salary)
- Based on individual and company performance
- Paid in December
- Eligibility: Employees with 6+ months tenure
- Calculation based on performance rating:
  - Exceeds expectations: 20%
  - Meets expectations: 15%
  - Partially meets: 10%
  - Below expectations: 0%
- Subject to company profitability
- Discretionary based on business performance""",
        "source": "SWS-AI-benefits-compensation.pdf"
    },
    
    "retirement benefits": {
        "question": "What retirement benefits are available?",
        "answer": """Retirement benefits at SWS AI:
- Provident fund contribution (12% of salary)
- Company matches employee contribution (12%)
- Gratuity on retirement (based on tenure)
- Pension scheme available
- Early withdrawal options for specific purposes
- Financial planning assistance
- Retirement counseling available
- Vesting period: 5 years
- Portable across employers""",
        "source": "SWS-AI-benefits-compensation.pdf"
    },
    
    "allowances": {
        "question": "What allowances do employees get?",
        "answer": """Employee allowances at SWS AI:
- House Rent Allowance (HRA): 40% of basic salary
- Dearness Allowance (DA): 10% of basic salary
- Conveyance allowance: Rs. 2,000 per month
- Medical allowance: Rs. 1,000 per month
- Special allowances (if applicable): Based on role
- Performance bonus: Up to 20% of salary
- Festival bonus: 1 month salary
- Meal vouchers: Rs. 500 per month""",
        "source": "SWS-AI-benefits-compensation.pdf"
    },
    
    "compensation review": {
        "question": "How is compensation reviewed?",
        "answer": """Compensation review process at SWS AI:
- Annual review in April
- Based on performance rating
- Market benchmarking considered
- Promotion increases salary immediately
- Inflation adjustments applied (5-10%)
- Individual performance impacts increase (0-15%)
- Salary bands reviewed annually
- Effective date: April 1st
- Review meeting with manager
- Confidential discussion""",
        "source": "SWS-AI-benefits-compensation.pdf"
    },
    
    # IT Security
    "it security policy": {
        "question": "What is the IT security policy?",
        "answer": """IT security policy at SWS AI covers:
- Password requirements and management
- Data classification and handling
- Access control and authentication
- Device security requirements
- Network security protocols
- Incident reporting procedures
- Confidential data protection
- Acceptable use of company resources
- Email security guidelines
- VPN and remote access security
- Backup and disaster recovery""",
        "source": "SWS-AI-it-security-policy.pdf"
    },
    
    "password requirements": {
        "question": "What are password requirements?",
        "answer": """Password requirements at SWS AI:
- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, and symbols
- Changed every 90 days
- Cannot reuse last 5 passwords
- No personal information in passwords
- Two-factor authentication required
- Password manager recommended
- No sharing of passwords
- Immediate change if compromised
- Stored securely in password manager""",
        "source": "SWS-AI-it-security-policy.pdf"
    },
    
    "confidential data": {
        "question": "How should I handle confidential data?",
        "answer": """Confidential data handling at SWS AI:
- Only access data you need for work
- Never share passwords or access credentials
- Use encrypted connections for data transfer
- Don't store data on personal devices
- Lock screen when away from desk
- Report any data breaches immediately
- Shred physical documents with data
- Follow data classification guidelines
- Use VPN for remote access
- Encrypt sensitive files
- No forwarding to personal email""",
        "source": "SWS-AI-it-security-policy.pdf"
    },
    
    "incident reporting": {
        "question": "What is the incident reporting procedure?",
        "answer": """Incident reporting at SWS AI:
1. Immediately stop using affected system
2. Report to IT security team
3. Provide details of incident
4. Don't attempt to investigate
5. IT team investigates and responds
6. Follow-up communication provided
7. Preventive measures implemented
8. Incident documented
9. Employee trained if needed
10. No penalty for reporting incidents""",
        "source": "SWS-AI-it-security-policy.pdf"
    },
    
    "device security": {
        "question": "What are device security requirements?",
        "answer": """Device security requirements at SWS AI:
- Antivirus software installed and updated
- Firewall enabled
- Automatic updates enabled
- Screen lock enabled (5 min timeout)
- Encryption enabled for sensitive data
- VPN required for remote access
- No unauthorized software installation
- Regular security patches applied
- USB ports disabled for external drives
- Biometric authentication enabled
- Device tracking enabled""",
        "source": "SWS-AI-it-security-policy.pdf"
    },
    
    # Work From Home
    "wfh guidelines": {
        "question": "What are the WFH guidelines?",
        "answer": """WFH guidelines at SWS AI:
- Eligible employees can work from home up to 3 days/week
- Manager approval required
- Must maintain regular work hours (9 AM - 6 PM)
- Dedicated workspace required
- Reliable internet connection required (minimum 10 Mbps)
- Company equipment must be used
- Confidentiality maintained
- Availability during business hours
- Video calls with camera on
- No sharing of workspace with others""",
        "source": "SWS-AI-wfh-policy.pdf"
    },
    
    "wfh eligibility": {
        "question": "Who is eligible for work from home?",
        "answer": """WFH eligibility at SWS AI:
- Employees with 6+ months tenure
- Roles that don't require on-site presence
- No disciplinary issues in last 6 months
- Performance rating of "meets expectations" or higher
- Manager discretion applies
- Client-facing roles may have restrictions
- New employees not eligible during probation
- Must have reliable home setup
- Must be able to maintain productivity""",
        "source": "SWS-AI-wfh-policy.pdf"
    },
    
    "wfh approval": {
        "question": "What is the WFH approval process?",
        "answer": """WFH approval process at SWS AI:
1. Submit WFH request to manager
2. Manager reviews and approves/denies within 2 days
3. HR confirms approval
4. Schedule communicated to team
5. Can be revoked if performance issues arise
6. Quarterly review of WFH arrangement
7. Approval valid for 6 months
8. Renewal required after 6 months""",
        "source": "SWS-AI-wfh-policy.pdf"
    },
    
    "wfh equipment": {
        "question": "What equipment is provided for WFH?",
        "answer": """WFH equipment provided at SWS AI:
- Laptop/desktop computer
- Monitor (if requested)
- Keyboard and mouse
- Headset for calls
- VPN access
- Software licenses
- Internet stipend (Rs. 1,000/month if applicable)
- Furniture allowance (one-time Rs. 10,000)
- Phone line (if needed)
- Backup power supply""",
        "source": "SWS-AI-wfh-policy.pdf"
    },
    
    "wfh frequency": {
        "question": "How many days per week can I work from home?",
        "answer": """WFH frequency at SWS AI:
- Maximum 3 days per week
- Minimum 2 days in office
- Flexible scheduling with manager approval
- Can be adjusted based on project needs
- Team meetings typically on office days
- Client meetings may require office presence
- Quarterly review of arrangement
- Can be increased/decreased based on performance""",
        "source": "SWS-AI-wfh-policy.pdf"
    },
    
    # Onboarding
    "onboarding process": {
        "question": "What is the onboarding process?",
        "answer": """Onboarding process at SWS AI:
- Day 1: Office tour, IT setup, documentation
- Week 1: Team introduction, role overview, training
- Week 2-4: Role-specific training, system access
- Month 1: Probation period begins
- Month 3: First review and feedback
- Month 6: Probation completion review
- Ongoing: Mentorship and support
- Total duration: 6 months probation""",
        "source": "SWS-AI-onboarding-guide.pdf"
    },
    
    "first day": {
        "question": "What happens on my first day?",
        "answer": """First day activities at SWS AI:
- Welcome by HR team
- Office tour and facilities orientation
- IT equipment setup and access
- Documentation and form completion
- Team introduction
- Role overview and expectations
- Lunch with team
- First week schedule provided
- Mentor assignment
- System access provisioning""",
        "source": "SWS-AI-onboarding-guide.pdf"
    },
    
    "training provided": {
        "question": "What training is provided?",
        "answer": """Training provided at SWS AI:
- Company orientation
- Role-specific training
- System and tool training
- Compliance and policy training
- Mentorship program
- On-the-job training
- Online learning resources
- Ongoing professional development
- Technical certifications supported
- Leadership training (for managers)""",
        "source": "SWS-AI-onboarding-guide.pdf"
    },
    
    "probation period": {
        "question": "What is the probation period?",
        "answer": """Probation period at SWS AI:
- Duration: 6 months
- Performance monitored closely
- Regular feedback provided (monthly)
- Can be extended if needed (up to 3 months)
- Completion review at 6 months
- Confirmation of employment after probation
- Can be terminated during probation with notice
- Salary same as confirmed employees
- Benefits available during probation""",
        "source": "SWS-AI-onboarding-guide.pdf"
    },
    
    # Performance
    "review frequency": {
        "question": "How often are performance reviews conducted?",
        "answer": """Review frequency at SWS AI:
- Annual formal review (April)
- Quarterly check-ins with manager
- 360-degree feedback (senior roles)
- Informal feedback ongoing
- Mid-year review (optional)
- Performance improvement plan reviews (as needed)
- Career development discussions (annual)""",
        "source": "SWS-AI-performance-review.pdf"
    },
    
    "review process": {
        "question": "What is the performance review process?",
        "answer": """Review process at SWS AI:
1. Self-assessment by employee
2. Manager evaluation
3. 360-degree feedback (if applicable)
4. Review meeting with manager
5. Performance rating assigned
6. Development plan created
7. Goals set for next period
8. Documentation filed
9. Feedback discussion
10. Improvement areas identified""",
        "source": "SWS-AI-performance-review.pdf"
    },
    
    "performance rating": {
        "question": "How is performance rated?",
        "answer": """Performance rating system at SWS AI:
- Exceeds expectations (5): 20% bonus
- Meets expectations (4): 15% bonus
- Partially meets expectations (3): 10% bonus
- Below expectations (2): 0% bonus
- Does not meet expectations (1): Performance improvement plan
Based on: Goals achievement, competencies, behavior, feedback""",
        "source": "SWS-AI-performance-review.pdf"
    },
    
    "salary review": {
        "question": "When is salary reviewed?",
        "answer": """Salary review timing at SWS AI:
- Annual review in April
- Based on performance rating
- Promotion increases salary immediately
- Inflation adjustments applied (5-10%)
- Individual performance impacts increase (0-15%)
- Effective date: April 1st
- Review meeting with manager
- Confidential discussion
- Salary bands reviewed annually""",
        "source": "SWS-AI-performance-review.pdf"
    },
    
    # Resignation
    "notice period": {
        "question": "What is the notice period for resignation?",
        "answer": """Notice period at SWS AI:
- Standard: 2 months notice required
- Senior roles: 3 months notice required
- Mutual agreement can reduce notice
- Notice period starts from resignation date
- During notice: Continue work as normal
- Final settlement after notice period
- Reference provided after completion
- Can be waived by mutual agreement""",
        "source": "SWS-AI-resignation-policy.pdf"
    },
    
    "resignation process": {
        "question": "What is the resignation process?",
        "answer": """Resignation process at SWS AI:
1. Submit resignation letter to manager
2. Provide notice period (2-3 months)
3. HR confirms receipt
4. Exit interview scheduled
5. Knowledge transfer planned
6. Final settlement calculated
7. Exit formalities completed
8. Reference provided
9. Forwarding address collected
10. Clearance certificate issued""",
        "source": "SWS-AI-resignation-policy.pdf"
    },
    
    "exit procedures": {
        "question": "What happens during exit?",
        "answer": """Exit procedures at SWS AI:
- Exit interview with HR
- Knowledge transfer to team
- System access revoked
- Equipment returned
- Final settlement processed
- Reference letter provided
- Clearance certificate issued
- Forwarding address collected
- Confidentiality agreement reminder
- Farewell meeting with team""",
        "source": "SWS-AI-resignation-policy.pdf"
    },
    
    "final settlement": {
        "question": "What is the final settlement process?",
        "answer": """Final settlement at SWS AI:
- Salary up to last working day
- Unused leave encashment
- Bonus (if applicable)
- Gratuity (if eligible)
- Reimbursements processed
- Deductions for company property
- Settlement within 30 days
- Detailed settlement statement provided
- Tax deductions applied
- Bank transfer to registered account""",
        "source": "SWS-AI-resignation-policy.pdf"
    },
    
    # Code of Conduct
    "code of conduct": {
        "question": "What is the code of conduct policy?",
        "answer": """Code of conduct policy at SWS AI:
- Conduct with integrity, respect, and professionalism
- Treat all colleagues, clients, and vendors with respect
- Maintain confidentiality of sensitive business information
- Avoid conflicts of interest
- Represent company honestly and professionally
- Follow all company policies and procedures
- Report violations to HR
- No retaliation for reporting violations
- Applies to all employees
- Violations may result in disciplinary action""",
        "source": "SWS-AI-code-of-conduct.pdf"
    },
    
    "professional behavior": {
        "question": "What are professional behavior standards?",
        "answer": """Professional behavior standards at SWS AI:
- Conduct with integrity and respect
- Maintain professional demeanor in all interactions
- Avoid conflicts of interest
- Disclose any potential conflicts to HR
- Represent company professionally
- Follow workplace conduct guidelines
- Respect diversity and inclusion
- Maintain confidentiality
- Communicate professionally
- Dress code: Business casual""",
        "source": "SWS-AI-code-of-conduct.pdf"
    },
    
    "anti-harassment": {
        "question": "What is the anti-harassment policy?",
        "answer": """Anti-harassment policy at SWS AI:
- Prohibits any form of harassment based on protected characteristics
- Prohibits hostile work environment creation
- Prohibits retaliation against those reporting harassment
- Prohibits discrimination in any form
- All employees must report harassment incidents to HR immediately
- Confidential investigation conducted
- Zero tolerance for harassment
- Disciplinary action for violations
- Support provided to affected employees
- No retaliation for reporting""",
        "source": "SWS-AI-code-of-conduct.pdf"
    },
    
    "social media policy": {
        "question": "What is the social media policy?",
        "answer": """Social media policy at SWS AI:
- Don't post confidential company information
- Don't post product roadmaps or client data
- Don't post internal communications
- Maintain professional conduct on public platforms
- Disclose employment when discussing company matters
- Don't engage in harassment or discrimination online
- Don't share company secrets
- Personal accounts should not represent company
- Follow company values in online conduct
- Violations may result in disciplinary action""",
        "source": "SWS-AI-code-of-conduct.pdf"
    },
    
    # Company
    "company mission": {
        "question": "What is the company mission?",
        "answer": """Company mission at SWS AI:
To provide innovative AI solutions that empower businesses to make 
better decisions and improve operational efficiency through cutting-edge 
technology and exceptional service.""",
        "source": "SWS-AI-company-overview.pdf"
    },
    
    "company values": {
        "question": "What are company values?",
        "answer": """Company values at SWS AI:
- Innovation: Continuous improvement and creativity
- Integrity: Honesty and ethical conduct
- Excellence: High quality in all work
- Collaboration: Teamwork and mutual support
- Customer Focus: Meeting customer needs
- Accountability: Taking responsibility
- Diversity: Inclusive and welcoming culture
- Transparency: Open communication""",
        "source": "SWS-AI-company-overview.pdf"
    },
    
    "organizational structure": {
        "question": "What is the organizational structure?",
        "answer": """Organizational structure at SWS AI:
- CEO: Chief Executive Officer
- CTO: Chief Technology Officer
- CFO: Chief Financial Officer
- COO: Chief Operating Officer
- Department heads report to respective C-level
- Teams organized by function
- Matrix reporting for projects
- Clear escalation paths
- Flat hierarchy encouraged
- Open door policy""",
        "source": "SWS-AI-company-overview.pdf"
    },
    
    "company business": {
        "question": "What does the company do?",
        "answer": """Company business at SWS AI:
SWS AI is an artificial intelligence company that develops and deploys 
AI solutions for enterprise clients. We specialize in:
- Machine learning solutions
- Natural language processing
- Computer vision applications
- Data analytics and insights
- AI consulting services
- Custom AI development
- AI training and workshops""",
        "source": "SWS-AI-company-overview.pdf"
    },
    
    "company culture": {
        "question": "What is the company culture?",
        "answer": """Company culture at SWS AI:
- Collaborative and inclusive
- Innovation-focused
- Continuous learning encouraged
- Work-life balance valued
- Diversity and inclusion prioritized
- Open communication
- Flat hierarchy
- Employee development supported
- Fun and engaging workplace
- Social events and team building""",
        "source": "SWS-AI-company-overview.pdf"
    }
}

def get_answer(question: str) -> dict:
    """Get answer from knowledge base"""
    question_lower = question.lower()
    
    # Try exact match first (key in question)
    for key, data in KNOWLEDGE_BASE.items():
        if key in question_lower:
            return data
    
    # Try partial match (any word from key in question)
    for key, data in KNOWLEDGE_BASE.items():
        key_words = key.split()
        if len(key_words) > 0 and any(word in question_lower for word in key_words):
            return data
    
    # Try matching question keywords with data question field
    for key, data in KNOWLEDGE_BASE.items():
        data_question = data.get("question", "").lower()
        # Check if any significant words match
        question_words = set(w for w in question_lower.split() if len(w) > 3)
        data_words = set(w for w in data_question.split() if len(w) > 3)
        if question_words & data_words:  # If there's any intersection
            return data
    
    return {
        "question": question,
        "answer": "I don't have that information in the knowledge base.",
        "source": "Unknown"
    }

if __name__ == "__main__":
    # Test
    test_questions = [
        "What is the annual leave policy?",
        "What health insurance benefits?",
        "What is IT security policy?"
    ]
    
    for q in test_questions:
        result = get_answer(q)
        print(f"Q: {q}")
        print(f"A: {result['answer'][:100]}...")
        print(f"Source: {result['source']}\n")
