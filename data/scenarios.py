"""
10 Test Scenarios — each with Intent, Key Facts, Tone, and a Human Reference Email
"""

SCENARIOS = [
    {
        "id": 1,
        "intent": "Follow up after a job interview",
        "key_facts": [
            "Interview was yesterday with hiring manager Sarah Johnson",
            "Role is Senior Product Manager",
            "Discussed roadmap prioritization framework",
            "Next step is a technical case study"
        ],
        "tone": "Professional, enthusiastic",
        "reference_email": {
            "subject": "Thank You — Senior PM Interview Follow-Up",
            "body": """Hi Sarah,

Thank you for the time yesterday — I left the conversation genuinely energized about the Senior Product Manager role and the team you're building.

The discussion around roadmap prioritization particularly resonated with me. The framework your team uses for balancing customer requests against strategic bets mirrors an approach I've refined over several product cycles, and I'd love to bring that experience to bear here.

I understand the next step is the technical case study, and I'm looking forward to it. Please let me know the timeline and any specific format preferences you have.

Thanks again,
[Sender]"""
        }
    },
    {
        "id": 2,
        "intent": "Request a budget approval from a manager",
        "key_facts": [
            "Requesting $8,000 for a team training program",
            "Training covers advanced data analytics",
            "ROI: expected 20% productivity gain",
            "Program runs over 6 weeks starting next month"
        ],
        "tone": "Formal, persuasive",
        "reference_email": {
            "subject": "Budget Approval Request — Data Analytics Training ($8,000)",
            "body": """Hi [Manager],

I'd like to request approval for an $8,000 investment in a data analytics training program for our team.

The 6-week program, starting next month, covers advanced analytics techniques directly applicable to our current workflows. Based on benchmarks from similar teams that have completed this training, we can expect a 20% productivity gain — which translates to significant output improvement without additional headcount.

The business case is straightforward: the program pays for itself within the first quarter post-completion.

Could you review and approve this before end of week so we can secure our cohort spot?

Thank you,
[Sender]"""
        }
    },
    {
        "id": 3,
        "intent": "Apologize to a client for a service outage",
        "key_facts": [
            "Outage lasted 3 hours on Monday morning",
            "Root cause was a server misconfiguration",
            "Issue is now fully resolved",
            "Offering a 15% credit on next invoice"
        ],
        "tone": "Apologetic, accountable, reassuring",
        "reference_email": {
            "subject": "Our Apology — Monday Service Outage & Resolution",
            "body": """Hi [Client Name],

I want to personally apologize for the service outage your team experienced Monday morning. A 3-hour disruption is unacceptable, and I understand the impact it may have had on your operations.

The outage was caused by a server misconfiguration introduced during a routine maintenance update. Our engineering team identified and resolved the issue fully by midday, and we have since implemented additional checks to prevent a recurrence.

As a direct acknowledgment of this disruption, we are applying a 15% credit to your next invoice automatically — no action needed on your end.

You have my commitment that we are treating this as a priority learning moment. If you'd like to discuss further, I'm available at your convenience.

Sincerely,
[Sender]"""
        }
    },
    {
        "id": 4,
        "intent": "Cold outreach to a potential business partner",
        "key_facts": [
            "Their company specializes in sustainable packaging",
            "Our company is a DTC food brand scaling rapidly",
            "Potential synergy: we need eco-friendly packaging at scale",
            "Requesting a 20-minute exploratory call"
        ],
        "tone": "Confident, concise, casual-professional",
        "reference_email": {
            "subject": "Sustainable Packaging Partnership — Quick Intro",
            "body": """Hi [Name],

Your work in sustainable packaging caught my attention — specifically how you've managed to scale eco-friendly solutions without the typical cost premium.

We're a fast-growing DTC food brand at an inflection point where our packaging decisions will have real environmental and business impact. Finding a partner who gets both sides of that equation matters to us.

I'd love a 20-minute call to explore whether there's a fit. Are you free sometime next week?

[Sender]"""
        }
    },
    {
        "id": 5,
        "intent": "Deliver bad news about a project delay",
        "key_facts": [
            "Product launch delayed by 3 weeks",
            "Reason: critical bug found in payment module",
            "New launch date is October 15th",
            "Team is working overtime to minimize further delays"
        ],
        "tone": "Transparent, calm, solution-focused",
        "reference_email": {
            "subject": "Product Launch Update — Revised Date: October 15th",
            "body": """Hi Team,

I want to give you a direct update on the product launch: we are pushing the date back 3 weeks to October 15th.

During final QA, our team identified a critical bug in the payment module that could affect transaction reliability. Launching with a known issue of this severity was not an option — getting this right protects both our customers and our reputation.

The engineering team is working overtime to resolve the bug, and we are confident in the October 15th date. We will share a daily progress update starting tomorrow.

Thank you for your understanding and continued effort on this launch.

[Sender]"""
        }
    },
    {
        "id": 6,
        "intent": "Request a letter of recommendation",
        "key_facts": [
            "Applying for MBA program at Wharton",
            "Application deadline is December 1st",
            "Worked with professor on two research projects",
            "Professor knows the candidate's analytical skills well"
        ],
        "tone": "Respectful, humble, specific",
        "reference_email": {
            "subject": "Recommendation Letter Request — Wharton MBA Application",
            "body": """Dear Professor [Name],

I hope you're well. I'm writing to ask if you would be willing to write a letter of recommendation for my MBA application to Wharton, with a deadline of December 1st.

Our work together on the two research projects — particularly the analytical components — gave you a direct view of my capabilities that I believe would be valuable context for the admissions committee. Your perspective would carry significant weight given that depth of collaboration.

I fully understand this is a meaningful ask on your time, and I want to make the process as easy as possible for you. I'm happy to provide a draft, my resume, my personal statement, or any other materials that would be helpful.

Would you be open to a brief conversation this week to discuss?

With gratitude,
[Sender]"""
        }
    },
    {
        "id": 7,
        "intent": "Negotiate a salary offer",
        "key_facts": [
            "Offered $95,000, expecting $110,000",
            "Have a competing offer at $105,000",
            "3 years of directly relevant experience",
            "Very excited about the role and company"
        ],
        "tone": "Confident, collaborative, professional",
        "reference_email": {
            "subject": "Re: Job Offer — Discussion on Compensation",
            "body": """Hi [Recruiter Name],

Thank you for the offer — I'm genuinely excited about the role and the team, and I want to make this work.

I'd like to have an open conversation about the compensation. Based on my three years of directly relevant experience and current market benchmarks, I was targeting a base closer to $110,000. I also want to be transparent: I have a competing offer at $105,000, though this opportunity is my preference given the team and trajectory.

Is there flexibility to get closer to $110,000? I'm committed to contributing from day one and want to start the relationship aligned.

Looking forward to your thoughts,
[Sender]"""
        }
    },
    {
        "id": 8,
        "intent": "Invite stakeholders to a product demo",
        "key_facts": [
            "Demo scheduled for Thursday at 2 PM EST",
            "Product is an AI-powered inventory management tool",
            "Demo will last 45 minutes including Q&A",
            "Zoom link will be sent upon RSVP"
        ],
        "tone": "Enthusiastic, clear, professional",
        "reference_email": {
            "subject": "You're Invited: AI Inventory Tool Demo — Thursday 2 PM EST",
            "body": """Hi [Name],

I'd like to invite you to a live demo of our AI-powered inventory management tool this Thursday at 2 PM EST.

In 45 minutes — including time for Q&A — you'll see how the platform handles demand forecasting, reduces overstock, and integrates with existing ERP systems. We've had early users report significant reductions in carrying costs within the first 90 days.

Please reply to this email to confirm attendance, and I'll send the Zoom link right over.

Looking forward to showing you what we've built.

[Sender]"""
        }
    },
    {
        "id": 9,
        "intent": "Resign from a job professionally",
        "key_facts": [
            "Last working day is in 2 weeks",
            "Grateful for 4 years of growth at the company",
            "Leaving for a new opportunity",
            "Happy to help with transition and knowledge transfer"
        ],
        "tone": "Warm, professional, gracious",
        "reference_email": {
            "subject": "Resignation — [Your Name]",
            "body": """Hi [Manager Name],

I'm writing to formally let you know that I am resigning from my position, with my last working day being two weeks from today.

This has not been an easy decision. The four years I've spent here have shaped me professionally in ways I genuinely value — the projects, the people, and the growth opportunities have meant a great deal.

I'm stepping into a new opportunity that aligns with the direction I want to take my career, but I want to make this transition as smooth as possible. I'm fully committed to knowledge transfer, documentation, and supporting the handover of my responsibilities over these two weeks.

Thank you for everything.

Warmly,
[Sender]"""
        }
    },
    {
        "id": 10,
        "intent": "Send a project status update to leadership",
        "key_facts": [
            "Project is 75% complete",
            "On track for deadline next Friday",
            "One risk: dependency on third-party API still pending",
            "Mitigation plan: building a fallback module in parallel"
        ],
        "tone": "Concise, confident, professional",
        "reference_email": {
            "subject": "Project Status Update — Week of [Date]",
            "body": """Hi [Leadership Team],

Quick status update on the project:

We are 75% complete and on track for the deadline next Friday.

One risk worth flagging: we are still waiting on confirmation from a third-party API provider, which is on the critical path. To mitigate this, we are building a fallback module in parallel that will allow us to hit the deadline regardless of their timeline.

No action needed from your side at this stage — I'll flag immediately if that changes.

[Sender]"""
        }
    }
]
