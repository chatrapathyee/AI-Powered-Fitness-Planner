import streamlit as st
import streamlit.components.v1 as components

def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    if bmi < 18.5: return "Underweight", "#4D96FF"
    elif 18.5 <= bmi < 25: return "Normal weight", "#39FF14"
    elif 25 <= bmi < 30: return "Overweight", "#FFA500"
    else: return "Obese", "#FF4B4B"

def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Profile Settings")
        
        with st.expander("👤 Personal Details", expanded=True):
            name = st.text_input("Name", "Alex")
            age = st.number_input("Age", 18, 100, 25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        with st.expander("📏 Body Metrics", expanded=True):
            weight = st.number_input("Weight (kg)", 30, 200, 70)
            height = st.number_input("Height (cm)", 100, 250, 175)
            
        with st.expander("🎯 Goals & Lifestyle", expanded=True):
            activity_level = st.select_slider("Activity Level", options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"])
            fitness_goal = st.selectbox("Primary Goal", ["Weight Loss", "Muscle Gain", "Endurance", "Flexibility", "General Health"])
            dietary_preference = st.selectbox("Diet Type", ["No Preference", "Keto", "Vegan", "Vegetarian", "Paleo", "Mediterranean"])

        generate_btn = st.button("🚀 Generate My Plan")

        bmi = calculate_bmi(weight, height)
        category, color = get_bmi_category(bmi)
        st.markdown("---")
        st.markdown(f"### Your BMI: <span style='color:{color}'>{bmi}</span>", unsafe_allow_html=True)
        st.caption(f"Category: {category}")
        
        return name, age, gender, weight, height, activity_level, fitness_goal, dietary_preference, generate_btn

def render_hero_section():
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 class="hero-title">Smart Health</h1>
        <p class="hero-subtitle">"A strong body fuels a brilliant mind."</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glass-container animate-up" style="animation-delay: 0.1s;">
            <div style="font-size: 3rem; margin-bottom: 15px;">🥗</div>
            <h3>Smart Nutrition</h3>
            <p style="color: #cbd5e1; line-height: 1.6;">AI-crafted meal plans tailored to your metabolic rate, dietary preferences, and caloric needs.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="glass-container animate-up" style="animation-delay: 0.2s;">
            <div style="font-size: 3rem; margin-bottom: 15px;">💪</div>
            <h3>Adaptive Training</h3>
            <p style="color: #cbd5e1; line-height: 1.6;">Dynamic workout routines that evolve with your progress, from strength to endurance.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="glass-container animate-up" style="animation-delay: 0.3s;">
            <div style="font-size: 3rem; margin-bottom: 15px;">🧠</div>
            <h3>Holistic Approach</h3>
            <p style="color: #cbd5e1; line-height: 1.6;">Complete lifestyle strategy including sleep optimization, hydration, and mindset coaching.</p>
        </div>
        """, unsafe_allow_html=True)

def render_results(meal_plan_response, fitness_plan_response, strategy_response):
    st.markdown("---")
    st.title("Smart Health")
    st.markdown("### *Your Personal Path to Peak Performance*")
    
    tab1, tab2, tab3 = st.tabs(["🥗 Meal Plan", "🏋️‍♂️ Workout", "🚀 Holistic Strategy"])
    
    with tab1:
        if meal_plan_response:
            st.markdown(meal_plan_response.content)
        else:
            st.warning("Could not generate meal plan.")
        
    with tab2:
        if fitness_plan_response:
            st.markdown(fitness_plan_response.content)
        else:
            st.warning("Could not generate workout plan.")
        
    with tab3:
        if strategy_response:
            st.markdown(strategy_response.content)
        else:
            st.warning("Could not generate strategy.")

def render_particles():
    components.html("""
    <script>
        try {
            const parentDoc = window.parent.document;
            
            // Remove existing cursor elements
            const existingCursors = parentDoc.querySelectorAll('.custom-cursor-follower, .cursor-particle');
            existingCursors.forEach(el => el.remove());

            // Particle settings
            const colors = ["#4facfe", "#00f2fe", "#ffffff"];
            const particles = [];
            
            function createParticle(x, y) {
                const particle = parentDoc.createElement('div');
                particle.className = 'cursor-particle';
                
                const size = Math.random() * 4 + 2;
                const color = colors[Math.floor(Math.random() * colors.length)];
                
                particle.style.position = 'fixed';
                particle.style.width = size + 'px';
                particle.style.height = size + 'px';
                particle.style.backgroundColor = color;
                particle.style.borderRadius = '50%';
                particle.style.pointerEvents = 'none';
                particle.style.zIndex = '99999';
                particle.style.left = x + 'px';
                particle.style.top = y + 'px';
                particle.style.boxShadow = `0 0 ${size * 2}px ${color}`;
                particle.style.opacity = '0.8';
                
                parentDoc.body.appendChild(particle);
                
                // Animate particle
                const angle = Math.random() * Math.PI * 2;
                const velocity = Math.random() * 0.5 + 0.2;
                const dx = Math.cos(angle) * velocity;
                const dy = Math.sin(angle) * velocity;
                
                particles.push({
                    element: particle,
                    dx: dx,
                    dy: dy,
                    life: 1.0
                });
            }
            
            function animateParticles() {
                for (let i = particles.length - 1; i >= 0; i--) {
                    const p = particles[i];
                    p.life -= 0.02;
                    
                    if (p.life <= 0) {
                        p.element.remove();
                        particles.splice(i, 1);
                    } else {
                        const currentLeft = parseFloat(p.element.style.left);
                        const currentTop = parseFloat(p.element.style.top);
                        
                        p.element.style.left = (currentLeft + p.dx) + 'px';
                        p.element.style.top = (currentTop + p.dy) + 'px';
                        p.element.style.opacity = p.life;
                        p.element.style.transform = `scale(${p.life})`;
                    }
                }
                requestAnimationFrame(animateParticles);
            }
            
            animateParticles();

            // Mouse move handler
            let lastX = 0;
            let lastY = 0;
            
            parentDoc.addEventListener('mousemove', (e) => {
                const distance = Math.hypot(e.clientX - lastX, e.clientY - lastY);
                
                // Only create particles if moved enough distance
                if (distance > 5) {
                    createParticle(e.clientX, e.clientY);
                    lastX = e.clientX;
                    lastY = e.clientY;
                }
            });
            
            // Click burst
            parentDoc.addEventListener('mousedown', (e) => {
                for(let i=0; i<8; i++) {
                    createParticle(e.clientX, e.clientY);
                }
            });
            
        } catch (e) {
            console.log("Could not access parent document for cursor animation.");
        }
    </script>
    """, height=0)
