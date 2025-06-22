<h1 align="center">Explain Youtube Video or Documents To Me Like I'm 5</h1>

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Have a 5-hour YouTube video or a folder of long documents but no time to read them? This LLM application pulls the main topics and explains them to you like you're 5, so you can catch up in just minutes.

<div align="center">
  <img src="./assets/front.png" width="700"/>
</div>

Design Doc: [docs/design.md](docs/design.md), Flow Source Code: [src/youtube_processor/flow.py](src/youtube_processor/flow.py)

Try running the code in your browser using the [demo notebook](https://colab.research.google.com/github/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/demo.ipynb).



## Example Outputs

|  [<img src="https://img.youtube.com/vi/7ARBJQn6QkM/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/NVIDIA_CEO_Jensen_Huangs_Vision_for_the_Future.html) <br> **NVIDIA CEO Jensen Huang's Vision for the Future**  | [<img src="https://img.youtube.com/vi/_1f-o0nqpEI/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/DeepSeek_China_OpenAI_NVIDIA_xAI_TSMC_Stargate_and_AI_Megaclusters__Lex_Fridman_Podcast_459.html) <br> DeepSeek, China, OpenAI, NVIDIA, xAI, TSMC, Stargate, and AI Megaclusters | [<img src="https://img.youtube.com/vi/qTogNUV3CAI/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/Demis_Hassabis_-_Scaling_Superhuman_AIs_AlphaZero_atop_LLMs_AlphaFold.html) <br> Demis Hassabis – Scaling, Superhuman AIs, AlphaZero atop LLMs, AlphaFold | [<img src="https://img.youtube.com/vi/JN3KPFbWCy8/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/Elon_Musk_War_AI_Aliens_Politics_Physics_Video_Games_and_Humanity__Lex_Fridman_Podcast_400.html) <br> Elon Musk: War, AI, Aliens, Politics, Physics, Video Games, and Humanity |
| :-------------: | :-------------: | :-------------: | :-------------: |
|[<img src="https://img.youtube.com/vi/CnxzrX9tNoc/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/In_conversation_with_Elon_Musk_Twitters_bot_problem_SpaceXs_grand_plan_Tesla_stories__more.html) <br> **In conversation with Elon Musk: Twitter's bot problem, SpaceX's grand plan, Tesla stories & more** | [<img src="https://img.youtube.com/vi/blqIZGXWUpU/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/In_conversation_with_President_Trump.html) <br> **In conversation with President Trump** |  [<img src="https://img.youtube.com/vi/v0gjI__RyCY/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/Jeff_Dean__Noam_Shazeer_-_25_years_at_Google_from_PageRank_to_AGI.html) <br> **Jeff Dean & Noam Shazeer – 25 years at Google: from PageRank to AGI** |  [<img src="https://img.youtube.com/vi/4pLY1X46H1E/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/In_conversation_with_Tucker_Carlson_plus_OpenAI_chaos_explained.html) <br> **In conversation with Tucker Carlson, plus OpenAI chaos explained** | 
 |[<img src="https://img.youtube.com/vi/xBMRL_7msjY/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/Jonathan_Ross_Founder__CEO__Groq_NVIDIA_vs_Groq_-_The_Future_of_Training_vs_Inference__E1260.html) <br> **Jonathan Ross, Founder & CEO @ Groq: NVIDIA vs Groq - The Future of Training vs Inference** | [<img src="https://img.youtube.com/vi/u321m25rKXc/maxresdefault.jpg" width=200>](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/Volodymyr_Zelenskyy_Ukraine_War_Peace_Putin_Trump_NATO_and_Freedom__Lex_Fridman_Podcast_456.html) <br>**Volodymyr Zelenskyy: Ukraine, War, Peace, Putin, Trump, NATO, and Freedom** |  [<img src="https://img.youtube.com/vi/YcVSgYz5SJ8/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/Sarah_C._M._Paine_-_Why_Dictators_Keep_Making_the_Same_Fatal_Mistake.html) <br> **Sarah C. M. Paine - Why Dictators Keep Making the Same Fatal Mistake** |  [<img src="https://img.youtube.com/vi/4GLSzuYXh6w/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/Satya_Nadella_-_Microsofts_AGI_Plan__Quantum_Breakthrough.html) <br> **Satya Nadella – Microsoft's AGI Plan & Quantum Breakthrough** | 
 |[<img src="https://img.youtube.com/vi/qpoRO378qRY/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/Full_interview_Godfather_of_artificial_intelligence_talks_impact_and_potential_of_AI.html) <br> **Full interview: "Godfather of artificial intelligence" talks impact and potential of AI** |  [<img src="https://img.youtube.com/vi/OxP55dZjqZs/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/The_Stablecoin_Future_Mileis_Memecoin_DOGE_for_the_DoD_Grok_3_Why_Stripe_Stays_Private.html) <br> **The Stablecoin Future, Milei's Memecoin, DOGE for the DoD, Grok 3, Why Stripe Stays Private**   | [<img src="https://img.youtube.com/vi/oX7OduG1YmI/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/The_Future_Mark_Zuckerberg_Is_Trying_To_Build.html) <br> **The Future Mark Zuckerberg Is Trying To Build** |  [<img src="https://img.youtube.com/vi/f_lRdkH_QoY/maxresdefault.jpg" width=200> ](https://the-pocket.github.io/Tutorial-Youtube-Made-Simple/examples/Tucker_Carlson_Putin_Navalny_Trump_CIA_NSA_War_Politics__Freedom__Lex_Fridman_Podcast_414.html) <br> **Tucker Carlson: Putin, Navalny, Trump, CIA, NSA, War, Politics & Freedom** | 

## How to Run

### 1. Setup

First, install the required dependencies:
```bash
pip install -r requirements.txt
```

Next, set up your LLM credentials in `src/youtube_processor/utils/call_llm.py`. You can refer to the PocketFlow [LLM Wrappers documentation](https://the-pocket.github.io/PocketFlow/utility_function/llm.html) for guidance.

You can verify that your LLM is correctly set up by running:
```bash
python src/youtube_processor/utils/call_llm.py
```

### 2. Run the Processor

You can process content from either a YouTube URL or a local folder containing `.txt` and `.pdf` files.

#### Process a YouTube Video
```bash
python main.py --url "https://www.youtube.com/watch?v=example"
```

#### Process a Local Folder
```bash
python main.py --folder "path/to/your/folder"
```

If you don't provide a `--url` or `--folder` flag, the script will prompt you to enter a YouTube URL.

#### Language Options

You can process the content in English (default) or Vietnamese. Use the `-v` flag for Vietnamese:

```bash
# Process a YouTube video in Vietnamese
python main.py --url "https://www.youtube.com/watch?v=example" -v

# Process a local folder in Vietnamese
python main.py --folder "path/to/your/folder" -v
```

### 3. View the Output

When the script is finished, it will create an `output.html` file in the project folder. Open this file in your browser to see the results.

## I built this in just an hour, and you can, too.

- Built With [Pocket Flow](https://github.com/The-Pocket/PocketFlow), a 100-line LLM framework that lets LLM Agents (e.g., Cursor AI) build Apps for you

- **Check out the Step-by-Step YouTube Tutorial:**
 
<br>
<div align="center">
  <a href="https://youtu.be/wc9O-9mcObc" target="_blank">
    <img src="./assets/youtube.png" width="500" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>
