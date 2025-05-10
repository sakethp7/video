# __import__('pysqlite3')
# import sys

# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# import streamlit as st
# import requests
# import os
# import re
# from pydantic import BaseModel, Field
# from crewai import Agent, Task, Crew, Process
# from crewai import LLM
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Define pydantic model for Manim code output
# class ManimCodeOutput(BaseModel):
#     code: str = Field(..., description="The complete Manim Python code")
#     scene_name: str = Field("", description="The name of the main scene class in the code (empty for all scenes)")

# # Set up the LLM
# def get_llm():
#     return LLM(model='anthropic/claude-3-7-sonnet-20250219', api_key=os.getenv('ANTHROPIC_API_KEY')
#     ,temperature=0.2,max_tokens=10000,max_completion_tokens=20000)

# # Define the agent
# def create_agents(llm):
#     # Agent 1: Content Generator Agent
#     content_generator_agent = Agent(
#         role="Educational Content Creator",
#         goal="Generate comprehensive educational content on mathematical topics",
#         backstory="""You are an expert mathematics educator with deep understanding of 
#         various mathematical concepts. You excel at explaining complex topics in clear, 
#         structured ways that make them accessible to students. You're known for your 
#         ability to break down difficult concepts into digestible chunks and for creating 
#         content that flows logically from introduction to advanced applications.""",
#         verbose=True,
#         llm=llm
#     )

  
#     manim_developer_agent = Agent(
#     role="Manim Animation Developer",
#     goal="""Transform educational content into beautiful animated visualizations using Manim stay aware of these kinds of errors:
#     NameError: name 'RightTriangle' is not defined in manim library use which are present dont halucinate
#     """,
#     backstory="""You are a Python developer specializing in mathematical animations 
#     using the Manim library (version 0.19.0). You have extensive experience translating mathematical 
#     concepts into visually stunning animations. You're skilled at writing clean, efficient 
#     Manim code that brings abstract mathematical concepts to life through animation.
#     You are known for creating perfectly timed animations with NO OVERLAPPING elements and
#     clear transitions between concepts.""",
#     verbose=True,
#     llm=llm
# )

#     return content_generator_agent, manim_developer_agent

# # Define the tasks
# def create_tasks(content_generator_agent, manim_developer_agent, topic):
#     # Task 1: Generate educational content
#     content_generation_task = Task(
#         name="generate_math_content",
#         description=f"""
#         Create comprehensive educational content about {topic} with the following:
        
#         1. Clear introduction to the concept
#         2. Step-by-step explanation of the key principles
#         3. Mathematical notation and formulas
#         4. At least one worked example demonstrating the concept
#         5. Suggestions for visual representations that would help illustrate the concept
        
#         Your content should be well-structured, engaging, and suitable for transformation 
#         into an animated video. Focus on both clarity and accuracy.
        
#         """,
#         agent=content_generator_agent,
#         expected_output="""Detailed educational content covering the requested mathematical topic,
#         including explanations, examples, and suggestions for visualization.""",
#     )

  

#     # Task 2: Develop Manim code based on content
#     manim_code_development_task = Task(
#     name="develop_manim_code",
#     description=f"""
#     Using the provided educational content about {topic}, create a Python script using 
#     the Manim library (version 0.19.0) that:
    
#     1. Implements all the key explanations from the content
#     2. Creates a SINGLE scene class named "MainScene" that inherits from Scene
#     3. Includes proper mathematical notation and formulas
#     4. Animates the worked examples with clear transitions
#     5. Uses color, movement, and timing effectively
    
#     CRITICAL REQUIREMENTS:
#     1. Create ONLY ONE scene class named "MainScene" - this is essential for proper rendering
#     2. Ensure your code follows these strict timing rules:
#        - Use self.wait() after each animation to provide breathing room
#        - NEVER have overlapping animations unless explicitly using AnimationGroup
#        - Always FadeOut or Transform old elements before introducing new ones in the same area
#        - Position text and equations with careful spacing (use buffers of at least 0.5)
#        - For text elements, use font_size parameter to control size
#     3. Start your response with: ```python
#     4. End your response with: ```
#     5. Include ONLY these two imports at the top:
#        ```
#        from manim import *
#        import numpy as np
#        ```
#     6. Your code must be complete and executable with no missing components
    
#     COMPATIBILITY REQUIREMENTS:
#     1. ONLY use standard Manim classes (v0.19.0):
#        - For geometric shapes, use: Circle, Square, Rectangle, Polygon, Line, Arrow, etc.
#        - For text, use: Text, Tex, or MathTex
#        - DO NOT use custom classes like 'RightAngleTriangle'
       
#     2. For a right-angled triangle, use Polygon:
#        ```python
#        triangle = Polygon(
#            ORIGIN, 
#            RIGHT * 4, 
#            UP * 3,
#            color=WHITE
#        )
#        ```
       
#     3. For right angle marks, use Square:
#        ```python
#        right_angle = Square(side_length=0.5, color=WHITE).move_to(
#            triangle.get_vertices()[0] + (RIGHT * 0.25 + UP * 0.25)
#        )
#        ```
      
#     4. DO NOT use print statements or comments with special Unicode characters
#     5. Use simple ASCII characters only in strings and comments
#     6. Use self.play() for all animations, not Transform() on its own
#     7. Break long animations into shorter sequences
    
#     GOOD EXAMPLE:
#     ```python
#     # Good spacing and timing example
#     title = Text("Integration Basics", font_size=48).to_edge(UP, buff=1.0)
#     self.play(Write(title))
#     self.wait(1)
    
#     # Later when we want to remove it:
#     self.play(FadeOut(title))
#     self.wait(0.5)
#     ```
#     """,
#     agent=manim_developer_agent,
#     expected_output="""A complete, well-structured Python script using Manim to animate
#     the educational content provided, with a single MainScene class and careful timing.""",
#     context=[content_generation_task]
# )
#     return content_generation_task, manim_code_development_task

# # Extract all scene class names from the code
# def extract_scene_classes(code):
#     scene_classes = []
#     pattern = r'class\s+(\w+)\s*\(\s*Scene\s*\)'
#     matches = re.finditer(pattern, code)
    
#     for match in matches:
#         scene_classes.append(match.group(1))
    
#     return scene_classes


# def extract_manim_code(result):
#     try:
#         # Convert result to string
#         result_str = str(result)
        
#         # Case 1: Standard code block with ```python ... ```
#         start_marker = "```python"
#         end_marker = "```"
        
#         start_pos = result_str.find(start_marker)
#         if start_pos != -1:
#             # Skip past the ```python part
#             code_start = start_pos + len(start_marker)
            
#             # Find the closing backticks
#             end_pos = result_str.find(end_marker, code_start)
            
#             # If we found both markers
#             if end_pos != -1:
#                 code = result_str[code_start:end_pos].strip()
#                 st.success("Found code between triple backticks")
#             else:
#                 # No ending marker, extract from start to end
#                 code = result_str[code_start:].strip()
#                 st.warning("No closing backticks found. Extracting from start marker to end.")
        
#         # Case 2: No start marker, but contains "from manim import"
#         elif "from manim import" in result_str:
#             # Find the start of what looks like Python code
#             code_start = result_str.find("from manim import")
#             code = result_str[code_start:].strip()
#             st.warning("No code block markers found. Extracting based on 'from manim import'")
        
#         # Case 3: No markers at all, but contains "class" and "Scene"
#         elif "class" in result_str and "Scene" in result_str:
#             # Start from where a class is defined that inherits from Scene
#             scene_class_match = re.search(r'class\s+\w+\s*\(\s*Scene\s*\)', result_str)
#             if scene_class_match:
#                 # Go back to find any imports
#                 import_pos = result_str.rfind("import", 0, scene_class_match.start())
#                 if import_pos != -1:
#                     code_start = import_pos
#                 else:
#                     code_start = scene_class_match.start()
                
#                 code = result_str[code_start:].strip()
#                 st.warning("No code markers or imports found. Extracting based on Scene class definition.")
#             else:
#                 st.error("No Scene class found. Cannot extract code.")
#                 return None
#         else:
#             st.error("Could not identify any code in the output.")
#             return None
        
#         # Ensure the code has proper imports
#         imports_to_add = []
#         if "from manim import" not in code and "import manim" not in code:
#             imports_to_add.append("from manim import *")
        
#         if "import numpy as np" not in code and "numpy" in code:
#             imports_to_add.append("import numpy as np")
            
#         if imports_to_add:
#             code = "\n".join(imports_to_add) + "\n\n" + code
#             st.warning("Added missing imports to the code.")
        
#         # Ensure it uses MainScene class - rename if necessary
#         if "class MainScene(Scene)" not in code:
#             # Find the first Scene class
#             scene_class_match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', code)
#             if scene_class_match:
#                 original_name = scene_class_match.group(1)
#                 st.warning(f"Renaming scene class from {original_name} to MainScene for consistency")
#                 code = code.replace(f"class {original_name}(Scene)", "class MainScene(Scene)")
#                 # Also replace any other references to this class name
#                 code = code.replace(f"{original_name}()", "MainScene()")
        
#         # Clean the code of any potentially problematic characters
#         # Remove any non-ASCII characters from comments and strings
#         cleaned_lines = []
#         for line in code.split('\n'):
#             # Only clean comments, not code
#             if '#' in line:
#                 comment_pos = line.find('#')
#                 code_part = line[:comment_pos]
#                 comment_part = line[comment_pos:]
#                 # Replace non-ASCII characters in comments with spaces
#                 cleaned_comment = ''.join(c if ord(c) < 128 else ' ' for c in comment_part)
#                 cleaned_lines.append(code_part + cleaned_comment)
#             else:
#                 cleaned_lines.append(line)
        
#         code = '\n'.join(cleaned_lines)
        
#         # Setting scene_name to "MainScene" to ensure only one scene is rendered
#         scene_name = "MainScene"
        
#         return ManimCodeOutput(code=code, scene_name=scene_name)
        
#     except Exception as e:
#         st.error(f"Error extracting code: {str(e)}")
#         if 'result_str' in locals():
#             st.code(result_str[:1000])
#         return None

# # Function to send code to the rendering API
# def render_manim_code(manim_code: ManimCodeOutput, api_url: str):
#     try:
#         if api_url.endswith('/'):
#             api_url = api_url[:-1]
            
#         st.info(f"Sending code to {api_url}/render")
        
#         # Create payload with the extracted code
#         payload = {
#             "code": manim_code.code,
#             "scene_name": manim_code.scene_name  # Empty string means render all scenes
#         }
        
#         # Send to API
#         response = requests.post(
#             f"{api_url}/render",
#             json=payload
#         )
        
#         if response.status_code != 200:
#             st.error(f"API returned status code {response.status_code}: {response.text}")
#             return None
            
#         data = response.json()
        
#         if data.get("success", False):
#             st.success(f"Rendering completed successfully! Scenes rendered: {', '.join(data.get('scenes_rendered', ['unknown']))}")
#             if "video_id" in data:
#                 return {"video_id": data["video_id"], "scenes_rendered": data.get("scenes_rendered", [])}
#             else:
#                 st.warning("No video ID returned from server")
#                 return None
#         else:
#             st.error(f"Rendering failed: {data.get('message', 'Unknown error')}")
#             return None
            
#     except Exception as e:
#         st.error(f"Error sending code to rendering API: {str(e)}")
#         return None

# # Streamlit App
# def main():
#     st.set_page_config(page_title="Math Animation Generator", page_icon="📚", layout="wide")
    
#     st.title("Math Concept Animation Generator")
#     st.write("Generate animated videos explaining mathematical concepts using AI and Manim")
    
#     # Input for API URL
#     api_url = st.sidebar.text_input(
#         "Rendering API URL", 
#         value="http://localhost:8000",
#         help="URL of the FastAPI rendering service"
#     )
    
#     # Input for the math topic
#     topic = st.text_input("Enter a mathematical topic or concept", value="Integration of partial fractions")
    
#     # Store video ID in session state
#     if 'video_id' not in st.session_state:
#         st.session_state.video_id = None
#     if 'manim_code' not in st.session_state:
#         st.session_state.manim_code = None
#     if 'content' not in st.session_state:
#         st.session_state.content = None
#     if 'scenes_rendered' not in st.session_state:
#         st.session_state.scenes_rendered = []
    
#     # Generate button
#     if st.button("Generate Animation"):
#         with st.spinner("Generating educational content and Manim code..."):
#             # Create the LLM, agents, and tasks
#             llm = get_llm()
#             content_generator_agent, manim_developer_agent = create_agents(llm)
#             content_generation_task, manim_code_development_task = create_tasks(
#                 content_generator_agent, manim_developer_agent, topic
#             )
            
#             # Create and run the crew
#             crew = Crew(
#                 agents=[content_generator_agent, manim_developer_agent],
#                 tasks=[content_generation_task, manim_code_development_task],
#                 verbose=True,
#                 process=Process.sequential
#             )
            
#             # Run the crew
#             result = crew.kickoff()
            
#             # Extract content if available
#             try:
#                 if hasattr(result, 'tasks_output') and result.tasks_output:
#                     for task_output in result.tasks_output:
#                         if hasattr(task_output, 'task') and task_output.task.name == "generate_math_content":
#                             st.session_state.content = task_output.output
#                             break
#             except Exception as e:
#                 st.warning(f"Could not extract educational content: {str(e)}")
            
#             # Extract the Manim code
#             manim_code = extract_manim_code(result)
#             if manim_code:
#                 st.session_state.manim_code = manim_code
#                 st.success("Manim code generated successfully!")
                
#                 # Display the code
#                 st.subheader("Generated Manim Code")
#                 st.code(manim_code.code, language="python")
                
#                 # Send the code to the rendering API
#                 with st.spinner("Sending code to rendering service..."):
#                     response = render_manim_code(manim_code, api_url)
#                     if response and "video_id" in response:
#                         st.session_state.video_id = response["video_id"]
#                         st.session_state.scenes_rendered = response.get("scenes_rendered", [])
#                         st.success(f"Video rendered successfully with {len(st.session_state.scenes_rendered)} scenes!")
#             else:
#                 st.error("Failed to extract Manim code from the agent's output.")
    
#     # Display educational content if available
#     if st.session_state.content:
#         with st.expander("Educational Content", expanded=False):
#             st.markdown(st.session_state.content)
    
#     # Display the video if available
#     if st.session_state.video_id:
#         st.subheader("Generated Animation")
#         try:
#             if api_url.endswith('/'):
#                 api_url = api_url[:-1]
            
#             video_url = f"{api_url}/video/{st.session_state.video_id}"
#             st.video(video_url)
#             st.success(f"Video ready! You can download it using [this link]({video_url})")
            
#             # Display rendered scenes
#             if st.session_state.scenes_rendered:
#                 st.info(f"Scenes in this video: {', '.join(st.session_state.scenes_rendered)}")
#         except Exception as e:
#             st.error(f"Could not display video: {str(e)}")

# if __name__ == "__main__":
#     main()

import streamlit as st
import requests
import os
import re
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
from crewai import LLM
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configure page settings and styling
st.set_page_config(
    page_title="Math Animation Studio",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 2rem;
    }
    .card {
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        background-color: white;
    }
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem;
    }
    .stButton button {
        background-color: #1E88E5;
        color: white;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
        border-radius: 4px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        padding: 0.75rem;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# Define pydantic model for Manim code output
class ManimCodeOutput(BaseModel):
    code: str = Field(..., description="The complete Manim Python code")
    scene_name: str = Field("", description="The name of the main scene class in the code")

# Set up the LLM
def get_llm():
    return LLM(
        model='anthropic/claude-3-7-sonnet-20250219', 
        api_key=os.getenv('ANTHROPIC_API_KEY'),
        temperature=0.2,
        max_tokens=10000,
        max_completion_tokens=20000
    )

# Define the agents
def create_agents(llm):
    # Agent 1: Content Generator Agent
    content_generator_agent = Agent(
        role="Educational Content Creator",
        goal="Generate comprehensive educational content on mathematical topics",
        backstory="""You are an expert mathematics educator with deep understanding of 
        various mathematical concepts. You excel at explaining complex topics in clear, 
        structured ways that make them accessible to students. You're known for your 
        ability to break down difficult concepts into digestible chunks and for creating 
        content that flows logically from introduction to advanced applications.""",
        verbose=False,  # Changed to False to reduce terminal output
        llm=llm
    )

    # Agent 2: Manim Developer Agent
    manim_developer_agent = Agent(
        role="Manim Animation Developer",
        goal="""Transform educational content into beautiful animated visualizations using Manim""",
        backstory="""You are a Python developer specializing in mathematical animations 
        using the Manim library (version 0.19.0). You have extensive experience translating mathematical 
        concepts into visually stunning animations. You're skilled at writing clean, efficient 
        Manim code that brings abstract mathematical concepts to life through animation.
        You are known for creating perfectly timed animations with NO OVERLAPPING elements and
        clear transitions between concepts.""",
        verbose=False,  # Changed to False to reduce terminal output
        llm=llm
    )

    return content_generator_agent, manim_developer_agent

# Define the tasks
def create_tasks(content_generator_agent, manim_developer_agent, topic):
    # Task 1: Generate educational content
    content_generation_task = Task(
        name="generate_math_content",
        description=f"""
        Create comprehensive educational content about {topic} with the following:
        
        1. Clear introduction to the concept
        2. Step-by-step explanation of the key principles
        3. Mathematical notation and formulas
        4. At least one worked example demonstrating the concept
        5. Suggestions for visual representations that would help illustrate the concept
        
        Your content should be well-structured, engaging, and suitable for transformation 
        into an animated video. Focus on both clarity and accuracy.
        """,
        agent=content_generator_agent,
        expected_output="""Detailed educational content covering the requested mathematical topic,
        including explanations, examples, and suggestions for visualization.""",
    )

    # Task 2: Develop Manim code based on content
    manim_code_development_task = Task(
        name="develop_manim_code",
        description=f"""
        Using the provided educational content about {topic}, create a Python script using 
        the Manim library (version 0.19.0) that:
        
        1. Implements all the key explanations from the content
        2. Creates a SINGLE scene class named "MainScene" that inherits from Scene
        3. Includes proper mathematical notation and formulas
        4. Animates the worked examples with clear transitions
        5. Uses color, movement, and timing effectively
        
        CRITICAL REQUIREMENTS:
        1. Create ONLY ONE scene class named "MainScene" - this is essential for proper rendering
        2. Ensure your code follows these strict timing rules:
           - Use self.wait() after each animation to provide breathing room
           - NEVER have overlapping animations unless explicitly using AnimationGroup
           - Always FadeOut or Transform old elements before introducing new ones in the same area
           - Position text and equations with careful spacing (use buffers of at least 0.5)
           - For text elements, use font_size parameter to control size
        3. Start your response with: ```python
        4. End your response with: ```
        5. Include ONLY these two imports at the top:
           ```
           from manim import *
           import numpy as np
           ```
        6. Your code must be complete and executable with no missing components
        
        COMPATIBILITY REQUIREMENTS:
        1. ONLY use standard Manim classes (v0.19.0):
           - For geometric shapes, use: Circle, Square, Rectangle, Polygon, Line, Arrow, etc.
           - For text, use: Text, Tex, or MathTex
           - DO NOT use custom classes like 'RightAngleTriangle'
           
        2. For a right-angled triangle, use Polygon:
           ```python
           triangle = Polygon(
               ORIGIN, 
               RIGHT * 4, 
               UP * 3,
               color=WHITE
           )
           ```
           
        3. For right angle marks, use Square:
           ```python
           right_angle = Square(side_length=0.5, color=WHITE).move_to(
               triangle.get_vertices()[0] + (RIGHT * 0.25 + UP * 0.25)
           )
           ```
          
        4. DO NOT use print statements or comments with special Unicode characters
        5. Use simple ASCII characters only in strings and comments
        6. Use self.play() for all animations, not Transform() on its own
        7. Break long animations into shorter sequences
        """,
        agent=manim_developer_agent,
        expected_output="""A complete, well-structured Python script using Manim to animate
        the educational content provided, with a single MainScene class and careful timing.""",
        context=[content_generation_task]
    )
    return content_generation_task, manim_code_development_task

# Extract all scene class names from the code (kept for utility)
def extract_scene_classes(code):
    scene_classes = []
    pattern = r'class\s+(\w+)\s*\(\s*Scene\s*\)'
    matches = re.finditer(pattern, code)
    
    for match in matches:
        scene_classes.append(match.group(1))
    
    return scene_classes

# Extract Manim code (minimal debugging messages)
def extract_manim_code(result):
    try:
        result_str = str(result)
        
        # Case 1: Standard code block with ```python ... ```
        start_marker = "```python"
        end_marker = "```"
        
        start_pos = result_str.find(start_marker)
        if start_pos != -1:
            code_start = start_pos + len(start_marker)
            end_pos = result_str.find(end_marker, code_start)
            
            if end_pos != -1:
                code = result_str[code_start:end_pos].strip()
            else:
                code = result_str[code_start:].strip()
        
        # Case 2: No start marker, but contains "from manim import"
        elif "from manim import" in result_str:
            code_start = result_str.find("from manim import")
            code = result_str[code_start:].strip()
        
        # Case 3: No markers at all, but contains "class" and "Scene"
        elif "class" in result_str and "Scene" in result_str:
            scene_class_match = re.search(r'class\s+\w+\s*\(\s*Scene\s*\)', result_str)
            if scene_class_match:
                import_pos = result_str.rfind("import", 0, scene_class_match.start())
                if import_pos != -1:
                    code_start = import_pos
                else:
                    code_start = scene_class_match.start()
                
                code = result_str[code_start:].strip()
            else:
                return None
        else:
            return None
        
        # Ensure the code has proper imports
        imports_to_add = []
        if "from manim import" not in code and "import manim" not in code:
            imports_to_add.append("from manim import *")
        
        if "import numpy as np" not in code and "numpy" in code:
            imports_to_add.append("import numpy as np")
            
        if imports_to_add:
            code = "\n".join(imports_to_add) + "\n\n" + code
        
        # Ensure it uses MainScene class - rename if necessary
        if "class MainScene(Scene)" not in code:
            scene_class_match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', code)
            if scene_class_match:
                original_name = scene_class_match.group(1)
                code = code.replace(f"class {original_name}(Scene)", "class MainScene(Scene)")
                code = code.replace(f"{original_name}()", "MainScene()")
        
        # Clean the code of any potentially problematic characters
        cleaned_lines = []
        for line in code.split('\n'):
            if '#' in line:
                comment_pos = line.find('#')
                code_part = line[:comment_pos]
                comment_part = line[comment_pos:]
                cleaned_comment = ''.join(c if ord(c) < 128 else ' ' for c in comment_part)
                cleaned_lines.append(code_part + cleaned_comment)
            else:
                cleaned_lines.append(line)
        
        code = '\n'.join(cleaned_lines)
        
        # Setting scene_name to "MainScene" to ensure only one scene is rendered
        scene_name = "MainScene"
        
        return ManimCodeOutput(code=code, scene_name=scene_name)
        
    except Exception as e:
        return None

# Function to send code to the rendering API
def render_manim_code(manim_code: ManimCodeOutput, api_url: str):
    try:
        if api_url.endswith('/'):
            api_url = api_url[:-1]
        
        # Create payload with the extracted code
        payload = {
            "code": manim_code.code,
            "scene_name": manim_code.scene_name
        }
        
        # Send to API
        response = requests.post(
            f"{api_url}/render",
            json=payload
        )
        
        if response.status_code != 200:
            return None
            
        data = response.json()
        
        if data.get("success", False):
            if "video_id" in data:
                return {"video_id": data["video_id"], "scenes_rendered": data.get("scenes_rendered", [])}
            else:
                return None
        else:
            return None
            
    except Exception as e:
        return None

# Animation spinner component
def animated_loader(text="Processing"):
    import time
    container = st.empty()
    for i in range(50):
        loading_text = text + "." * (i % 4)
        container.markdown(f"<div style='text-align: center; font-size: 20px; color: #1E88E5;'>{loading_text}</div>", unsafe_allow_html=True)
        time.sleep(0.1)
    return container

# Main application function
def main():
    # Application header
    st.markdown("<h1 class='main-header'>Math Animation Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Generate beautiful educational videos explaining mathematical concepts using AI</p>", unsafe_allow_html=True)
    
    # Hidden configuration in the sidebar (collapsed by default)
    with st.sidebar.expander("Advanced Configuration", expanded=False):
        api_url = st.text_input(
            "Rendering Service URL", 
            value="http://localhost:8000",
            help="URL of the rendering service (default is fine for most users)"
        )
    
    # Main card for input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        topic = st.text_input(
            "Enter a mathematical topic or concept",
            value="",
            placeholder="E.g., Partial Fractions, Pythagorean Theorem, Derivatives, etc."
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card' style='display: flex; justify-content: center; align-items: center; height: 80px;'>", unsafe_allow_html=True)
        generate_button = st.button("Generate Animation 🎬", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Store session state
    if 'video_id' not in st.session_state:
        st.session_state.video_id = None
    if 'manim_code' not in st.session_state:
        st.session_state.manim_code = None
    if 'content' not in st.session_state:
        st.session_state.content = None
    if 'scenes_rendered' not in st.session_state:
        st.session_state.scenes_rendered = []
    if 'generation_complete' not in st.session_state:
        st.session_state.generation_complete = False
    
    # Progress tracking
    if 'progress_status' not in st.session_state:
        st.session_state.progress_status = None
    
    # Handle generation workflow
    if generate_button and topic:
        st.session_state.generation_complete = False
        st.session_state.video_id = None
        
        # Progress container
        progress_container = st.container()
        
        with progress_container:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            # Step 1: Content Generation
            st.markdown("#### Step 1: Creating educational content")
            content_progress = st.progress(0)
            content_status = st.empty()
            content_status.markdown("🧠 Researching and planning educational content...")
            
            # Step 2: Animation Generation
            st.markdown("#### Step 2: Designing animations")
            animation_progress = st.progress(0)
            animation_status = st.empty()
            
            # Step 3: Video Rendering
            st.markdown("#### Step 3: Rendering final video")
            rendering_progress = st.progress(0)
            rendering_status = st.empty()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Run the generation process
        try:
            # Initialize the LLM and agents
            llm = get_llm()
            content_generator_agent, manim_developer_agent = create_agents(llm)
            content_generation_task, manim_code_development_task = create_tasks(
                content_generator_agent, manim_developer_agent, topic
            )
            
            # Create and run the crew
            crew = Crew(
                agents=[content_generator_agent, manim_developer_agent],
                tasks=[content_generation_task, manim_code_development_task],
                verbose=False,
                process=Process.sequential
            )
            
            # Animate content generation progress
            for i in range(40):
                content_progress.progress((i + 1) / 100)
                time.sleep(0.05)
            
            content_status.markdown("🧠 Analyzing mathematical concepts...")
            
            for i in range(40, 70):
                content_progress.progress((i + 1) / 100)
                time.sleep(0.05)
            
            content_status.markdown("📝 Formulating explanations and examples...")
            
            # Run the crew
            result = crew.kickoff()
            
            # Mark content as complete
            content_progress.progress(100)
            content_status.markdown("✅ Educational content created successfully!")
            
            # Extract the content
            try:
                if hasattr(result, 'tasks_output') and result.tasks_output:
                    for task_output in result.tasks_output:
                        if hasattr(task_output, 'task') and task_output.task.name == "generate_math_content":
                            st.session_state.content = task_output.output
                            break
            except:
                pass
            
            # Animate animation progress
            animation_status.markdown("🎨 Generating animation code...")
            
            for i in range(50):
                animation_progress.progress((i + 1) / 100)
                time.sleep(0.05)
            
            animation_status.markdown("💻 Optimizing animation sequences...")
            
            for i in range(50, 100):
                animation_progress.progress((i + 1) / 100)
                time.sleep(0.05)
            
            animation_status.markdown("✅ Animation code generated successfully!")
            
            # Extract the Manim code
            manim_code = extract_manim_code(result)
            
            if manim_code:
                st.session_state.manim_code = manim_code
                
                # Render the video
                rendering_status.markdown("🎬 Rendering animation frames...")
                
                # Animate rendering progress
                for i in range(30):
                    rendering_progress.progress((i + 1) / 100)
                    time.sleep(0.1)
                
                # Use the default API URL if not provided
                if not api_url:
                    api_url = "http://localhost:8000"
                
                # Send to rendering service
                rendering_status.markdown("🎥 Processing video...")
                response = render_manim_code(manim_code, api_url)
                
                for i in range(30, 90):
                    rendering_progress.progress((i + 1) / 100)
                    time.sleep(0.1)
                
                if response and "video_id" in response:
                    st.session_state.video_id = response["video_id"]
                    st.session_state.scenes_rendered = response.get("scenes_rendered", [])
                    rendering_progress.progress(100)
                    rendering_status.markdown("✅ Video rendered successfully!")
                    st.session_state.generation_complete = True
                else:
                    rendering_progress.progress(100)
                    rendering_status.markdown("❌ Video rendering failed. Please try again.")
            else:
                animation_status.markdown("❌ Animation code generation failed. Please try again.")
                rendering_status.markdown("⏸️ Video rendering skipped.")
        
        except Exception as e:
            st.error(f"An error occurred during generation. Please try again.")
    
    # Display results after generation is complete
    if st.session_state.generation_complete and st.session_state.video_id:
        results_container = st.container()
        
        with results_container:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 🎉 Your Math Animation is Ready!")
            
            # Video display
            if api_url.endswith('/'):
                api_url = api_url[:-1]
            
            video_url = f"{api_url}/video/{st.session_state.video_id}"
            st.video(video_url)
            
            # Download button
            st.markdown(f"<div style='text-align: center;'><a href='{video_url}' download='math_animation.mp4' target='_blank'><button style='background-color: #1E88E5; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;'>Download Video</button></a></div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Educational content in expander
            if st.session_state.content:
                with st.expander("View Educational Content", expanded=False):
                    st.markdown(st.session_state.content)
            
            # Code in expander for those who want to see it
            if st.session_state.manim_code:
                with st.expander("View Animation Code", expanded=False):
                    st.code(st.session_state.manim_code.code, language="python")
    
    # Footer
    st.markdown("<div class='footer'>Math Animation Studio © 2025 | Powered by AI and Mathematical Visualization</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
