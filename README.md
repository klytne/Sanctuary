# Wellness Journal – Sanctuary 

## Wellness Problem

Many people struggle to face their issues head-on with the increasing pressures of life, and opening up to someone could lead to the risk of their private issues being shared with more people. Additionally, many people come from different backgrounds that hinder them from seeking professional help or wellness resources. Most individuals also find themselves not making progress in their life goals because they always add more things to do and do not keep track of what they started on and what they are currently working on. This leads to an overwhelming feeling, and they become unhappy, depressed, or feel stagnant. They also lack a work-life balance 

## Wellness Solution

### Journal Page

The journal page comes with a gratitude quote and the author at the top, which the user could read before writing their entry to give them some inspiration. The quote changes each day that the user logs in. With a journal like Sanctuary, one could unpack as much as they can through journaling to survive and take on day-to-day responsibilities until their next booked appointment with their therapist. For people with limited wellness resources, the Sanctuary journal will be accessible to them and provides a calm, safe place to unpack, grow, reflect, and reconnect with themselves.  Often people find it hard to start an entry, especially if it’s completely new to them, so we’ve included some guided prompts to help people have a starting point for their entry by answering simple questions, which they could shuffle if they need more related questions that apply to them. The user can also reflect on past entries at the bottom of the page and have the option to delete. 

### Goals Page 

Under this page is a list of categories with the user’s tasks for each goal. For each task, there’s a progress bar that helps the user see how much they’ve covered. Most people like check boxes, and we’ve incorporated that so users can see what’s left to do. It also gives a sense of accomplishment to see how many boxes they’ve ticked. Each time the user works on their task, they time themselves and log the time spent on the app. 
Hobbies Tracker Page 
This page shows the user’s active hobbies and allows them to add new suggested hobbies that align with their interests. This way, they could explore different hobbies and get to know themselves a little more. Each time the user engages in their active hobbies, they log the time spent upon completion.  

### Insights Page

This page gives the person a weekly overview of the patterns in their mood across their entries through a bar graph. This way, the person can get a better understanding of how their feelings have changed over the week. The page also contains a streak section showing consistency in journaling and the days that the person journaled. This helps the user remain consistent to keep their streak alive. The gratitude themes section contains the recurring keywords that appeared in the user’s entries. 

The pages also display the amount of time that was allocated to each task and hobby according to what the user logged for the time spent on each task and hobby. The user can see their progress and adjust their schedule if they are not satisfied with the insights. 

### Settings Page 

With busy schedules, it’s hard to make time to journal and take a moment to breathe and reflect; therefore, with this page, the user can select the number of times they would be able to commit to journaling. To hold them accountable to their commitment, they have an option to enable gentle nudges when they leave mid-entry and notifications on the days they must journal, and this enforces discipline. They can personalize the notification, perhaps with something that guilt-trips them into fulfilling their promise. They can also select their interests to get personalized suggestions for their hobbies. 

## Tech Stack

### Framework

We used Streamlit as the core framework

### Standard Libraries

We used Python and its libraries for our wellness gratitude journal. The journal page uses the random Python standard library for the quotes and prompt questions that are shuffled. It randomly selects the quotes and prompts to be displayed on the page from a list that exists and recycles them once they are all used up.  datetime was used for streak calculations, reminders, and timestamps when the entries were written. The standard library re was used to match keywords from the gratitude themes on the insights page that appeared in the entries. collections. Counter  was used to tally the frequency  of the keywords from the gratitude themes that appeared in the journal entries. 

### Internal Modules

core.data_manager (dm) was used to handle saving journal entries, loading the entries, saving settings, and user information. The core. layout modules like require_login and render_account_bar were used for authentication and navigation. For core.styles, we used the inject_global_css module for the Sanctuary theme. 

## User Flow

1.Login/Register -> 2.Log entry on the journal page -> 3.Goals -> 4. Hobbies Tracker -> 5. View insights and consistency streaks -> 4. Settings for preferences

## Tools/Prompts

### Tools: 

1. Claude Sonnet 5 - free plan
2. Google Stitch Gemini 3 Flash - free plan
3. Git
4. VSCode

#### AI Prompts

- provide code for the profile.py page within streamlit for creating a user account. The URL has to be a login/register link
- write code for the journal.py page which comes right after the profile page
- write code for the insights.py file using this html file. the insights page is page number 3 and comes after the journal page
- write code for the goals.py file that comes after the insights page using the attached html file
- write code for the settings.py page that comes after the goals page
- generate code for the app.py file, which is the main file
- display the code for the goals page
- this is the insights page: (followed by pasted error)
- where are the account details i enter on the profile page going to? is there a database in place tat you've set up?
- (pasted terminal error, no separate question text)
- so should i paste the same code under insights?
- Change the following code in journal.py so that when the user wants to view past entries they can only see the log list without the full entry, and when they click the log name they can then see the full entry:
- add a delete function for the past entry incase the user might want to delete a past entry
- Does this also delete the json file with the entry?
- well i want code that creates the delete function for the past entries, a confirmation of the deletion and also deletes that specific entry from the json list, not all the entries but the selected one so right after saving the entry, it doesn't always clear the writing section and needs me to manually backspace. Add code that deletes after 'save entry'
- For this code, i would like the user to see different quotes everytime they log in related to gratitude, and not recycle the quotes (followed by pasted code)
- for th insight's file, replace all the emojis with icons, comment out the goal/hobbies related lines. There should only be the bar graph but make it a bit more clear
- for this code, display the days of the week and they should have circles. The circle that's filled witha green colour shows the day the streak was obtained. Try adding the fire icon next to the numbeer of streaks and remove ':material_local_fire_department:' from appearing on the page (followed by pasted code)
- okay use a fire emoji like before for the streak instead. I'm getting this on the page (followed by pasted HTML output)
- remove the consistency part and only keep the streak in this code (followed by pasted document)
- move the streak block slightly down so it's in alignment with the bargraph
- Add the emojis for the feelings to the bar graph, you removed the theme part so please add it back and the streak block put in such a way that it's midway the bar graph
- please fix the errors here: (followed by pasted code)
- (pasted code only, no separate question text)
- so for this specific insights file, I want the streak section to be little smaller and next to the bar graph on the side, not at the bottom of the bar graph. And I also want you to remove the small by space that is right on top of the theme that is right on top of the theme part. please (followed by pasted document)
- For the entries, when a entry name is clicked, a pop up should appear to show full log message, something like which uses Streamlit Dialog: (followed by pasted code
- I want to use the streamlit framework for a project but confused on the collaboration and how it works. How I and my coworker have to install it separately but then what gets tracked by the on Github?
- This is my current file structure for the... These are the changes I want to make: [IF NEEDED] Create data folder then redirect all data creation process to data folder with subfolders e.g data_storage/users/user.json; change profile page to login/register page; remove navigation from the left to the top; From login page, user shouldn't be able to see the other navigation tags; After user has logged in, profile tag shouldn't be visible; Remove app page; When the user json file is deleted and an old user creates an account again, it appears that the entries to that user still exist; after registering the user must be logged in and directed to the journal_entries page and same with the login page; if there are any emojis they should be replaced with icons e.g. icon=":material/delete:"; update colors and visuals to the design.md. Can you please help me makes the above changes and ask if you are unsure about something
- What does this mean and what is the problem?
- I keep on getting errors like this every time I try log in, register, and log out. And the first times, if I click the button the first time, I get an error like this. If I click on the second time, then it works. What's the issue?
- Can you help me with with some prefilled data that I can use to record as a demo video? It feels off like the the interface because it's empty. So what I need is just prefilled data directed to a specific user ID, which I'll provide. Its for a active user.
- I changed the date of created at to 2026-02-06
- I'm done with the demo video. I need help with deploying. I just wanna know how to deploy on Streamlit and the process and what I need to deploy. Before you give me the instructions, is it similar to Netlify where you connect to your GitHub?
- What is Streamlit as a framework? and in what situations can we use it for?
- I'm trying to deploy but I'm getting the error when I try visit the deployed site:
- Ok deployed we decided to add the other pages - goals and habit tracker. Lets start with the goals page I will give you the page by the google stitch ui/ux design and create the page but remember to stick to the design.md from the repo and also indicate where I need to make changes, for the goals page in the insights you also need to add the time allocation stats.

## Setup Instructions

If someone wants to set up from their local environment, they’ll git clone the repo and then install the requirements by running pip install -r requirements.txt. This installs the framework in the person’s local environment and any other dependencies that are needed to run the repo. The person can then run the environment by running streamlit run app.py. The local host link can be opened in the default browser.

## Challenges

We are in different time zones with a 7-hour time difference, making it hard for virtual meetups with our day-to-day responsibilities, but we found a way to get work done by splitting pages to work on right after the opening ceremony. 

We used Streamlit for our web app without knowing how the framework works, so we’re learning on the go. If we had more time, we would’ve learned how to connect it to real-world databases. It was my (Caroline) first time vibe coding and my first hackathon experience, so I needed to adapt to a hackathon environment 

We used AI tools on a free plan, which had limitations. This delayed the development of our web app by a few hours, and with more time, we could’ve perfected our features.  We wanted to add a timer that starts upon being clicked by the user in the hobbies tracker and goals pages and pauses when the user logs off the app, sending gentle nudges to remind the user to finish their session, but because of time, the user can only log time spent on each task and hobby.

## Credit

I (Caroline) created the UI/UX design using Google Stitch, handled the project management tasks and the documentation. Kelly handled the deployment and the demo video. We divided the development work and tasks based on the pages. I (Caroline) worked on the	Journal and Insights pages and Kelly worked on the Login, Settings, Goals and Hobbies Tracker pages.







