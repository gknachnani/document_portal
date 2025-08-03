- [Commands needs to follow](#commands-needs-to-follow)
- [below command is for windows(CMD)](#below-command-is-for-windowscmd)
- [for conda env setup](#for-conda-env-setup)
- [git commands(this commands is for the later uses)](#git-commandsthis-commands-is-for-the-later-uses)
  - [for cloning my repo use this command](#for-cloning-my-repo-use-this-command)
  - [minimum requirement for this project](#minimum-requirement-for-this-project)
- [GROQ API KEY LINK](#groq-api-key-link)
  - [GEMINI API KEY](#gemini-api-key)

## Commands needs to follow

## below command is for windows(CMD)

```
mkdir <project_folder_name>
```

```
cd <project_folder_name>
```

```
code .
```

## for conda env setup

```
conda create -p <env_name> python=3.10 -y
```

```
conda activate <path_of_the_env>
```

```
pip install -r requirements.txt
```

## git commands(this commands is for the later uses)

```
git init
```

```
git add .
```

```
git commit -m "<write your commit message>"
```

```
git push
```

### for cloning my repo use this command

```
git clone https://github.com/gknachnani/document_portal.git
```

### minimum requirement for this project

1. LLM Model ## groq(freely), openai(paid), gemini(15days free accesss), claude(paid), huggingface(freely),ollama(local setup)

2. Embedding model ## openai, hf, gemini

3. vectordatabase ##inmemory ##ondisk ##cloudbased

## GROQ API KEY LINK

```
https://console.groq.com/keys

https://console.groq.com/docs/overview
```

### GEMINI API KEY

```
https://aistudio.google.com/apikey

https://ai.google.dev/gemini-api/docs/models
```