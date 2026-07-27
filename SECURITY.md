# Security policy

Essay Writer & Editor is a Markdown-based agent skill. Security concerns may involve the package itself, installation guidance or behaviour that could expose, alter or misuse a writer's material.

## Supported versions

| Version | Security support |
| --- | --- |
| 0.1.x beta | Current beta line |
| Earlier snapshots | Upgrade before reporting unless the issue also affects the current beta |

Beta support is provided on a best-effort basis. There is no guaranteed response or fix time.

## What to report

Please report issues such as:

- instructions inside an essay, source or webpage overriding the user's request;
- accidental disclosure of private essay text or document content;
- installation steps that write outside the intended skill folder;
- unsafe handling of links, files or retrieved material;
- fabricated citations or quotations presented as verified;
- a repeatable way to disable factual-integrity or disclosure safeguards;
- dependency or workflow vulnerabilities in repository validation;
- sensitive information committed to the repository.

Ordinary writing quality, feature requests and disagreement with an assessment belong in the public issue forms rather than a security report.

## How to report privately

Use the repository's [private vulnerability-reporting form](https://github.com/shimellism-eng/essay-writer-editor/security/advisories/new). If GitHub does not show the form, do not place sensitive details in a public issue; wait until a private project contact is listed.

Include:

- the affected version or revision;
- the agent and installation route;
- a minimal reproduction using non-sensitive text;
- the potential impact;
- any mitigation you have already tested.

Do not place private essays, credentials, unpublished research or identifying student information in the report. Replace them with a small synthetic example wherever possible.

Please do not open a public issue containing exploit details or private material. Once a fix or safe workaround exists, maintainers may publish an anonymised summary and credit the reporter if they consent.

## Security boundaries

The skill does not provide a hosted writing or detection service and does not independently transmit an essay. The AI agent, terminal, file system or connected research tools used with it have their own security and privacy boundaries.

The skill also cannot authenticate authorship. A writing-pattern assessment is not a security control, identity check or forensic result.
