## Scalability & Extension Write-Up

To evolve this pipeline to support 10+ locales, multiple content types, and an editorial review workflow, I propose some enhancements as follows:

---

### 1. Supporting 10+ Locales

#### Locale-Specific Prompt Overrides
- Structure Jinja templates under `templates/{locale}/…` , so we can have specifc templates for avery locale.
- This will allow to tweak tone, examples, or instructions per locale without duplicating shared logic.

#### Translation Memory Integration
- Store validated translations of product names, feature bullets, and boilerplate so repeated LLM calls for identical fragments are skipped—improving consistency and reducing token usage.

---

### 2. Adding New Content Types

#### Flexible Contentful Schemas
- Define distinct Content Types in Contentful—e.g., `productPage` with detailed specs and `faqItem` with question/answer fields.
- Each type has its own JSON schema for draft entries.

#### Templated Prompts per Type
- In `prompts.jinja`, macros for each content type:
  - **Product Pages**: Accept product attributes, key features, technical specs; intro, detailed description, and a spec table.
  - **FAQs**: Accept a list of questions; SEO-optimized Q&A entries.

#### Generic input Extension
- Refactor the pipeline’s entrypoint to accept a `content_type` parameter.
- Based on that parameter, pick the right prompt macro, input data, and Contentful API endpoint.


---

### 3. Integrating Editorial Review Workflows

#### Draft & Review Status
- Add a custom `status` field (e.g., `needs_review`, `approved`) on each entry specially when a generation dont pass a quality check, allowing inthis way a quick human intervention to fix the content.

#### Notifications
- Configure a Contentful webhook to notify Slack channels or email lists when new drafts arrive, including direct editor links.

#### Editor Annotations
- Add `editorNotes` and `approvedBy` fields in the Contentful schema so reviewers can leave contextual feedback before publishing.
