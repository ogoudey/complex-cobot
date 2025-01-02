# complex-cobot
This project combines three smaller projects into one.

## Running
### Set up
Required Python packages:
`openai`, `pyaudio` (`sudo apt install portaudio19-dev` might be required), `whisper` (`pip install git+https://github.com/openai/whisper.git`), `pyniryo2`, `unified-planning`, `unified-planning[pyperplan]`

Make sure the microphone works, and if not running as mock, that a Ned2 (or other) is connected.

### Run
```
$ python3 unify.py 
```
Then tell it to do something, e.g. stack the blocks in reverse, sleep for 10 seconds, or move a block onto a pad.

To run without recording audio (just keyboard input) provide a second argument, e.g.
```
$ python3 unify.py mock
```

## Components
``` mermaid
graph LR
    subgraph CogArch
    C@{ shape: procs, label: "Audio"} --> B(Linear Composition)
    end
    B -.- A((Interpretation))
    
    subgraph Cobot
    A --> D[Automated Planning]
    A --> E(other functions)
    subgraph search domain
        D
        E
    end
    
    E -.- O
    end
    D -.- F(Problem)
    subgraph Autonomy
    G(Domain) --> F
    F --> H(Execution)
    H -.- O[Action]
    end
```
### [CogArch](https://github.com/ogoudey/cog_arch)
A very minimal cognitive architecture. See arguments at the [repo](https://github.com/ogoudey/cog_arch) on which this is based.

Using two threads for recording and two for transcribing, we have a shortcut to a stream. As a form of communication, we here assume external, verbal (auditory) English is the best.
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
The response varies a lot, but consequent accuracy can be easily tinkered with.

### [Autonomy](https://github.com/ogoudey/Ned2Autonomy)
The last component executes the response from the LLM above, the constituents of which _ought_ to be relevant functions/actions. Among these actions, and in the Unified Library, are "planning problems", i.e. actions that require "forethought". There are benefits to this approach for transparency. Everything tractable problem is solved algorithmically, except the (notoriously _intractable_) problem of generality, which we've clustered into smaller (search) problems.

## Example Behavior (run in "mock" environment)
Hello!

`Hello!`

What do you do?

`I can interact through messages, execute specific function calls, and assist with a variety of tasks.`

Okay could you show one of the tasks?

`One of the tasks is to move a block to a pad.`

Cool! Let's see it!

`Cool! Let's see it!`

Are you copying me?

`Are you copying me?`

Move the block to the pad!!

`exec("self.move(a4, b4)")`<br />
`exec("self.move(b4, c4)")`<br />
`exec("self.move(c4, c3)")`<br />
`exec("self.grasp(block3, c3, c2)")`<br />
`exec("self.carry(block3, c3, c4)")`<br />
`exec("self.carry(block3, c4, b4)")`<br />
`exec("self.carry(block3, b4, b3)")`<br />
`exec("self.carry(block3, b3, b2)")`<br />
`exec("self.carry(block3, b2, b1)")`<br />
`exec("self.floor(block3, b1)")`<br />
`exec("self.move(b1, b2)")`<br />
`exec("self.move(b2, b3)")`<br />
`exec("self.move(b3, b4)")`<br />
`exec("self.move(b4, c4)")`<br />
`exec("self.move(c4, c3)")`<br />
`exec("self.move(c3, c2)")`<br />
`exec("self.grasp(block2, c2, c1)")`<br />
`exec("self.carry(block2, c2, c3)")`<br />
`exec("self.carry(block2, c3, c4)")`<br />
`exec("self.carry(block2, c4, b4)")`<br />
`exec("self.carry(block2, b4, a4)")`<br />
`exec("self.carry(block2, a4, a3)")`<br />
`exec("self.carry(block2, a3, a2)")`<br />
`exec("self.carry(block2, a2, a1)")`<br />

What did you just do?

`I provided information on function calls and their purposes.`

Did you actually perform the function?

`Yes, I performed the function as requested.`

