# DishpitDev Software Style Guide

This document outlines the coding standards, style guidelines, Git workflow, and estimation practices we use at DishpitDev. Following these guidelines ensures code consistency, readability, maintainability, and realistic project planning across all our projects, both internal and open-source. 

Adherence to this guide is expected for all team members, and is strongly encouraged for external contributors.

## Table of Contents

[1. General Principles](#i-general-principles)

[2. Code Formatting](#ii-code-formatting)

[3. Documentation](#iii-documentation)

[4. Git Workflow](#iv-git-workflow)

[5. Code Review](#v-code-review)

[6. Commit Message Guidelines](#vi-commit-message-guidelines)

[7. Software Estimation](#vii-software-estimation)
  - [Break down work into less complex tasks](#break-down-work-into-less-complex-tasks)
  - [Estimate Uncertainty](#estimate-uncertainty)
  - [Do the math](#do-the-math)
  - [Prioritize](#prioritize)

[8. Open Source Contributions](#viii-open-source-contributions)

## I. General Principles

- Code should be easy to understand. Prioritize clarity over cleverness.
- Follow the established style within a project. Inconsistencies make code harder to read and maintain.
- Write code that is easy to modify and extend in the future.
- Design code that is easy to test.
- Avoid duplication code. Extract common logic into reusable functions or modules.
- Favor simple solutions over complex ones.
- Don't add functionality until it's actually needed.
- Handle errors gracefully and provide informative error messages.
- Be mindful of security vulnerabilities and follow secure coding practices.

## II. Code Formatting

- Use 4 spaces for indentation. Do *not* use tabs. Configure your editor to automatically convert tabs to spaces.
- Try to limit lines to a maximum of 120 characters. This improves readability, especially on smaller screens. Nobody wants to read your `AbstractConfigurableSingletonServiceFactoryGeneratorProvider`.
- Whitespace
  - Use 1 blank line to separate logical blocks of code.
  - Add a space after commas in argument lists and dictionaries.
  - Add spaces around operators (=, +, -, *, /, etc).
  - Do not add trailing whitespace at the end of lines.
- Naming Conventions
  - Use descriptive and meaningful names for variables, functions, and classes.
  - Follow language-specific naming conventions.
- Use K&R braces for all languages, with the exception of Allman for C#.

## III. Documentation

- Write clear and concise comments to explain complex logic, algorithms, and non-obvious code. Avoid commenting on the obvious.
- Document all public APIs thoroughly.
- Include a README file in each project with a clear description of the project, instructions for building and running the code, and information on how to contribute.
- For complex projects, create design documents to outline the architecture, data flow, and key design decisions.
- Provide user guides for applications and libraries.

## IV. Git Workflow

- Use the following branching model.
  - `main`: The main branch, representing the stable, production-ready code.
  - `feature/*`: Feature branches for developing new features. Create a new branch for each feature.
  - `bugfix/*`: Bugfix branches for fixing bugs.
  - `release/*`: Release branches for preparing a release.
  - `hotfix/*`: Hotfix branches for critical fixes to production.
- Use pull requests for all code changes. Pull requests provide an opportunity for code review and discussion.
- Use merge commits to preserve the history of feature branches. Squashing is acceptable for small, self-contained changes.
- Use a .gitignore file to exclude generated files, build artifacts, and other unnecessary files from the repository.

## V. Code Review

- All code must be reviewed before being merged into the `main` branch.
- Reviewers should focus on:
  - Code correctness
  - Code style
  - Code readability
  - Test coverage (if applicable)
  - Security vulnerabilities
  - Overall design
- Be specific and explain your reasoning.
- Address all review comments before merging the pull request.
- Iterate on the code until all reviewers are satisfied.

## VI. Commit Message Guidelines

- Start with a verb that denotes the change.
- Limit the subject line to 50 characters.
- Separate the subject from the body with a blank line.
- Use the body to provide more context and explain the reasoning behind the change.
- Reference issue numbers when applicable.

Example:
```
fix: handle edge case in user authentication

this commmit fixes an edge case in the user authentication process where users with special characters in their passwords were not able to log in. the password validation logic has been update to properly handle these characters.

fixes #42069
```

## VII. Software Estimation

### Break down work into less-complex tasks
| Complexity  | Time              |
|-------------|-------------------|
| small       | 1 day             |
| medium      | 3 days            |
| large       | 1 week (5 days)   |
| extra-large | 2 weeks (10 days) |

It is critical to use real wall-clock time here, which means:
- You must map complexity to actual time units. The whole point is to eventually get to a calendar-time estimate and you should do that mapping in as granular a way as possible.
- Use real wall-clock hours and days, not idealized "programmer days" that assume engineers will write code 8 hours a day. That is, in the above system, a `small` task is something that really will take about 4 hours, accounting for all the other things an engineer has to deal with during a normal workday.
- Try to capture realistic expected times. Don't be overly optimistic and go with "best-case": if something probably will take 3 days, but might take 1 if you get lucky, call it `medium`. On the other hand, don't be overly pessimistic: don't "upgrade" that `medium` to a `large` just to cover. Aim for the expected time.

The more granular you can get, the more accurate your ultimate estimate will be. If you're doing this well, most broken-down tasks should be `small` or `medium`. You should have few `larges` and probably no `extra-large` tasks.

A good approach is to do an initial rough estimate which _will_ include any number of too-large tasks, and then refine and break them further down later.

### Estimate Uncertainty
| Uncertainty Level | Multiplier |
|-------------------|------------|
| low               | 1.1        |
| moderate          | 1.5        |
| high              | 2.0        |
| extreme           | 5.0        |

The multiplier is a scale to get a pessimistic estimate. So if we have a `medium` task with `high` uncertainty, that means "I think this will take 3 days, but it could take up to 6 days" (3 x 2.0). Or, a `large` task with `low` uncertainty means "I expect this will take 5 days, but it might bleed over into the sixth day."

Like with the time estimate, aim to have low uncertainty. Too many `high` and `extreme` uncertainty estimates are a sign you want to iterate and refine your estimate.

### Do the math
Now it's just a matter of doing the math, given our complexity/uncertainty definitions, which will give you a broken-down estimate that looks like this:

| Task | Complexity | Uncertainty | Expected | Worst-case |
|------|------------|-------------|----------|------------|
| Refactor the doodad | small | low | 1 day | 1.1 days |
| Swizzle columns | large | moderate | 5 days | 7.5 days |
| Reticulate splines | medium | extreme | 5 days | 25 days |
| Reverse manifold intake | medium | medium  | 3 days | 4.5 days |
| Deploy | small | low | 1 day | 1.1 days |
| | | __Total:__ | __15 days__ | __39 days__ |

Thus, for this imaginary project: "I expect it'll take about 3 weeks. Worst-case, it could take up to 8 weeks."

### Prioritize
|    | Urgency    | Impact     | Example                                                              | Response                                                   |
|----|------------|------------|----------------------------------------------------------------------|------------------------------------------------------------|
| P0 | Critical   | Extensive  | System outage                                                        | Immediate                                                  |
| P1 | High       | Large      | Major feature malfunctioning                                         | Urgent but not out of business-as-usual schedule           |
| P2 | Moderate   | Moderate   | Minor feature malfunctioning                                         | Important but needs to be prioritized against other issues |
| P3 | Low        | Minor      | Functionality or feature prevents a few users from using the product | Part of routine work                                       |
| P4 | Negligible | Negligible | Minor issue that doesn't affect user base                            | Should be placed on backlog                                |

## VIII. Open Source Contributions

We welcome contributions to our open-source projects! Please follow these guidelines:

- Read the README file for the project to understand its purpose and how to contribute.
- Follow this style guide.
- Submit pull requests with clear descriptions of the changes.
- Include tests for any new features or bug fixes.
- Be respectful and professional in your interactions with other contributors.
- All contributions will be licensed under the project's existing open-source license.

## Appendix

### Revision History

| Date       | Version | Author                                | Description                                     |
|------------|---------|---------------------------------------|-------------------------------------------------|
| 2025.02.18 | v1.1.0  | [Dishpit](https://github.com/Dishpit) | Added information for open source contributions |
| 2024.10.12 | v1.0.0  | [Dishpit](https://github.com/Dishpit) | Initial draft                                   |