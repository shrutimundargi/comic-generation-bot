# comic-generation-bot


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

There are 5 parameters using which a animator (or a end user) can change to create different style to check if they meet their needs. The parameters are:

    Art-style: User can choose between multiple art styles native to the api like - Enhance, Anime, Photographic, Digital Art, Comic Book, Fantasy Art, Neon punk, Pixel art, Line art, Origami etc.
    CFG Scale:"CFG Scale" refers to Classifier Free Guidance Scale. It's a parameter that influences how strictly the AI model adheres to the input prompt when generating images. v2-x models respond well to lower CFG (IE: 4-8), where as v1-x models respond well to a higher range (IE: 7-14) and SDXL models respond well to a wider range (IE: 4-12).

<img width="595" alt="Screenshot 2024-02-20 at 1 04 25 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/c1f3c661-a3ca-4669-b1e2-bfbd4a92c535">

    Seed: "Seed" refers to a value used to initialize the algorithm's random number generator.The seed value is a crucial parameter in AI image generation that controls the randomness of the output. Specifying a seed allows for reproducibility and consistency in results, while not specifying it (or setting it to 0) results in varied and unpredictable outputs.

<img width="627" alt="Screenshot 2024-02-20 at 1 06 34 PM" src="https://github.com/shrutimundargi/comic-generation-bot/assets/48567754/abb33a60-fb52-44ce-a292-516a7a561528">

Steps: AI models like Stable Diffusion use a process called 'diffusion' to generate images. This process involves gradually transforming a pattern of random noise into a coherent image. The transformation occurs over a series of steps. In each step, the model slightly adjusts the image, making it progressively less random and more structured, based on the input prompt.

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





