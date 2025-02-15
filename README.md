# Complex Cobotics Framework
A framework for interaction with cobots. So far it has been applied to two robots, a robotic arm and a wheeled robot. 

The robot associates (by an LLM) transcriptions of sensory input to functions from a defined library. If these functions require planning (they are "complex") a planning domain will be instantiated with the current state variables, solved, and executed, affecting the state variables.


A collaboration is a triad of a planning environment, a plan executor, and a cognitive architecture which interprets communication from the user in order to act in the real environment of the user. The collaboration should appeal to the user's environment, so here we harness human language as the communication medium, decoded with OpenAI's `whisper`. 

 ![diagram.png](resources/diagram.png)

## Running
Run with a `car` or an `arm`, on "deaf" mode, or with bypassing the LLM. (`--deaf` is recommended.)
```
$ python3 unify.py <--car, --arm> [--deaf] [--bypassLLM]
```

# More on How it Works
## Components
``` mermaid
graph LR
    subgraph CogArch
    C@{ shape: procs, label: "Audio"} --> B(Linear Composition)
    end
    B --> A((Interpretation))
    
    subgraph Cobot
    A --> D[Automated Planning]
    A --> E(other functions)
    subgraph search domain
        D
        E
    end
    
    E --> O
    end
    D --> F(Problem)
    subgraph Autonomy
    G(Domain) --> F
    F --> H(Execution)
    H --> O[Action]
    end
    subgraph Inventory
    K[Inventory] --> F
    end
    O --remove--- K
```
### [CogArch](https://github.com/ogoudey/cog_arch)
A very minimal cognitive architecture. See arguments at the [repo](https://github.com/ogoudey/cog_arch) on which this is based.

Using two threads for recording and two for transcribing, we have a shortcut to a stream. As a form of communication, we here assume external, verbal (auditory) English is the best. The output is a sequence of text.
```mermaid
sequenceDiagram
    actor _
    _ ->> Recorder: audio
    Recorder->>+Transcriber: .wav
    
    _ ->> Recorder: audio
    Recorder->>+Transcriber: .wav
    Transcriber-->>-Composition: Yo yo yo! Could you move the block to the pad?
    Transcriber-->>-Composition: ... please?
```
### [Cobot](https://github.com/ogoudey/simple_cobots)
In addition to the requirements of communication, the robot is declared to be "collaborative" (the "co-" in "cobot"). It is collaborative with humans not only in that it parses human language: it also associates the language with actions. This is done with another foundational model. The "actions" are function calls from a defined set of functions, like a menu for the LLM to pick from. In the first figure this is called the Search Domain, but it should really be called a "domain for association". Below, this domain is called the Unified Library.
``` mermaid
flowchart LR
    Composition ---> P((Prompt))
    B@{ shape: braces, label: "'Which functions?'" } --> P

    L[Unified Library] --> P
    A[all functions deemed acceptable] --> L
    P ---|LLM Call|Response
```
The response is the interpretation, which chooses what to do next.

### [Autonomy](https://github.com/ogoudey/Ned2Autonomy)
Should the interpretation yield a "complex" action (a "planning problem"), the cobot will call a planner. The problem domain for the planner is derivative: Each time a complex action is required, the domain refers to the `Inventory` for what the domain actually is.

## Running
### Set up
For the full version, the equired Python packages are:
`openai`, `pyaudio` (`sudo apt install portaudio19-dev` might be required), `whisper` (`pip install git+https://github.com/openai/whisper.git`), `pyniryo2`, `unified-planning`, `unified-planning[pyperplan]`

Make sure the microphone works, and if not running as mock, that a Ned2 (or other) is connected.
