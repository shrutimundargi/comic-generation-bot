# Shakespearify - Comic Generator


<img width="923" alt="Screenshot 2024-02-08 at 7 00 15 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/1d948bbb-bd30-4890-abc6-4d00b0a8ede7">


### ABOUT

The "Shakespearify" project is a pioneering endeavor that seamlessly blends AI-driven storytelling with captivating illustrations to contemporize the timeless works of Shakespeare for today's audience. Leveraging cutting-edge AI tools, the project dynamically segments and extracts Shakespearean texts, subsequently generating vibrant artistic prompts through OpenAI's API for visually engaging illustrations.

This innovative narrative transformation is brought to life through an interactive platform hosted on Streamlit, offering users an immersive and engaging experience. By combining AI-driven text processing with rich visual storytelling, "Shakespearify" bridges the gap between classic literature and modern technology, breathing new life into Shakespeare's masterpieces for a digital-savvy audience.

To ensure seamless data management and security, the project relies on the robust infrastructure of the Google Cloud Platform, providing a stable and reliable foundation for storing and processing the extensive dataset.

Ultimately, "Shakespearify" aims to reignite interest in Shakespeare's timeless stories by reimagining them in a digital context, fostering a deeper appreciation for his works among contemporary audiences while showcasing the transformative potential of AI in storytelling and artistic expression.

Furthermore, users have the option to effortlessly transform their beloved storybooks into captivating comics. Simply by uploading an EPUB file of the desired story, the system seamlessly converts it into an engaging comic strip, offering a delightful fusion of literature and visual storytelling.

### TECH STACK

<img width="824" alt="Screenshot 2024-02-08 at 7 09 50 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/6768fea8-a68c-481d-b477-5e4334f58fc6">

### Key Features

#### Home page

<img width="719" alt="Screenshot 2024-02-20 at 12 58 34 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/e18fe734-d991-4af5-a2ca-b836c33af558">

#### Illustration of the Shakespere play 'Macbeth'

<img width="715" alt="Screenshot 2024-02-20 at 1 00 06 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/63a999b9-0c03-4d9e-bd25-a05d0a1147d3">

#### Epub upload options

<img width="715" alt="Screenshot 2024-02-20 at 1 02 48 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/c385355f-214b-4221-bc5a-8af494613925">

Here are five customizable parameters available for the animator or end user to adjust and tailor their creative output:

Art Style: Users can select from a diverse range of art styles native to the API, including options like Enhance, Anime, Photographic, Digital Art, Comic Book, Fantasy Art, Neon punk, Pixel art, Line art, Origami, and more.

CFG Scale: Short for Classifier Free Guidance Scale, this parameter influences how closely the AI model follows the input prompt when generating images. Different model versions respond optimally to varying CFG scales: v2-x models perform well with lower CFG values (e.g., 4-8), v1-x models excel with higher ranges (e.g., 7-14), and SDXL models demonstrate proficiency across a wider range (e.g., 4-12). Adjusting this scale allows users to fine-tune the level of guidance provided to the AI model, catering to their specific preferences and requirements.

<img width="595" alt="Screenshot 2024-02-20 at 1 04 25 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/c1f3c661-a3ca-4669-b1e2-bfbd4a92c535">

Seed: The "Seed" parameter denotes a value utilized to initialize the algorithm's random number generator. This value plays a pivotal role in AI image generation as it governs the randomness of the output. By specifying a seed, users ensure reproducibility and consistency in results. Conversely, not specifying a seed (or setting it to 0) yields varied and unpredictable outputs. Adjusting the seed allows for fine control over the generated images, enabling users to explore different variations while maintaining the ability to replicate desired results.

<img width="627" alt="Screenshot 2024-02-20 at 1 06 34 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/abb33a60-fb52-44ce-a292-516a7a561528">

Steps: AI models such as Stable Diffusion employ a technique known as 'diffusion' to generate images. This process entails the gradual transformation of a random noise pattern into a coherent image. The transformation unfolds over a sequence of steps, with each step involving slight adjustments to the image. These adjustments progressively reduce randomness and enhance structure, guided by the input prompt. Modifying the number of steps allows users to influence the pace and granularity of the image generation process, enabling them to achieve the desired level of detail and refinement in the final output.

<img width="617" alt="Screenshot 2024-02-20 at 1 06 54 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/fc4d36d3-1b27-43ed-8bae-a52a0d9fcb49">

### Dynamic changes with different parameter values

#### Pixel art

<img width="596" alt="Screenshot 2024-02-20 at 1 07 37 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/15cc23c7-8912-4c6f-9c6f-9468a9838b63">

#### Line art

<img width="595" alt="Screenshot 2024-02-20 at 1 08 18 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/4a9f2bc6-a353-4914-9980-b6887ba7ad51">

#### Neon punk

<img width="592" alt="Screenshot 2024-02-20 at 1 12 23 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/ab6bdbf7-3fae-4479-a242-9d53852f80da">

#### Pixel art for another prompt

<img width="585" alt="Screenshot 2024-02-20 at 1 12 55 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/9fe00249-e76e-4198-be31-8e587b655eff">





