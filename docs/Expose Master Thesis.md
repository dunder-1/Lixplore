# Expose for my Master Thesis

### 1. Introduction

In this expose I would like to give an overview of the planned structure of my master thesis. I chose this topic because it includes elements of Natural Language Processing (NLP) and I find this field very interesting.
Nowadays, large amounts of data occur not only in structured but also increasingly in unstructured form. An example of this are natural language texts like books. Since these allow a free presentation, it is even more important to approach them in a structured way. This is where NLP comes into play. It aims at processing and analyzing data in natural language. However this field also offers a lot of challenges, because with natural language the context and interpretation has to be considered.

### 2. Research Question

My master thesis will deal with the question to what extent the process of a literature search could be simplified or automated. For this purpose, I would like to build on the work of Atezaz Ahmad: On the OpenLAIR 148 scientific texts from the area of Learning Analytics of the research field Education Technology were categorized based on the metrics used. These were then summarized into indicators. Thus, an indicator consists of at least one but rather several metrics. Several indicators form a learning activity of a learning event or objectives [1]. 
The learning events have the goal of leading to an increase in knowledge among the learners. There are 8 learning events: experiment, explore, practice, create, imitate, debate, receive, self-reflect/meta-learn. For each learning event there are a number of different activities that serve to initiate or review the learning process such as exercises or exams [2] [3].

Since this process has to be started all over again for new research literature, I would like to create a program that automatically performs the necessary steps and identifies the metrics for a given text, summarizes them into an indicator, and finally correctly assigns them to a learning activity of a learning event. I will use state of the art frameworks for NLP like the Natural Language Toolkit (NLTK) [4].

### 3. Methodology

In this section, I would like to go into more detail about the planned implementation. First, I will briefly introduce the technologies used and why they are important for solving the problem. Afterwards, the expected steps of the algorithm will be described briefly and a quick overview on how the algorithm might be evaluated is provided.

#### 3.1 Technology

The implementation uses the latest findings from the field of Natural Language Processing. Therefore, it also makes sense to use the leading framework from this area. The Natural Language Toolkit (NLTK) was chosen for this purpose. It offers the possibility to analyze natural language efficiently and to perform steps like classification or tokenization [4]. The texts to be analyzed are in PDF format. Therefore, it is important to extract them cleanly. For this purpose I use the library PyPDF2 [5]. Since NLTK and PyPDF2 are libraries of the Python programming language, this technology must of course also be used [6]. Apart from that I might also rely on data analysis libraries such as pandas [7].

#### 3.2 Algorithm

The algorithm to be developed should expectedly perform the following steps:

1. Extract the text of the literature (in PDF format)
2. Identify specific words (metrics and/or indicators) from the text.
3. Categorize the metrics into indicators
4. Categorize the indicators into learning activities of the learning events

The results should be a dataset that is able to extend the knowledge of the OpenLAIR. 

#### 3.3 Evaluation

To test this algorithm, I will use the metrics and categorizations already identified for the 148 scientific papers [1]. In this way, the performance of the algorithm can be evaluated. This step is very important, otherwise it cannot be guaranteed that the algorithm works correctly. Furthermore, it must also be checked to what extent the program can handle differently formatted PDF files, especially if they contain images.

### 4. Project Timeline

In this section I want to give an overview of the planned process of the master thesis. Since this is a programming project, I will probably spend most of the time on development. Nevertheless, the main focus is on creating the master thesis. To achieve this goal I plan the following time periods for different tasks:

| Task                                                         | Estimated duration |
| ------------------------------------------------------------ | ------------------ |
| Reading the related literature and analyzing the OpenLAIR dataset | 1 month            |
| Implementing the algorithm (incl. small tests, bug fixes etc.)<br />Evaluating the algorithm | 3 months           |
| Summarizing the findings and integrating them into the Master's thesis | 2 months           |

### Sources

[1] OpenLAIR, https://atezaz.github.io/display/data (Accessed: 2021-10-11)

[2] Leclercq, D. & Poumay, M. (2005). The 8 learning Events Model. (2005).1. LabSET

[3] Gruber, Marion. (2019). Design Thinking for Technology Enhanced Learning. 

[4] NLTK, https://www.nltk.org/ (Accessed: 2021-10-13)

[5] PyPDF2 (Github Repository), https://github.com/mstamy2/PyPDF2 (Accessed: 2021-10-13)

[6] Python, https://www.python.org/ (Accessed: 2021-10-14)

[7] pandas, https://pandas.pydata.org/ (Accessed: 2021-10-15)