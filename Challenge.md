# Programming Challenge

Congratulations on being selected to participate in our technical test. It consists of a programming challenge and it will address different skills. Read the instructions carefully and we wish you the best of luck.

## Before You Start

Fork this repository and once you have finished your challenge, grant access to the Github user "matheus.dantas19". Upload all your deliverables to your forked repository. We will use it to evaluate your test.

## Introduction

We want you to develop a project that makes uses of the [MovieLens](https://grouplens.org/datasets/movielens/) dataset. It consists of three goals and the details on each one of them is given below.

## Preparing the Data

The first goal of this challenge is to obtain and prepare the data you will work with.

In order to do so, you must download a [publicly available dataset](http://files.grouplens.org/datasets/movielens/ml-25m.zip). You can find the details about what data is stored and how it is structured in the [instructions](http://files.grouplens.org/datasets/movielens/ml-25m-README.html).

Then, you are asked to write a program to read the input files for the dataset and create a database out of it. You can choose to use the database in memory, in files, or in a database management system, as long as you process and consume this data in the upcoming parts.

## Making the Data Available

The second goal of this challenge is to make the processed data available for consumption.

To do such, you must implement a REST API in and it should provide the following methods:
- List movies by title: given a title, we want to know what movies match the given title;
- List movies by year and genre: given a year and a genre, we want to know what movies match the given year and are of the given genre;
- List top K rated movies: given a number K, we want to know the best K rated movies in descending order;
- Bonus - list movies based on their popularity: in this dataset, there are some movies that do not have many ratings by users, so they end up with a higher score. The idea here is to implement a heuristic to find the popularity of the movies, taking into account the number of ratings.

## Consuming the Data

The third goal of this challenge is to consume the methods of the REST API.

Thus, you are asked to implement a client application that accesses such an API. It must have a graphical interface to interact with users to consume the three methods above. It is up to you how to design the user interface, as long as it is usable.

## Deliverables

You must provide the following artifacts:
- The source-code of the programs that you implemented;
- Your solution must be dockerized (provide a detailed guide on how to get it running);
- A set of instructions on how to prepare the environment, build the programs, run each part of the challenge, and how to use your project;
- Comments on what technologies and patterns you used and the reasons to do so, as well as the decisions you made throughout the challenge;
- Any other artifact you find relevant for your overall evaluation.

## Tips

- Make sure your instructions are easy to follow and that each step works as expected;
- Our main environment is Windows, so please make sure that your solution works on it;
- If you want, you can show us how you can set up your project using Docker;
- We suggest you implement the challenge using the following languages (you can use more than one of them if you want): Python, C#, Java, Typescript and/or JavaScript;
- Testing is more than welcome;
- Show us everything you know about best practices in Git;
- Think carefully about your code quality, in terms of maintainability, readability, and simplicity;
- Do not overengineer your solution.
