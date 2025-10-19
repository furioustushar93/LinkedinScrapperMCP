# 💬 Conversational Features - Ask Follow-Up Questions!

Your LinkedIn Scraper now supports **natural conversations** with context memory! Ask follow-up questions about results without repeating yourself.

## 🎯 What's New?

### ✨ Key Features

1. **Numbered Results** - All results show with numbers (#1, #2, #3...)
2. **Conversation Memory** - Gemini remembers your last 10 messages
3. **Context Awareness** - Ask "tell me more about #2" and it knows what you mean
4. **Follow-Up Questions** - Natural conversation flow
5. **Clear Command** - Reset conversation anytime

---

## 🚀 Example Conversation

### Initial Search
```
You: Search for Python developer jobs in San Francisco

🔧 Gemini calling: search_linkedin_jobs
✓ Tool executed successfully

💬 Gemini: I found several Python developer positions in San Francisco!

📋 Found 10 job(s):

1. **Senior Python Developer** at Google
   📍 Location: San Francisco, CA
   🔗 URL: https://linkedin.com/jobs/view/12345

2. **Python Backend Engineer** at Meta
   📍 Location: San Francisco, CA
   🔗 URL: https://linkedin.com/jobs/view/23456

3. **Full Stack Python Developer** at Stripe
   📍 Location: San Francisco, CA
   🔗 URL: https://linkedin.com/jobs/view/34567

[... 7 more jobs ...]

💡 You can ask: 'Tell me more about #2' or 'What's the salary for job #3?'
```

### Follow-Up Questions
```
You: Tell me more about job #2

💬 Gemini: Job #2 is the Python Backend Engineer position at Meta in San Francisco.
This role focuses on building scalable backend systems...
[Gemini provides detailed info from the stored context]

────────────────────────────────────────────────────────────────────────────────

You: What about the requirements for that one?

💬 Gemini: For the Python Backend Engineer position at Meta, the requirements include:
- 5+ years of Python experience
- Strong understanding of distributed systems
- Experience with databases like PostgreSQL, Redis...

────────────────────────────────────────────────────────────────────────────────

You: Compare this with job #1

💬 Gemini: Comparing the Meta position (#2) with the Google position (#1):

Google - Senior Python Developer:
- More senior level
- Focus on infrastructure
- Requires 8+ years experience

Meta - Python Backend Engineer:
- Mid-senior level
- Focus on backend APIs
- Requires 5+ years experience

────────────────────────────────────────────────────────────────────────────────

You: Which one pays better?

💬 Gemini: Based on the available information:
- Google position likely offers higher compensation (senior level)
- Typical range: $180k-$250k for senior roles at Google
- Meta position: $150k-$200k for mid-senior backend engineers

(Note: Actual salaries depend on many factors and may not be visible in job postings)
```

---

## 📝 How It Works

### 1. Results Are Numbered
When you search for anything, results are automatically numbered:

```
📋 Found 5 profile(s):

1. **John Doe**
   💼 Senior Python Developer at Google
   📍 San Francisco Bay Area

2. **Jane Smith**
   💼 Python Engineer at Meta
   📍 New York, NY

3. **Bob Johnson**
   💼 Full Stack Developer at Amazon
   📍 Seattle, WA
```

### 2. Context Is Preserved
The system remembers:
- ✅ Last search results (jobs, profiles, companies)
- ✅ Previous conversation (last 10 messages)
- ✅ What numbers refer to what items

### 3. Natural Language Understanding
You can refer to results in many ways:

```
"Tell me about #2"
"What's the salary for the second one?"
"More details on job number 3"
"Compare the first and third jobs"
"What about that Meta position?"
```

---

## 🎨 Use Cases

### Job Search Workflow
```
1. Search for jobs
   → Get numbered list

2. Ask about specific jobs
   → "Tell me about #2"
   → "What are requirements for #5?"

3. Compare jobs
   → "Compare #1 and #3"
   → "Which pays better?"

4. Get application links
   → "How do I apply for #2?"
```

### Profile Research Workflow
```
1. Find people
   → "Find data scientists in Seattle"

2. Learn more about specific profiles
   → "Tell me about profile #3"
   → "What's their background?"

3. Compare candidates
   → "Compare #1 and #2"
   → "Who has more experience?"
```

### Company Research Workflow
```
1. Get company info
   → "Tell me about Google as a company"

2. Ask follow-ups
   → "How many employees do they have?"
   → "What's their main focus?"
   → "Are they hiring?"
```

---

## 💡 Pro Tips

### Tip 1: Be Specific with Numbers
```
✅ Good: "Tell me more about job #2"
✅ Good: "What's the salary for the second one?"
❌ Vague: "Tell me more" (Gemini might not know what to tell more about)
```

### Tip 2: Use Context
```
You: Search for Python jobs in SF
     [Gets 10 results]

You: Now search for Java jobs in the same location

💬 Gemini: [Understands "same location" = San Francisco]
```

### Tip 3: Clear When Starting Fresh
```
You: clear

🔄 Conversation cleared!

You: [Start new conversation]
```

### Tip 4: Natural Follow-Ups
```
You: Get info about Microsoft

💬 Gemini: [Company info]

You: Are they bigger than Google?

💬 Gemini: [Compares based on previous context]
```

---

## 🛠️ Commands

| Command | What It Does |
|---------|-------------|
| `clear` | Clears conversation history and results |
| `quit` or `exit` | Exits the chat |
| Regular question | Processes with context |

---

## 🔍 Advanced Examples

### Example 1: Multi-Step Job Analysis

```
You: Search for remote Python jobs

📋 Found 15 job(s)...

You: Which ones are at startups?

💬 Gemini: Based on the results, jobs #3, #7, and #12 are at startup companies:
- #3: Python Engineer at TechStartup Inc.
- #7: Backend Developer at InnovateCo
- #12: Full Stack Python at StartupHub

You: Tell me more about #3

💬 Gemini: Job #3 - Python Engineer at TechStartup Inc.:
[Detailed information]

You: What do they work on?

💬 Gemini: TechStartup Inc. focuses on...
[Uses context from job #3]

You: Is this better than #7?

💬 Gemini: Comparing TechStartup Inc. (#3) with InnovateCo (#7)...
```

### Example 2: Profile Comparison

```
You: Find senior Python developers in New York

📋 Found 8 profile(s)...

You: Who has the most experience?

💬 Gemini: Based on the profiles, #1 (John Doe) has the most experience 
with 15+ years in Python development.

You: Compare their skills with #3

💬 Gemini: Comparing skills:
John Doe (#1): Python, Django, AWS, PostgreSQL, Docker
Jane Smith (#3): Python, Flask, GCP, MongoDB, Kubernetes

Both are strong, but #1 has more years of experience while #3 has 
more modern cloud-native skills.

You: Who should I hire for a cloud project?

💬 Gemini: For a cloud project, profile #3 (Jane Smith) might be a 
better fit because of her Kubernetes and GCP experience...
```

### Example 3: Company Research Chain

```
You: Get info about Anthropic

💬 Gemini: [Company information]

You: How many people work there?

💬 Gemini: According to the data, Anthropic has approximately...

You: Are they hiring?

💬 Gemini: Let me search for jobs at Anthropic...

🔧 Gemini calling: search_linkedin_jobs
✓ Tool executed successfully

Yes! I found 23 open positions at Anthropic...

You: Show me engineering roles

💬 Gemini: Here are the engineering positions:
#1: Senior Software Engineer...
#5: ML Engineer...
[Filters from previous results]
```

---

## 🎯 Benefits

### For Job Seekers
- ✅ Quick comparison of opportunities
- ✅ Deep dive into specific roles
- ✅ Natural conversation flow
- ✅ No need to repeat context

### For Recruiters
- ✅ Efficient candidate screening
- ✅ Quick profile comparisons
- ✅ Context-aware queries
- ✅ Streamlined research

### For Researchers
- ✅ Iterative investigation
- ✅ Follow-up questions
- ✅ Cross-reference information
- ✅ Natural workflow

---

## 🐛 Troubleshooting

### "I can't refer to previous results"
```
Solution: Make sure you got numbered results first.
Try: Search for something, then ask about "#1"
```

### "Gemini forgot the context"
```
Possible reasons:
1. More than 10 messages ago - context limit
2. Used 'clear' command - intentional reset
3. Server restarted - memory cleared

Solution: Repeat your search or question
```

### "Numbers don't match what I see"
```
Solution: Use the exact number format shown: #1, #2, etc.
```

---

## 📊 Conversation Memory

### What's Remembered
- ✅ Last 10 messages
- ✅ Last search results (full data)
- ✅ Previous queries and responses
- ✅ Context from tool calls

### What's NOT Remembered
- ❌ Messages from previous sessions
- ❌ Results after 'clear' command
- ❌ Data after server restart
- ❌ Messages beyond 10 exchanges back

---

## 🚀 Getting Started

### 1. Run the Client
```bash
python src/gemini_client.py
```

### 2. Do a Search
```
You: Search for Python jobs in Seattle
```

### 3. Ask Follow-Ups
```
You: Tell me about job #2
You: What about the salary?
You: Compare with #1
```

### 4. Clear When Needed
```
You: clear
```

---

## 🎓 Best Practices

1. **Start with a search** - Get numbered results first
2. **Use specific references** - "#2" not "that job"
3. **Ask naturally** - The system understands context
4. **Clear between topics** - Reset when switching focus
5. **Be specific** - "job #2" is clearer than "the second one"

---

## 🎉 Summary

Your LinkedIn Scraper is now **conversational**!

✨ Features:
- Numbered results for easy reference
- Conversation memory (10 messages)
- Natural follow-up questions
- Context-aware responses

💬 You can now:
- Search once, ask many questions
- Compare results naturally
- Deep dive into specific items
- Have multi-turn conversations

---

**Try it now!**
```bash
python src/gemini_client.py
```

Ask: "Search for Python jobs in San Francisco"
Then: "Tell me more about #2"

🚀 **Enjoy your conversational LinkedIn scraper!**

