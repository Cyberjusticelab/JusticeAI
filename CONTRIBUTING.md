# Contributing

## Project Development

We are actively developing this project by valuing working and test code over extensive documentation. However, we are using an Agile method to manage and track the project's progress.

### GitHub Issues and User Stories
GitHub issues are considered as user stories with associated story points, risk and priority.

Each user story must have:
- [x] the story description: "As a X, I want Y."
- [x] the story points assigned during poker planning
- [x] the story's priority
- [x] the story's technical risk
- [x] the engineering task breakdown, with the ideal time allocated for each task
- [x] any changes to the initial engineering solution
- [x] all documentation, diagrams, etc. related to that story
- [x] all tests passing and an approved and merged pull request which references the issue
- [x] the steps required to demo this story
- [x] product owner signoff


### GitHub Labels and Features

GitHub Labels must be attached to issues and are used to describe what specific aspect of the system the user story relates to.

### GitHub Milestones and Iterations

Our user stories, represented as GitHub issues, are assigned to iterations, represented as GitHub milestones. Iterations occur every two weeks and comprise a set of user stories.

### GitHub Tags and Releases

Releases occur every three iterations, are accompanied with a release document and are tagged within the repository.

## Pull Request Process

Pull requests can be created after branching from the `master` trunk or by forking the repository.

If you create any branch, the branch name ***must*** be in this format, or our continuous integration service will fail your build and you will not be able to merge:
```
<issue-number>/<short-description-of-issue>
```

An example might be:
```
87/store-user-session-data
```

In order for a pull request to be merged, it must have at least 2 approvals by reviewers that can validate your changes. Additionally, all continuous integration services must pass.

## Git Commit Style

We will be following a similar approach to the [Git commit guidelines](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project#_commit_guidelines).

Every commit in our repository ***must*** have a well-formatted message, or our continuous integration service will fail your build and you will not be able to merge:
```
[#<issue-number>] <very-short-summary-of-changes>

- Detailed bullet
- list of
- important changes
```

An example might be:
```
[#12] Added user login feature

    - Created user model
    - Added Oauth library to our dependencies for authyaoentication
    - Created a login page
```

## Coding Style Guide

We lint all source code with our continuous integration services using [Google's Style Guide](https://google.github.io/styleguide/) as a reference.

### Python
- Style Guide: https://google.github.io/styleguide/pyguide.html
- Tools: `pylint`, `flake8`

### HTML and CSS
- Style Guide: https://google.github.io/styleguide/htmlcssguide.html
- Tools: `csslint`, `HTMLBeautify`

### Javascript
- Style Guide: https://google.github.io/styleguide/jsguide.html
- Tools: `jshint`, `eslint`

## Unit Tests and Code Coverage

We expect every pull request to have unit tests. In order to ensure that unit tests are always being written, we are using CodeCov as a service which monitors for unit test code coverage. If the total code coverage falls below a certain preset percentage, or if that pull request introduces a large negative diff in our code coverage, our CI build will fail and you will not be able to merge.
