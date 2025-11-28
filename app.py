import os
import time
import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from streamlit_lottie import st_lottie
from dotenv import load_dotenv
from components import render_sidebar, render_hero_section, render_results, render_particles

load_dotenv()

st.set_page_config(
    page_title="Smart Health",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("style.css")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.warning("GROQ_API_KEY not found in .env. Please enter it below.")
    api_key = st.text_input("Enter Groq API Key", type="password")
    if not api_key:
        st.stop()

model_ids = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"]

def get_model(model_id):    
    try:
        return Groq(id=model_id, api_key=api_key)
    except Exception as e:
        return None

def run_agent_with_retry(agent, prompt, retries=3, delay=2):
    for i in range(retries):
        try:
            return agent.run(prompt)
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if i < retries - 1:
                    time.sleep(delay * (i + 1))
                    continue
            if i == retries - 1:
                pass 
            return None
    return None

def get_agents(model):

    dietary_planner = Agent(
        model=model,
        description="Expert Nutritionist creating personalized meal plans.",
        instructions=[
            "Generate a detailed daily meal plan (Breakfast, Lunch, Dinner, Snacks).",
            "Focus on the user's dietary preferences and caloric needs.",
            "Include macronutrient estimates for each meal.",
            "Suggest hydration strategies.",
            "Format the output with clear Markdown headings and bullet points.",
        ],
        tools=[DuckDuckGoTools()],
        markdown=True
    )

    fitness_trainer = Agent(
        model=model,
        description="Elite Fitness Coach designing workout routines.",
        instructions=[
            "Create a comprehensive workout session or weekly plan.",
            "Include Warm-up, Main Workout (Sets/Reps), and Cool-down.",
            "Tailor intensity to the user's fitness level.",
            "Provide form tips and safety warnings.",
            "Format the output with clear Markdown headings and tables where appropriate.",
        ],
        tools=[DuckDuckGoTools()],
        markdown=True
    )

    team_lead = Agent(
        model=model,
        description="Holistic Health Strategist.",
        instructions=[
            "Synthesize the meal and workout plans into a cohesive lifestyle strategy.",
            "Explain how the diet supports the training and vice versa.",
            "Provide 3 actionable daily habits for success.",
            "Write in a motivating, encouraging tone.",
        ],
        markdown=True
    )
    return dietary_planner, fitness_trainer, team_lead

name, age, gender, weight, height, activity_level, fitness_goal, dietary_preference, generate_btn = render_sidebar()

if not generate_btn:
    render_hero_section()
else:
    with st.status("🧠 AI Agents are brainstorming...", expanded=True) as status:
        success = False
        meal_plan_response = None
        fitness_plan_response = None
        strategy_response = None

        for m_id in model_ids:
            try:
                st.write(f"🔄 Attempting with model: {m_id}...")
                current_model = Groq(id=m_id, api_key=api_key)
                dietary_planner, fitness_trainer, team_lead = get_agents(current_model)
                
                st.write("🥗 Nutritionist is analyzing your needs...")
                meal_prompt = (f"Create a 1-day meal plan for a {age} year old {gender}, {weight}kg, {height}cm. "
                               f"Goal: {fitness_goal}. Diet: {dietary_preference}. Activity: {activity_level}.")
                
                try:
                    meal_plan_response = dietary_planner.run(meal_prompt)
                except Exception as e:
                    if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                        st.warning(f"⚠️ Quota exceeded for {m_id}. Switching model...")
                        continue
                    else:
                        st.error(f"Error generating meal plan: {e}")
                        break

                time.sleep(1)
                st.write("🏋️‍♂️ Trainer is designing your workout...")
                fitness_prompt = (f"Create a workout session for a {age} year old {gender}, {weight}kg, {height}cm. "
                                  f"Goal: {fitness_goal}. Activity: {activity_level}. Focus on {fitness_goal}.")
                
                try:
                    fitness_plan_response = fitness_trainer.run(fitness_prompt)
                except Exception as e:
                     if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                        st.warning(f"⚠️ Quota exceeded for {m_id}. Switching model...")
                        continue
                     else:
                        st.error(f"Error generating fitness plan: {e}")
                        break

                time.sleep(1)
                st.write("🤝 Team Lead is finalizing the strategy...")
                strategy_prompt = (f"User: {name}. Combine this meal plan: {meal_plan_response.content} "
                                   f"and this workout: {fitness_plan_response.content} into a summary strategy.")
                
                try:
                    strategy_response = team_lead.run(strategy_prompt)
                except Exception as e:
                     if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                        st.warning(f"⚠️ Quota exceeded for {m_id}. Switching model...")
                        continue
                     else:
                        st.error(f"Error generating strategy: {e}")
                        break
                
                success = True
                break 

            except Exception as e:
                st.error(f"Unexpected error with {m_id}: {e}")
                continue
        
        if success:
            status.update(label="✨ Plan Generated Successfully!", state="complete", expanded=False)
        else:
            status.update(label="❌ Failed to generate plan.", state="error", expanded=True)
            st.error("Could not generate plan with any available model due to API limits. Please try again later.")


    render_results(meal_plan_response, fitness_plan_response, strategy_response)

render_particles()